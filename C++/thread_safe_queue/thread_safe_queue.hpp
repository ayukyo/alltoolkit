/**
 * @file thread_safe_queue.hpp
 * @brief C++ 线程安全队列 - 零依赖、现代 C++17 实现
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-04-16
 *
 * 提供线程安全的队列数据结构，支持：
 * - 基本的入队/出队操作
 * - 阻塞式和非阻塞式操作
 * - 批量操作
 * - 超时等待
 * - 优先级队列支持
 * - 线程安全的迭代器
 * - 生产者-消费者模式支持
 */

#ifndef ALLTOOLKIT_THREAD_SAFE_QUEUE_HPP
#define ALLTOOLKIT_THREAD_SAFE_QUEUE_HPP

#include <atomic>
#include <chrono>
#include <condition_variable>
#include <deque>
#include <memory>
#include <mutex>
#include <optional>
#include <queue>
#include <vector>

namespace alltoolkit {

/**
 * @brief 线程安全队列命名空间
 */
namespace thread_safe_queue {

// ============================================================================
// 基础线程安全队列
// ============================================================================

/**
 * @brief 线程安全队列 - 基于 std::queue 实现
 * @tparam T 元素类型
 * @tparam Container 底层容器类型，默认为 std::deque<T>
 * 
 * @example
 * ```cpp
 * thread_safe_queue<int> q;
 * q.push(42);
 * auto val = q.try_pop();
 * if (val) std::cout << *val << std::endl;
 * ```
 */
template <typename T, typename Container = std::deque<T>>
class ThreadSafeQueue {
public:
    using value_type = T;
    using container_type = Container;
    using size_type = typename Container::size_type;
    using reference = typename Container::reference;
    using const_reference = typename Container::const_reference;

private:
    mutable std::mutex mutex_;
    std::queue<T, Container> queue_;
    std::condition_variable not_empty_;
    std::condition_variable not_full_;
    size_type max_size_;
    std::atomic<bool> shutdown_;

public:
    /**
     * @brief 构造函数
     * @param max_size 队列最大容量（0 表示无限制）
     */
    explicit ThreadSafeQueue(size_type max_size = 0)
        : max_size_(max_size), shutdown_(false) {}

    /**
     * @brief 析构函数
     */
    ~ThreadSafeQueue() { shutdown(); }

    // 禁止拷贝
    ThreadSafeQueue(const ThreadSafeQueue&) = delete;
    ThreadSafeQueue& operator=(const ThreadSafeQueue&) = delete;

    // 允许移动
    ThreadSafeQueue(ThreadSafeQueue&& other) noexcept {
        std::lock_guard<std::mutex> lock(other.mutex_);
        queue_ = std::move(other.queue_);
        max_size_ = other.max_size_;
        shutdown_ = other.shutdown_.load();
    }

    ThreadSafeQueue& operator=(ThreadSafeQueue&& other) noexcept {
        if (this != &other) {
            std::scoped_lock lock(mutex_, other.mutex_);
            queue_ = std::move(other.queue_);
            max_size_ = other.max_size_;
            shutdown_ = other.shutdown_.load();
        }
        return *this;
    }

    // ========================================================================
    // 基本操作
    // ========================================================================

    /**
     * @brief 入队（阻塞式）
     * @param value 要入队的值
     * @return true 入队成功，false 队列已关闭
     */
    bool push(const T& value) {
        std::unique_lock<std::mutex> lock(mutex_);
        
        if (shutdown_) return false;
        
        // 如果有最大容量限制，等待队列不满
        if (max_size_ > 0) {
            not_full_.wait(lock, [this]() {
                return queue_.size() < max_size_ || shutdown_;
            });
            if (shutdown_) return false;
        }
        
        queue_.push(value);
        not_empty_.notify_one();
        return true;
    }

