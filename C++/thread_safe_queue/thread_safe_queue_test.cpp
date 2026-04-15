/**
 * @file thread_safe_queue_test.cpp
 * @brief 线程安全队列测试文件
 * @author AllToolkit
 * @date 2026-04-16
 */

#include "thread_safe_queue.hpp"
#include <cassert>
#include <chrono>
#include <iostream>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

using namespace alltoolkit;

// ============================================================================
// 测试辅助宏
// ============================================================================

#define TEST_ASSERT(condition, message) \
    do { \
        if (!(condition)) { \
            std::cerr << "测试失败: " << message << std::endl; \
            return false; \
        } \
    } while (0)

#define TEST_PASS(name) \
    std::cout << "[PASS] " << name << std::endl

// ============================================================================
// ThreadSafeQueue 基础测试
// ============================================================================

bool test_basic_queue_operations() {
    ThreadSafeQueue<int> queue;
    
    // 测试初始状态
    TEST_ASSERT(queue.empty(), "新队列应为空");
    TEST_ASSERT(queue.size() == 0, "新队列大小应为 0");
    
    // 测试入队
    TEST_ASSERT(queue.push(1), "入队 1 应成功");
    TEST_ASSERT(queue.push(2), "入队 2 应成功");
    TEST_ASSERT(queue.push(3), "入队 3 应成功");
    TEST_ASSERT(queue.size() == 3, "队列大小应为 3");
    TEST_ASSERT(!queue.empty(), "队列不应为空");
    
    // 测试查看队首
    auto peek = queue.peek();
    TEST_ASSERT(peek.has_value() && peek.value() == 1, "队首应为 1");
    
    // 测试非阻塞出队
    auto val1 = queue.try_pop();
    TEST_ASSERT(val1.has_value() && val1.value() == 1, "出队应为 1");
    
    auto val2 = queue.try_pop();
    TEST_ASSERT(val2.has_value() && val2.value() == 2, "出队应为 2");
    
    auto val3 = queue.try_pop();
    TEST_ASSERT(val3.has_value() && val3.value() == 3, "出队应为 3");
    
    // 测试空队列出队
    auto val4 = queue.try_pop();
    TEST_ASSERT(!val4.has_value(), "空队列出队应为 nullopt");
    
    TEST_ASSERT(queue.empty(), "队列应为空");
    TEST_ASSERT(queue.size() == 0, "队列大小应为 0");
    
    return true;
}

bool test_bounded_queue() {
    ThreadSafeQueue<int> queue(3); // 最大容量 3
    
    // 填满队列
    TEST_ASSERT(queue.try_push(1), "入队 1 应成功");
    TEST_ASSERT(queue.try_push(2), "入队 2 应成功");
    TEST_ASSERT(queue.try_push(3), "入队 3 应成功");
    TEST_ASSERT(queue.full(), "队列应已满");
    
    // 测试队列满时入队失败
    TEST_ASSERT(!queue.try_push(4), "队列已满时入队应失败");
    
    // 出队一个元素
    auto val = queue.try_pop();
    TEST_ASSERT(val.has_value() && val.value() == 1, "出队应为 1");
    TEST_ASSERT(!queue.full(), "队列不应再满");
    
    // 现在应该能入队了
    TEST_ASSERT(queue.try_push(4), "入队 4 应成功");
    
    return true;
}

bool test_queue_clear() {
    ThreadSafeQueue<int> queue;
    
    queue.push(1);
    queue.push(2);
    queue.push(3);
    
    TEST_ASSERT(queue.size() == 3, "队列大小应为 3");
    
    queue.clear();
    
    TEST_ASSERT(queue.empty(), "清空后队列应为空");
    TEST_ASSERT(queue.size() == 0, "清空后大小应为 0");
    
    return true;
}

