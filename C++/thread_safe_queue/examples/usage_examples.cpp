/**
 * @file usage_examples.cpp
 * @brief 线程安全队列使用示例
 * @author AllToolkit
 * @date 2026-04-16
 */

#include "thread_safe_queue.hpp"
#include <chrono>
#include <iostream>
#include <thread>
#include <vector>

using namespace alltoolkit;

// ============================================================================
// 示例 1: 基本队列操作
// ============================================================================

void example_basic_queue() {
    std::cout << "\n=== 示例 1: 基本队列操作 ===" << std::endl;
    
    ThreadSafeQueue<int> queue;
    
    // 入队
    queue.push(10);
    queue.push(20);
    queue.push(30);
    
    std::cout << "队列大小: " << queue.size() << std::endl;
    
    // 非阻塞出队
    while (!queue.empty()) {
        auto val = queue.try_pop();
        if (val) {
            std::cout << "出队: " << *val << std::endl;
        }
    }
    
    std::cout << "队列是否为空: " << queue.empty() << std::endl;
}

// ============================================================================
// 示例 2: 有界队列
// ============================================================================

void example_bounded_queue() {
    std::cout << "\n=== 示例 2: 有界队列 ===" << std::endl;
    
    // 创建容量为 3 的有界队列
    ThreadSafeQueue<int> queue(3);
    
    // 填满队列
    queue.try_push(1);
    queue.try_push(2);
    queue.try_push(3);
    
    std::cout << "队列大小: " << queue.size() << " (容量: " << queue.capacity() << ")" << std::endl;
    std::cout << "队列是否已满: " << queue.full() << std::endl;
    
    // 尝试再入队（会失败）
    if (!queue.try_push(4)) {
        std::cout << "队列已满，入队失败" << std::endl;
    }
    
    // 出队一个元素
    auto val = queue.try_pop();
    std::cout << "出队: " << (val ? std::to_string(*val) : "无") << std::endl;
    
    // 现在可以再入队
    if (queue.try_push(4)) {
        std::cout << "入队成功: 4" << std::endl;
    }
}

// ============================================================================
// 示例 3: 生产者-消费者模式
// ============================================================================

void example_producer_consumer() {
    std::cout << "\n=== 示例 3: 生产者-消费者模式 ===" << std::endl;
    
    ThreadSafeQueue<int> queue(10);
    const int total_items = 20;
    
    // 生产者线程
    std::thread producer([&]() {
        for (int i = 0; i < total_items; ++i) {
            queue.push(i);
            std::cout << "[生产者] 生产: " << i << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(10));
        }
        queue.shutdown(); // 生产完成后关闭队列
        std::cout << "[生产者] 完成，关闭队列" << std::endl;
    });
    
    // 消费者线程
    std::thread consumer([&]() {
        int count = 0;
        while (true) {
            auto val = queue.pop(); // 阻塞等待
            if (!val) {
                // 队列已关闭且为空
                std::cout << "[消费者] 队列已关闭，退出" << std::endl;
                break;
            }
            std::cout << "[消费者] 消费: " << *val << std::endl;
            count++;
        }
        std::cout << "[消费者] 共消费 " << count << " 个元素" << std::endl;
    });
    
    producer.join();
    consumer.join();
}

// ============================================================================
// 示例 4: 优先级队列
// ============================================================================

void example_priority_queue() {
    std::cout << "\n=== 示例 4: 优先级队列 ===" << std::endl;
    
    // 大根堆（默认）
    ThreadSafePriorityQueue<int> max_pq;
    
    max_pq.push(3);
    max_pq.push(1);
    max_pq.push(4);
    max_pq.push(1);
    max_pq.push(5);
    
    std::cout << "大根堆出队顺序:" << std::endl;
    while (!max_pq.empty()) {
        auto val = max_pq.try_pop();
        std::cout << *val << " ";
    }
    std::cout << std::endl;
    
    // 小根堆
    ThreadSafePriorityQueue<int, std::greater<int>> min_pq;
    
    min_pq.push(3);
    min_pq.push(1);
    min_pq.push(4);
    min_pq.push(1);
    min_pq.push(5);
    
    std::cout << "小根堆出队顺序:" << std::endl;
    while (!min_pq.empty()) {
        auto val = min_pq.try_pop();
        std::cout << *val << " ";
    }
    std::cout << std::endl;
}

// ============================================================================
// 示例 5: 双端队列
// ============================================================================

void example_deque() {
    std::cout << "\n=== 示例 5: 双端队列 ===" << std::endl;
    
    ThreadSafeDeque<int> dq;
    
    // 从两端入队
    dq.push_back(1);  // 队尾: [1]
    dq.push_front(2); // 队首: [2, 1]
    dq.push_back(3);  // 队尾: [2, 1, 3]
    dq.push_front(4); // 队首: [4, 2, 1, 3]
    
    std::cout << "队列大小: " << dq.size() << std::endl;
    
    auto front = dq.peek_front();
    auto back = dq.peek_back();
    std::cout << "队首: " << (front ? std::to_string(*front) : "无") << std::endl;
    std::cout << "队尾: " << (back ? std::to_string(*back) : "无") << std::endl;
    
    // 从队首出队
    std::cout << "队首出队顺序:" << std::endl;
    while (!dq.empty()) {
        auto val = dq.try_pop_front();
        std::cout << *val << " ";
    }
    std::cout << std::endl;
}