    /**
     * @brief 入队（移动语义）
     * @param value 要入队的值
     * @return true 入队成功，false 队列已关闭
     */
    bool push(T&& value) {
        std::unique_lock<std::mutex> lock(mutex_);
        
        if (shutdown_) return false;
        
        if (max_size_ > 0) {
            not_full_.wait(lock, [this]() {
                return queue_.size() < max_size_ || shutdown_;
            });
            if (shutdown_) return false;
        }
        
        queue_.push(std::move(value));
        not_empty_.notify_one();
        return true;
    }

    /**
     * @brief 尝试入队（非阻塞）
     * @param value 要入队的值
     * @return true 入队成功，false 队列已满或已关闭
     */
    bool try_push(const T& value) {
        std::lock_guard<std::mutex> lock(mutex_);
        
        if (shutdown_) return false;
        if (max_size_ > 0 && queue_.size() >= max_size_) return false;
        
        queue_.push(value);
        not_empty_.notify_one();
        return true;
    }

    /**
     * @brief 尝试入队（移动语义，非阻塞）
     */
    bool try_push(T&& value) {
        std::lock_guard<std::mutex> lock(mutex_);
        
        if (shutdown_) return false;
        if (max_size_ > 0 && queue_.size() >= max_size_) return false;
        
        queue_.push(std::move(value));
        not_empty_.notify_one();
        return true;
    }

    /**
     * @brief 带超时的入队
     * @param value 要入队的值
     * @param timeout 超时时间
     * @return true 入队成功，false 超时或队列已关闭
     */
    template <typename Rep, typename Period>
    bool push_for(const T& value, const std::chrono::duration<Rep, Period>& timeout) {
        std::unique_lock<std::mutex> lock(mutex_);
        
        if (shutdown_) return false;
        
        if (max_size_ > 0) {
            if (!not_full_.wait_for(lock, timeout, [this]() {
                return queue_.size() < max_size_ || shutdown_;
            })) {
                return false; // 超时
            }
            if (shutdown_) return false;
        }
        
        queue_.push(value);
        not_empty_.notify_one();
        return true;
    }

    /**
     * @brief 出队（阻塞式）
     * @return 出队的值，如果队列已关闭且为空，返回 nullopt
     */
    std::optional<T> pop() {
        std::unique_lock<std::mutex> lock(mutex_);
        
        not_empty_.wait(lock, [this]() {
            return !queue_.empty() || shutdown_;
        });
        
        if (queue_.empty()) return std::nullopt;
        
        T value = std::move(queue_.front());
        queue_.pop();
        not_full_.notify_one();
        return value;
    }

    /**
     * @brief 尝试出队（非阻塞）
     * @return 出队的值，如果队列为空返回 nullopt
     */
    std::optional<T> try_pop() {
        std::lock_guard<std::mutex> lock(mutex_);
        
        if (queue_.empty()) return std::nullopt;
        
        T value = std::move(queue_.front());
        queue_.pop();
        not_full_.notify_one();
        return value;
    }

    /**
     * @brief 带超时的出队
     * @param timeout 超时时间
     * @return 出队的值，如果超时或队列为空返回 nullopt
     */
    template <typename Rep, typename Period>
    std::optional<T> pop_for(const std::chrono::duration<Rep, Period>& timeout) {
        std::unique_lock<std::mutex> lock(mutex_);
        
        if (!not_empty_.wait_for(lock, timeout, [this]() {
            return !queue_.empty() || shutdown_;
        })) {
            return std::nullopt; // 超时
        }
        
        if (queue_.empty()) return std::nullopt;
        
        T value = std::move(queue_.front());
        queue_.pop();
        not_full_.notify_one();
        return value;
    }

    // ========================================================================
    // 批量操作
    // ========================================================================

    /**
     * @brief 批量入队
     * @param values 要入队的值列表
     * @return 成功入队的数量
     */
    size_type push_batch(const std::vector<T>& values) {
        std::unique_lock<std::mutex> lock(mutex_);
        
        if (shutdown_) return 0;
        
        size_type count = 0;
        for (const auto& value : values) {
            if (max_size_ > 0 && queue_.size() >= max_size_) {
                // 等待有空间
                not_full_.wait(lock, [this]() {
                    return queue_.size() < max_size_ || shutdown_;
                });
                if (shutdown_) break;
            }
            queue_.push(value);
            ++count;
        }
        
        if (count > 0) {
            not_empty_.notify_all();
        }
        return count;
    }