bool test_queue_shutdown() {
    ThreadSafeQueue<int> queue;
    
    // 关闭队列
    queue.shutdown();
    TEST_ASSERT(queue.is_shutdown(), "队列应已关闭");
    
    // 关闭后入队应失败
    TEST_ASSERT(!queue.push(1), "关闭后入队应失败");
    TEST_ASSERT(!queue.try_push(2), "关闭后入队应失败");
    
    // 重启队列
    queue.restart();
    TEST_ASSERT(!queue.is_shutdown(), "队列应未关闭");
    
    // 重启后应能入队
    TEST_ASSERT(queue.push(3), "重启后入队应成功");
    
    return true;
}

bool test_batch_operations() {
    ThreadSafeQueue<int> queue;
    
    // 批量入队
    std::vector<int> items = {1, 2, 3, 4, 5};
    auto count = queue.push_batch(items);
    TEST_ASSERT(count == 5, "批量入队 5 个元素");
    TEST_ASSERT(queue.size() == 5, "队列大小应为 5");
    
    // 批量出队
    auto result = queue.pop_batch(3);
    TEST_ASSERT(result.size() == 3, "批量出队 3 个元素");
    TEST_ASSERT(result[0] == 1 && result[1] == 2 && result[2] == 3, "出队元素应正确");
    
    TEST_ASSERT(queue.size() == 2, "队列剩余 2 个元素");
    
    return true;
}

// ============================================================================
// ThreadSafePriorityQueue 测试
// ============================================================================

bool test_priority_queue_basic() {
    ThreadSafePriorityQueue<int> pq;
    
    // 测试初始状态
    TEST_ASSERT(pq.empty(), "新队列应为空");
    
    // 入队（无序）
    pq.push(3);
    pq.push(1);
    pq.push(4);
    pq.push(1);
    pq.push(5);
    pq.push(9);
    
    TEST_ASSERT(pq.size() == 6, "队列大小应为 6");
    
    // 默认大根堆，出队顺序应为降序
    auto v1 = pq.try_pop();
    TEST_ASSERT(v1.has_value() && v1.value() == 9, "最大值应为 9");
    
    auto v2 = pq.try_pop();
    TEST_ASSERT(v2.has_value() && v2.value() == 5, "第二大值应为 5");
    
    auto v3 = pq.try_pop();
    TEST_ASSERT(v3.has_value() && v3.value() == 4, "第三大值应为 4");
    
    auto v4 = pq.try_pop();
    TEST_ASSERT(v4.has_value() && v4.value() == 3, "第四大值应为 3");
    
    auto v5 = pq.try_pop();
    TEST_ASSERT(v5.has_value() && v5.value() == 1, "第五大值应为 1");
    
    auto v6 = pq.try_pop();
    TEST_ASSERT(v6.has_value() && v6.value() == 1, "第六大值应为 1");
    
    // 队列为空
    auto v7 = pq.try_pop();
    TEST_ASSERT(!v7.has_value(), "空队列出队应为 nullopt");
    
    return true;
}

bool test_priority_queue_peek() {
    ThreadSafePriorityQueue<int> pq;
    
    // 空队列查看
    auto peek = pq.peek();
    TEST_ASSERT(!peek.has_value(), "空队列查看应为 nullopt");
    
    pq.push(42);
    
    peek = pq.peek();
    TEST_ASSERT(peek.has_value() && peek.value() == 42, "查看应为 42");
    
    // 查看不应改变队列
    TEST_ASSERT(pq.size() == 1, "队列大小应仍为 1");
    
    return true;
}

// ============================================================================
// ThreadSafeDeque 测试
// ============================================================================