// ============================================================================
// 示例 6: 环形缓冲区
// ============================================================================

void example_ring_buffer() {
    std::cout << "\n=== 示例 6: 环形缓冲区 ===" << std::endl;
    
    ThreadSafeRingBuffer<int> rb(5);
    
    // 填满缓冲区
    for (int i = 1; i <= 5; ++i) {
        rb.try_push(i);
    }
    
    std::cout << "缓冲区大小: " << rb.size() << " (容量: " << rb.capacity() << ")" << std::endl;
    std::cout << "是否已满: " << rb.full() << std::endl;
    
    // 出队 2 个
    auto v1 = rb.try_pop();
    auto v2 = rb.try_pop();
    std::cout << "出队: " << *v1 << ", " << *v2 << std::endl;
    
    // 再入队 2 个（环绕写入）
    rb.try_push(6);
    rb.try_push(7);
    
    std::cout << "剩余元素:" << std::endl;
    while (!rb.empty()) {
        auto val = rb.try_pop();
        std::cout << *val << " ";
    }
    std::cout << std::endl;
}

// ============================================================================
// 示例 7: 超时等待
// ============================================================================

void example_timeout() {
    std::cout << "\n=== 示例 7: 超时等待 ===" << std::endl;
    
    ThreadSafeQueue<int> queue;
    
    // 带超时的出队（队列为空）
    auto start = std::chrono::steady_clock::now();
    auto val = queue.pop_for(std::chrono::milliseconds(100));
    auto end = std::chrono::steady_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    std::cout << "等待时间: " << duration.count() << "ms" << std::endl;
    std::cout << "出队结果: " << (val ? std::to_string(*val) : "超时") << std::endl;
}

// ============================================================================
// 示例 8: 批量操作
// ============================================================================

void example_batch_operations() {
    std::cout << "\n=== 示例 8: 批量操作 ===" << std::endl;
    
    ThreadSafeQueue<int> queue;
    
    // 批量入队
    std::vector<int> items = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    size_t count = queue.push_batch(items);
    std::cout << "批量入队: " << count << " 个元素" << std::endl;
    
    // 批量出队
    auto batch = queue.pop_batch(5);
    std::cout << "批量出队 5 个:" << std::endl;
    for (auto val : batch) {
        std::cout << val << " ";
    }
    std::cout << std::endl;
    
    std::cout << "剩余元素数量: " << queue.size() << std::endl;
}

// ============================================================================
// 示例 9: 多线程协作
// ============================================================================

void example_thread_pool_style() {
    std::cout << "\n=== 示例 9: 多线程协作（线程池风格） ===" << std::endl;
    
    ThreadSafeQueue<std::function<void()>> task_queue(100);
    std::atomic<bool> running{true};
    
    // 工作线程
    std::vector<std::thread> workers;
    for (int i = 0; i < 3; ++i) {
        workers.emplace_back([&]() {
            while (running) {
                auto task = task_queue.pop_for(std::chrono::milliseconds(100));
                if (task) {
                    (*task)();
                }
            }
        });
    }
    
    // 添加任务
    for (int i = 0; i < 10; ++i) {
        task_queue.push([i]() {
            std::cout << "[工作线程] 执行任务 " << i << std::endl;
        });
    }
    
    // 等待任务完成
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    
    // 停止工作线程
    running = false;
    task_queue.shutdown();
    
    for (auto& w : workers) {
        w.join();
    }
    
    std::cout << "所有任务完成" << std::endl;
}

// ============================================================================
// 示例 10: 使用类型别名
// ============================================================================

void example_type_aliases() {
    std::cout << "\n=== 示例 10: 使用类型别名 ===" << std::endl;
    
    // 使用简短的类型别名
    TSQueue<int> queue;          // ThreadSafeQueue
    TSPriorityQueue<int> pq;     // ThreadSafePriorityQueue
    TSDeque<int> dq;             // ThreadSafeDeque
    TSRingBuffer<int> rb(10);    // ThreadSafeRingBuffer
    
    queue.push(42);
    pq.push(10);
    dq.push_back(5);
    rb.try_push(7);
    
    std::cout << "队列大小: " << queue.size() << std::endl;
    std::cout << "优先级队列大小: " << pq.size() << std::endl;
    std::cout << "双端队列大小: " << dq.size() << std::endl;
    std::cout << "环形缓冲区大小: " << rb.size() << std::endl;
}

// ============================================================================
// 主函数
// ============================================================================

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "线程安全队列使用示例" << std::endl;
    std::cout << "========================================" << std::endl;
    
    example_basic_queue();
    example_bounded_queue();
    example_producer_consumer();
    example_priority_queue();
    example_deque();
    example_ring_buffer();
    example_timeout();
    example_batch_operations();
    example_thread_pool_style();
    example_type_aliases();
    
    std::cout << "\n========================================" << std::endl;
    std::cout << "所有示例执行完成" << std::endl;
    std::cout << "========================================" << std::endl;
    
    return 0;
}