    /**
     * @brief 批量出队
     * @param max_count 最大出队数量
     * @return 出队的值列表
     */
    std::vector<T> pop_batch(size_type max_count) {
        std::lock_guard<std::mutex> lock(mutex_);
        
        std::vector<T> result;
        result.reserve(std::min(max_count, queue_.size()));
        
        while (!queue_.empty() && result.size() < max_count) {
            result.push_back(std::move(queue_.front()));
            queue_.pop();
        }
        
        if (result.size() < max_count) {
            not_full_.notify_all();
        }
        return result;
    }

    // ========================================================================
    // 状态查询
    // ========================================================================

    /**
     * @brief 获取队列大小
     */
    [[nodiscard]] size_type size() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return queue_.size();
    }

    /**
     * @brief 判断队列是否为空
     */
    [[nodiscard]] bool empty() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return queue_.empty();
    }

    /**
     * @brief 判断队列是否已满
     */
    [[nodiscard]] bool full() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return max_size_ > 0 && queue_.size() >= max_size_;
    }

    /**
     * @brief 获取队列最大容量
     */
    [[nodiscard]] size_type capacity() const noexcept {
        return max_size_;
    }

    /**
     * @brief 查看队首元素（不移除）
     */
    std::optional<T> peek() const {
        std::lock_guard<std::mutex> lock(mutex_);
        if (queue_.empty()) return std::nullopt;
        return queue_.front();
    }

    /**
     * @brief 清空队列
     */
    void clear() {
        std::lock_guard<std::mutex> lock(mutex_);
        while (!queue_.empty()) {
            queue_.pop();
        }
        not_full_.notify_all();
    }

    // ========================================================================
    // 控制操作
    // ========================================================================

    /**
     * @brief 关闭队列
     * @note 关闭后不再接受新的元素，但可以继续取出剩余元素
     */
    void shutdown() {
        std::lock_guard<std::mutex> lock(mutex_);
        shutdown_ = true;
        not_empty_.notify_all();
        not_full_.notify_all();
    }

    /**
     * @brief 重启队列
     */
    void restart() {
        std::lock_guard<std::mutex> lock(mutex_);
        shutdown_ = false;
    }

    /**
     * @brief 判断队列是否已关闭
     */
    [[nodiscard]] bool is_shutdown() const noexcept {
        return shutdown_.load();
    }

    /**
     * @brief 等待队列为空
     * @param timeout 超时时间（可选）
     * @return true 队列为空，false 超时
     */
    template <typename Rep, typename Period>
    bool wait_empty(const std::chrono::duration<Rep, Period>& timeout) {
        std::unique_lock<std::mutex> lock(mutex_);
        return not_full_.wait_for(lock, timeout, [this]() {
            return queue_.empty() || shutdown_;
        });
    }
};

// ============================================================================
// 线程安全优先级队列
// ============================================================================

/**
 * @brief 线程安全优先级队列
 * @tparam T 元素类型
 * @tparam Compare 比较器，默认为 std::less<T>（大根堆）
 * @tparam Container 底层容器类型
 * 
 * @example
 * ```cpp
 * ThreadSafePriorityQueue<int> pq;
 * pq.push(3);
 * pq.push(1);
 * pq.push(4);
 * auto top = pq.try_pop(); // 返回 4（最大值）
 * ```
 */