bool test_deque_basic() {
    ThreadSafeDeque<int> dq;
    
    // 测试初始状态
    TEST_ASSERT(dq.empty(), "新双端队列应为空");
    
    // 队首入队
    dq.push_front(1);
    dq.push_front(2);
    dq.push_front(3);
    // 队列: [3, 2, 1]
    
    TEST_ASSERT(dq.size() == 3, "队列大小应为 3");
    
    // 查看队首和队尾
    auto front = dq.peek_front();
    auto back = dq.peek_back();
    TEST_ASSERT(front.has_value() && front.value() == 3, "队首应为 3");
    TEST_ASSERT(back.has_value() && back.value() == 1, "队尾应为 1");
    
    // 队尾入队
    dq.push_back(4);
    // 队列: [3, 2, 1, 4]
    
    back = dq.peek_back();
    TEST_ASSERT(back.has_value() && back.value() == 4, "队尾应为 4");
    
    // 队首出队
    auto val = dq.try_pop_front();
    TEST_ASSERT(val.has_value() && val.value() == 3, "队首出队应为 3");
    
    // 队尾出队
    val = dq.try_pop_back();
    TEST_ASSERT(val.has_value() && val.value() == 4, "队尾出队应为 4");
    
    // 队列: [2, 1]
    TEST_ASSERT(dq.size() == 2, "队列大小应为 2");
    
    return true;
}

// ============================================================================
// ThreadSafeRingBuffer 测试
// ============================================================================

bool test_ring_buffer_basic() {
    ThreadSafeRingBuffer<int> rb(5);
    
    // 测试初始状态
    TEST_ASSERT(rb.empty(), "新缓冲区应为空");
    TEST_ASSERT(!rb.full(), "新缓冲区不应满");
    TEST_ASSERT(rb.capacity() == 5, "容量应为 5");
    
    // 填满缓冲区
    for (int i = 1; i <= 5; ++i) {
        TEST_ASSERT(rb.try_push(i), "入队应成功");
    }
    
    TEST_ASSERT(rb.full(), "缓冲区应已满");
    TEST_ASSERT(rb.size() == 5, "大小应为 5");
    
    // 测试队列满时入队失败
    TEST_ASSERT(!rb.try_push(6), "缓冲区满时入队应失败");
    
    // 出队
    for (int i = 1; i <= 5; ++i) {
        auto val = rb.try_pop();
        TEST_ASSERT(val.has_value() && val.value() == i, "出队值应正确");
    }
    
    TEST_ASSERT(rb.empty(), "缓冲区应为空");
    
    return true;
}

bool test_ring_buffer_wrap_around() {
    ThreadSafeRingBuffer<int> rb(3);
    
    // 填满: [1, 2, 3]
    rb.try_push(1);
    rb.try_push(2);
    rb.try_push(3);
    
    // 出队 2 个
    rb.try_pop(); // 1
    rb.try_pop(); // 2
    // 缓冲区: [_, _, 3]
    
    // 再入队 2 个（环绕）
    rb.try_push(4);
    rb.try_push(5);
    // 缓冲区: [4, 5, 3]
    
    TEST_ASSERT(rb.size() == 3, "大小应为 3");
    
    // 出队顺序应为: 3, 4, 5
    auto v1 = rb.try_pop();
    auto v2 = rb.try_pop();
    auto v3 = rb.try_pop();
    
    TEST_ASSERT(v1.has_value() && v1.value() == 3, "出队应为 3");
    TEST_ASSERT(v2.has_value() && v2.value() == 4, "出队应为 4");
    TEST_ASSERT(v3.has_value() && v3.value() == 5, "出队应为 5");
    
    return true;
}

// ============================================================================
// 多线程测试
// ============================================================================

bool test_multithreaded_queue() {
    ThreadSafeQueue<int> queue;
    const int producer_count = 3;
    const int consumer_count = 2;
    const int items_per_producer = 100;
    
    std::vector<std::thread> producers;
    std::vector<std::thread> consumers;
    std::atomic<int> total_consumed{0};
    std::atomic<int> sum{0};
    
    // 启动生产者
    for (int p = 0; p < producer_count; ++p) {
        producers.emplace_back([&queue, p]() {
            for (int i = 0; i < items_per_producer; ++i) {
                queue.push(p * items_per_producer + i);
            }
        });
    }
    
    // 启动消费者
    for (int c = 0; c < consumer_count; ++c) {
        consumers.emplace_back([&queue, &total_consumed, &sum]() {
            int local_count = 0;
            while (local_count < (producer_count * items_per_producer) / consumer_count + 10) {
                auto val = queue.pop_for(std::chrono::milliseconds(10));
                if (val.has_value()) {
                    sum += val.value();
                    total_consumed++;
                }
            }
        });
    }
    
    // 等待生产者完成
    for (auto& t : producers) {
        t.join();
    }
    
    // 关闭队列以唤醒消费者
    queue.shutdown();
    
    // 等待消费者完成
    for (auto& t : consumers) {
        t.join();
    }
    
    // 验证
    int expected_total = producer_count * items_per_producer;
    TEST_ASSERT(total_consumed == expected_total, 
                 "消费总数应等于生产总数");
    
    // 计算期望的和
    int expected_sum = 0;
    for (int i = 0; i < expected_total; ++i) {
        expected_sum += i;
    }
    TEST_ASSERT(sum == expected_sum, "元素和应正确");
    
    return true;
}