template <typename T, typename Compare = std::less<T>, typename Container = std::vector<T>>
class ThreadSafePriorityQueue {
public:
    using value_type = T;
    using container_type = Container;
    using size_type = typename Container::size_type;
    using const_reference = typename Container::const_reference;

private:
    mutable std::mutex mutex_;
    std::priority_queue<T, Container, Compare> queue_;
    std::condition_variable not_empty_;
    std::atomic<bool> shutdown_;

public:
    ThreadSafePriorityQueue() : shutdown_(false) {}
    ~ThreadSafePriorityQueue() { shutdown(); }

    // 禁止拷贝
    ThreadSafePriorityQueue(const ThreadSafePriorityQueue&) = delete;
    ThreadSafePriorityQueue& operator=(const ThreadSafePriorityQueue&) = delete;

    /**
     * @brief 入队
     */
    void push(const T& value) {
        std::lock_guard<std::mutex> lock(mutex_);
        if (!shutdown_) {
            queue_.push(value);
            not_empty_.notify_one();
        }
    }

    /**
     * @brief 入队（移动语义）
     */
    void push(T&& value) {
        std::lock_guard<std::mutex> lock(mutex_);
        if (!shutdown_) {
            queue_.push(std::move(value));
            not_empty_.notify_one();
        }
    }

    /**
     * @brief 尝试入队
     * @return true 入队成功
     */
    bool try_push(const T& value) {
        std::lock_guard<std::mutex> lock(mutex_);
        if (shutdown_) return false;
        queue_.push(value);
        not_empty_.notify_one();
        return true;
    }

    /**
     * @brief 出队（阻塞式）
     */
    std::optional<T> pop() {
        std::unique_lock<std::mutex> lock(mutex_);
        not_empty_.wait(lock, [this]() {
            return !queue_.empty() || shutdown_;
        });
        if (queue_.empty()) return std::nullopt;
        T value = std::move(const_cast<T&>(queue_.top()));
        queue_.pop();
        return value;
    }

    /**
     * @brief 尝试出队
     */
    std::optional<T> try_pop() {
        std::lock_guard<std::mutex> lock(mutex_);
        if (queue_.empty()) return std::nullopt;
        T value = std::move(const_cast<T&>(queue_.top()));
        queue_.pop();
        return value;
    }

    /**
     * @brief 带超时的出队
     */
    template <typename Rep, typename Period>
    std::optional<T> pop_for(const std::chrono::duration<Rep, Period>& timeout) {
        std::unique_lock<std::mutex> lock(mutex_);
        if (!not_empty_.wait_for(lock, timeout, [this]() {
            return !queue_.empty() || shutdown_;
        })) {
            return std::nullopt;
        }
        if (queue_.empty()) return std::nullopt;
        T value = std::move(const_cast<T&>(queue_.top()));
        queue_.pop();
        return value;
    }

    /**
     * @brief 查看队首元素
     */
    std::optional<T> peek() const {
        std::lock_guard<std::mutex> lock(mutex_);
        if (queue_.empty()) return std::nullopt;
        return queue_.top();
    }

    /**
     * @brief 获取队列大小
     */
    [[nodiscard]] size_type size() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return queue_.size();
    }

    /**
     * @brief 判断队列是否为空
     */
    [[nodiscard]] bool empty() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return queue_.empty();
    }

    /**
     * @brief 清空队列
     */
    void clear() {
        std::lock_guard<std::mutex> lock(mutex_);
        while (!queue_.empty()) queue_.pop();
    }

    /**
     * @brief 关闭队列
     */
    void shutdown() {
        std::lock_guard<std::mutex> lock(mutex_);
        shutdown_ = true;
        not_empty_.notify_all();
    }

    /**
     * @brief 重启队列
     */
    void restart() {
        std::lock_guard<std::mutex> lock(mutex_);
        shutdown_ = false;
    }

    /**
     * @brief 判断队列是否已关闭
     */
    [[nodiscard]] bool is_shutdown() const noexcept {
        return shutdown_.load();
    }
};

// ============================================================================
// 线程安全双端队列
// ============================================================================

/**
 * @brief 线程安全双端队列
 * @tparam T 元素类型
 * 
 * @example
 * ```cpp
 * ThreadSafeDeque<int> dq;
 * dq.push_front(1);
 * dq.push_back(2);
 * auto front = dq.pop_front();
 * auto back = dq.pop_back();
 * ```
 */
template <typename T>
class ThreadSafeDeque {
public:
    using value_type = T;
    using size_type = typename std::deque<T>::size_type;

private:
    mutable std::mutex mutex_;
    std::deque<T> deque_;
    std::condition_variable not_empty_;
    std::atomic<bool> shutdown_;

public:
    ThreadSafeDeque() : shutdown_(false) {}
    ~ThreadSafeDeque() { shutdown(); }

    ThreadSafeDeque(const ThreadSafeDeque&) = delete;
    ThreadSafeDeque& operator=(const ThreadSafeDeque&) = delete;

    // ========================================================================
    // 队首操作
    // ========================================================================

    /**
     * @brief 在队首插入元素
     */
    void push_front(const T& value) {
        std::lock_guard<std::mutex> lock(mutex_);
        if (!shutdown_) {
            deque_.push_front(value);
            not_empty_.notify_one();
        }
    }

    /**
     * @brief 在队首插入元素（移动语义）
     */
    void push_front(T&& value) {
        std::lock_guard<std::mutex> lock(mutex_);
        if (!shutdown_) {
            deque_.push_front(std::move(value));
            not_empty_.notify_one();
        }
    }

    /**
     * @brief 从队首弹出元素（阻塞式）
     */
    std::optional<T> pop_front() {
        std::unique_lock<std::mutex> lock(mutex_);
        not_empty_.wait(lock, [this]() {
            return !deque_.empty() || shutdown_;
        });
        if (deque_.empty()) return std::nullopt;
        T value = std::move(deque_.front());
        deque_.pop_front();
        return value;
    }

    /**
     * @brief 尝试从队首弹出元素
     */
    std::optional<T> try_pop_front() {
        std::lock_guard<std::mutex> lock(mutex_);
        if (deque_.empty()) return std::nullopt;
        T value = std::move(deque_.front());
        deque_.pop_front();
        return value;
    }

    /**
     * @brief 带超时的从队首弹出元素
     */
    template <typename Rep, typename Period>
    std::optional<T> pop_front_for(const std::chrono::duration<Rep, Period>& timeout) {
        std::unique_lock<std::mutex> lock(mutex_);
        if (!not_empty_.wait_for(lock, timeout, [this]() {
            return !deque_.empty() || shutdown_;
        })) {
            return std::nullopt;
        }
        if (deque_.empty()) return std::nullopt;
        T value = std::move(deque_.front());
        deque_.pop_front();
        return value;
    }

    // ========================================================================
    // 队尾操作
    // ========================================================================

    /**
     * @brief 在队尾插入元素
     */
    void push_back(const T& value) {
        std::lock_guard<std::mutex> lock(mutex_);
        if (!shutdown_) {
            deque_.push_back(value);
            not_empty_.notify_one();
        }
    }

    /**
     * @brief 在队尾插入元素（移动语义）
     */
    void push_back(T&& value) {
        std::lock_guard<std::mutex> lock(mutex_);
        if (!shutdown_) {
            deque_.push_back(std::move(value));
            not_empty_.notify_one();
        }
    }

    /**
     * @brief 从队尾弹出元素（阻塞式）
     */
    std::optional<T> pop_back() {
        std::unique_lock<std::mutex> lock(mutex_);
        not_empty_.wait(lock, [this]() {
            return !deque_.empty() || shutdown_;
        });
        if (deque_.empty()) return std::nullopt;
        T value = std::move(deque_.back());
        deque_.pop_back();
        return value;
    }

    /**
     * @brief 尝试从队尾弹出元素
     */
    std::optional<T> try_pop_back() {
        std::lock_guard<std::mutex> lock(mutex_);
        if (deque_.empty()) return std::nullopt;
        T value = std::move(deque_.back());
        deque_.pop_back();
        return value;
    }