bool test_multithreaded_ring_buffer() {
    ThreadSafeRingBuffer<int> rb(100);
    const int total_items = 1000;
    std::atomic<int> produced{0};
    std::atomic<int> consumed{0};
    std::atomic<bool> done{false};
    
    // 生产者线程
    std::thread producer([&]() {
        for (int i = 0; i < total_items; ++i) {
            while (!rb.try_push(i)) {
                std::this_thread::yield();
            }
            produced++;
        }
        done = true;
    });
    
    // 消费者线程
    std::thread consumer([&]() {
        while (!done || !rb.empty()) {
            auto val = rb.pop_for(std::chrono::milliseconds(1));
            if (val.has_value()) {
                consumed++;
            }
        }
    });
    
    producer.join();
    consumer.join();
    
    TEST_ASSERT(produced == total_items, "生产数应正确");
    TEST_ASSERT(consumed == total_items, "消费数应正确");
    
    return true;
}

// ============================================================================
// 超时测试
// ============================================================================

bool test_queue_timeout() {
    ThreadSafeQueue<int> queue;
    
    // 测试空队列超时
    auto start = std::chrono::steady_clock::now();
    auto val = queue.pop_for(std::chrono::milliseconds(100));
    auto end = std::chrono::steady_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    TEST_ASSERT(!val.has_value(), "超时出队应返回 nullopt");
    TEST_ASSERT(duration.count() >= 90, "应等待至少 90ms");
    TEST_ASSERT(duration.count() < 200, "应不超过 200ms");
    
    return true;
}

bool test_ring_buffer_timeout() {
    ThreadSafeRingBuffer<int> rb(5);
    
    // 测试空缓冲区超时
    auto start = std::chrono::steady_clock::now();
    auto val = rb.pop_for(std::chrono::milliseconds(50));
    auto end = std::chrono::steady_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    TEST_ASSERT(!val.has_value(), "超时出队应返回 nullopt");
    TEST_ASSERT(duration.count() >= 40, "应等待至少 40ms");
    TEST_ASSERT(duration.count() < 150, "应不超过 150ms");
    
    return true;
}

// ============================================================================
// 字符串类型测试
// ============================================================================

bool test_string_queue() {
    ThreadSafeQueue<std::string> queue;
    
    queue.push("Hello");
    queue.push("World");
    queue.push("!");
    
    TEST_ASSERT(queue.size() == 3, "队列大小应为 3");
    
    auto s1 = queue.try_pop();
    TEST_ASSERT(s1.has_value() && s1.value() == "Hello", "应为 Hello");
    
    auto s2 = queue.try_pop();
    TEST_ASSERT(s2.has_value() && s2.value() == "World", "应为 World");
    
    auto s3 = queue.try_pop();
    TEST_ASSERT(s3.has_value() && s3.value() == "!", "应为 !");
    
    return true;
}