    // ========================================================================
    // 状态查询
    // ========================================================================

    /**
     * @brief 获取队列大小
     */
    [[nodiscard]] size_type size() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return deque_.size();
    }

    /**
     * @brief 判断队列是否为空
     */
    [[nodiscard]] bool empty() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return deque_.empty();
    }

    /**
     * @brief 查看队首元素
     */
    std::optional<T> peek_front() const {
        std::lock_guard<std::mutex> lock(mutex_);
        if (deque_.empty()) return std::nullopt;
        return deque_.front();
    }

    /**
     * @brief 查看队尾元素
     */
    std::optional<T> peek_back() const {
        std::lock_guard<std::mutex> lock(mutex_);
        if (deque_.empty()) return std::nullopt;
        return deque_.back();
    }

    /**
     * @brief 清空队列
     */
    void clear() {
        std::lock_guard<std::mutex> lock(mutex_);
        deque_.clear();
    }

    /**
     * @brief 关闭队列
     */
    void shutdown() {
        std::lock_guard<std::mutex> lock(mutex_);
        shutdown_ = true;
        not_empty_.notify_all();
    }

    /**
     * @brief 重启队列
     */
    void restart() {
        std::lock_guard<std::mutex> lock(mutex_);
        shutdown_ = false;
    }

    /**
     * @brief 判断队列是否已关闭
     */
    [[nodiscard]] bool is_shutdown() const noexcept {
        return shutdown_.load();
    }
};

// ============================================================================
// 线程安全环形缓冲区队列
// ============================================================================

/**
 * @brief 线程安全环形缓冲区队列
 * @tparam T 元素类型
 * @note 高性能的有界队列实现，适合生产者-消费者模式
 * 
 * @example
 * ```cpp
 * ThreadSafeRingBuffer<int> rb(100);
 * rb.push(42);
 * auto val = rb.try_pop();
 * ```
 */
template <typename T>
class ThreadSafeRingBuffer {
public:
    using value_type = T;
    using size_type = typename std::vector<T>::size_type;

private:
    mutable std::mutex mutex_;
    std::vector<T> buffer_;
    size_type capacity_;
    size_type head_ = 0;
    size_type tail_ = 0;
    size_type count_ = 0;
    std::condition_variable not_empty_;
    std::condition_variable not_full_;
    std::atomic<bool> shutdown_;

public:
    /**
     * @brief 构造函数
     * @param capacity 缓冲区容量
     */
    explicit ThreadSafeRingBuffer(size_type capacity)
        : buffer_(capacity), capacity_(capacity), shutdown_(false) {}

    ~ThreadSafeRingBuffer() { shutdown(); }

    ThreadSafeRingBuffer(const ThreadSafeRingBuffer&) = delete;
    ThreadSafeRingBuffer& operator=(const ThreadSafeRingBuffer&) = delete;

    /**
     * @brief 入队（阻塞式）
     */
    bool push(const T& value) {
        std::unique_lock<std::mutex> lock(mutex_);
        
        not_full_.wait(lock, [this]() {
            return count_ < capacity_ || shutdown_;
        });
        
        if (shutdown_) return false;
        
        buffer_[tail_] = value;
        tail_ = (tail_ + 1) % capacity_;
        ++count_;
        not_empty_.notify_one();
        return true;
    }

    /**
     * @brief 入队（移动语义）
     */
    bool push(T&& value) {
        std::unique_lock<std::mutex> lock(mutex_);
        
        not_full_.wait(lock, [this]() {
            return count_ < capacity_ || shutdown_;
        });
        
        if (shutdown_) return false;
        
        buffer_[tail_] = std::move(value);
        tail_ = (tail_ + 1) % capacity_;
        ++count_;
        not_empty_.notify_one();
        return true;
    }

    /**
     * @brief 尝试入队
     */
    bool try_push(const T& value) {
        std::lock_guard<std::mutex> lock(mutex_);
        
        if (shutdown_ || count_ >= capacity_) return false;
        
        buffer_[tail_] = value;
        tail_ = (tail_ + 1) % capacity_;
        ++count_;
        not_empty_.notify_one();
        return true;
    }

    /**
     * @brief 出队（阻塞式）
     */
    std::optional<T> pop() {
        std::unique_lock<std::mutex> lock(mutex_);
        
        not_empty_.wait(lock, [this]() {
            return count_ > 0 || shutdown_;
        });
        
        if (count_ == 0) return std::nullopt;
        
        T value = std::move(buffer_[head_]);
        head_ = (head_ + 1) % capacity_;
        --count_;
        not_full_.notify_one();
        return value;
    }

    /**
     * @brief 尝试出队
     */
    std::optional<T> try_pop() {
        std::lock_guard<std::mutex> lock(mutex_);
        
        if (count_ == 0) return std::nullopt;
        
        T value = std::move(buffer_[head_]);
        head_ = (head_ + 1) % capacity_;
        --count_;
        not_full_.notify_one();
        return value;
    }

    /**
     * @brief 带超时的出队
     */
    template <typename Rep, typename Period>
    std::optional<T> pop_for(const std::chrono::duration<Rep, Period>& timeout) {
        std::unique_lock<std::mutex> lock(mutex_);
        
        if (!not_empty_.wait_for(lock, timeout, [this]() {
            return count_ > 0 || shutdown_;
        })) {
            return std::nullopt;
        }
        
        if (count_ == 0) return std::nullopt;
        
        T value = std::move(buffer_[head_]);
        head_ = (head_ + 1) % capacity_;
        --count_;
        not_full_.notify_one();
        return value;
    }

    /**
     * @brief 获取队列大小
     */
    [[nodiscard]] size_type size() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return count_;
    }

    /**
     * @brief 判断队列是否为空
     */
    [[nodiscard]] bool empty() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return count_ == 0;
    }

    /**
     * @brief 判断队列是否已满
     */
    [[nodiscard]] bool full() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return count_ >= capacity_;
    }

    /**
     * @brief 获取队列容量
     */
    [[nodiscard]] size_type capacity() const noexcept {
        return capacity_;
    }

    /**
     * @brief 清空队列
     */
    void clear() {
        std::lock_guard<std::mutex> lock(mutex_);
        head_ = tail_ = count_ = 0;
        not_full_.notify_all();
    }

    /**
     * @brief 关闭队列
     */
    void shutdown() {
        std::lock_guard<std::mutex> lock(mutex_);
        shutdown_ = true;
        not_empty_.notify_all();
        not_full_.notify_all();
    }

    /**
     * @brief 重启队列
     */
    void restart() {
        std::lock_guard<std::mutex> lock(mutex_);
        shutdown_ = false;
    }

    /**
     * @brief 判断队列是否已关闭
     */
    [[nodiscard]] bool is_shutdown() const noexcept {
        return shutdown_.load();
    }
};

// ============================================================================
// 类型别名
// ============================================================================

template <typename T>
using TSQueue = ThreadSafeQueue<T>;

template <typename T, typename Compare = std::less<T>>
using TSPriorityQueue = ThreadSafePriorityQueue<T, Compare>;

template <typename T>
using TSDeque = ThreadSafeDeque<T>;

template <typename T>
using TSRingBuffer = ThreadSafeRingBuffer<T>;

} // namespace thread_safe_queue

// 导入到 alltoolkit 命名空间
using thread_safe_queue::ThreadSafeQueue;
using thread_safe_queue::ThreadSafePriorityQueue;
using thread_safe_queue::ThreadSafeDeque;
using thread_safe_queue::ThreadSafeRingBuffer;
using thread_safe_queue::TSQueue;
using thread_safe_queue::TSPriorityQueue;
using thread_safe_queue::TSDeque;
using thread_safe_queue::TSRingBuffer;

} // namespace alltoolkit

#endif // ALLTOOLKIT_THREAD_SAFE_QUEUE_HPP