bool test_string_priority_queue() {
    ThreadSafePriorityQueue<std::string, std::greater<std::string>> pq;
    
    // 小根堆（字母序）
    pq.push("banana");
    pq.push("apple");
    pq.push("cherry");
    
    auto s1 = pq.try_pop();
    TEST_ASSERT(s1.has_value() && s1.value() == "apple", "最小应为 apple");
    
    auto s2 = pq.try_pop();
    TEST_ASSERT(s2.has_value() && s2.value() == "banana", "第二小应为 banana");
    
    auto s3 = pq.try_pop();
    TEST_ASSERT(s3.has_value() && s3.value() == "cherry", "第三小应为 cherry");
    
    return true;
}

// ============================================================================
// 移动语义测试
// ============================================================================

class MovableObject {
public:
    int value;
    bool moved = false;
    
    MovableObject(int v) : value(v) {}
    MovableObject(MovableObject&& other) noexcept : value(other.value), moved(false) {
        other.moved = true;
    }
    MovableObject& operator=(MovableObject&& other) noexcept {
        value = other.value;
        other.moved = true;
        return *this;
    }
    MovableObject(const MovableObject&) = delete;
    MovableObject& operator=(const MovableObject&) = delete;
};

bool test_move_semantics() {
    ThreadSafeQueue<MovableObject> queue;
    
    MovableObject obj(42);
    queue.push(std::move(obj));
    TEST_ASSERT(obj.moved, "对象应被移动");
    
    auto val = queue.try_pop();
    TEST_ASSERT(val.has_value() && val->value == 42, "值应为 42");
    
    return true;
}

// ============================================================================
// 运行所有测试
// ============================================================================

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "线程安全队列测试" << std::endl;
    std::cout << "========================================" << std::endl;
    
    int passed = 0;
    int failed = 0;
    
    auto run_test = [&](const char* name, bool (*test_func)()) {
        std::cout << "测试: " << name << "... ";
        try {
            if (test_func()) {
                std::cout << "通过" << std::endl;
                passed++;
            } else {
                std::cout << "失败" << std::endl;
                failed++;
            }
        } catch (const std::exception& e) {
            std::cout << "异常: " << e.what() << std::endl;
            failed++;
        }
    };
    
    // ThreadSafeQueue 测试
    std::cout << "\n--- ThreadSafeQueue 基础测试 ---" << std::endl;
    run_test("基础操作", test_basic_queue_operations);
    run_test("有界队列", test_bounded_queue);
    run_test("清空队列", test_queue_clear);
    run_test("队列关闭", test_queue_shutdown);
    run_test("批量操作", test_batch_operations);
    
    // ThreadSafePriorityQueue 测试
    std::cout << "\n--- ThreadSafePriorityQueue 测试 ---" << std::endl;
    run_test("优先级队列基础", test_priority_queue_basic);
    run_test("优先级队列查看", test_priority_queue_peek);
    
    // ThreadSafeDeque 测试
    std::cout << "\n--- ThreadSafeDeque 测试 ---" << std::endl;
    run_test("双端队列基础", test_deque_basic);
    
    // ThreadSafeRingBuffer 测试
    std::cout << "\n--- ThreadSafeRingBuffer 测试 ---" << std::endl;
    run_test("环形缓冲区基础", test_ring_buffer_basic);
    run_test("环形缓冲区环绕", test_ring_buffer_wrap_around);
    
    // 多线程测试
    std::cout << "\n--- 多线程测试 ---" << std::endl;
    run_test("多线程队列", test_multithreaded_queue);
    run_test("多线程环形缓冲区", test_multithreaded_ring_buffer);
    
    // 超时测试
    std::cout << "\n--- 超时测试 ---" << std::endl;
    run_test("队列超时", test_queue_timeout);
    run_test("环形缓冲区超时", test_ring_buffer_timeout);
    
    // 类型测试
    std::cout << "\n--- 类型测试 ---" << std::endl;
    run_test("字符串队列", test_string_queue);
    run_test("字符串优先级队列", test_string_priority_queue);
    run_test("移动语义", test_move_semantics);
    
    // 结果
    std::cout << "\n========================================" << std::endl;
    std::cout << "测试结果: " << passed << " 通过, " << failed << " 失败" << std::endl;
    std::cout << "========================================" << std::endl;
    
    return failed > 0 ? 1 : 0;
}