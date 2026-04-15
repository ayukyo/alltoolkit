/**
 * @file quick_test.cpp
 * @brief 快速测试文件（不含长时间运行的多线程测试）
 */

#include "thread_safe_queue.hpp"
#include <cassert>
#include <iostream>

using namespace alltoolkit;

int main() {
    std::cout << "=== 线程安全队列快速测试 ===" << std::endl;
    
    // Test 1: ThreadSafeQueue 基础操作
    {
        ThreadSafeQueue<int> q;
        q.push(1);
        q.push(2);
        q.push(3);
        assert(q.size() == 3);
        auto v = q.try_pop();
        assert(v && *v == 1);
        v = q.try_pop();
        assert(v && *v == 2);
        v = q.try_pop();
        assert(v && *v == 3);
        assert(q.empty());
        std::cout << "[PASS] ThreadSafeQueue 基础操作" << std::endl;
    }
    
    // Test 2: 有界队列
    {
        ThreadSafeQueue<int> q(2);
        assert(q.try_push(1));
        assert(q.try_push(2));
        assert(!q.try_push(3)); // 应失败
        assert(q.full());
        q.try_pop();
        assert(q.try_push(3)); // 现在应成功
        std::cout << "[PASS] 有界队列" << std::endl;
    }
    
    // Test 3: ThreadSafePriorityQueue
    {
        ThreadSafePriorityQueue<int> pq;
        pq.push(5);
        pq.push(1);
        pq.push(3);
        auto v = pq.try_pop();
        assert(v && *v == 5); // 大根堆
        v = pq.try_pop();
        assert(v && *v == 3);
        v = pq.try_pop();
        assert(v && *v == 1);
        std::cout << "[PASS] ThreadSafePriorityQueue" << std::endl;
    }
    
    // Test 4: ThreadSafeDeque
    {
        ThreadSafeDeque<int> dq;
        dq.push_front(1);
        dq.push_back(2);
        auto f = dq.peek_front();
        auto b = dq.peek_back();
        assert(f && *f == 1);
        assert(b && *b == 2);
        f = dq.try_pop_front();
        assert(f && *f == 1);
        b = dq.try_pop_back();
        assert(b && *b == 2);
        std::cout << "[PASS] ThreadSafeDeque" << std::endl;
    }
    
    // Test 5: ThreadSafeRingBuffer
    {
        ThreadSafeRingBuffer<int> rb(3);
        assert(rb.try_push(1));
        assert(rb.try_push(2));
        assert(rb.try_push(3));
        assert(!rb.try_push(4)); // 满
        assert(rb.full());
        auto v = rb.try_pop();
        assert(v && *v == 1);
        assert(rb.try_push(4)); // 环绕写入
        std::cout << "[PASS] ThreadSafeRingBuffer" << std::endl;
    }
    
    // Test 6: 批量操作
    {
        ThreadSafeQueue<int> q;
        std::vector<int> items = {1, 2, 3, 4, 5};
        auto count = q.push_batch(items);
        assert(count == 5);
        auto batch = q.pop_batch(3);
        assert(batch.size() == 3);
        assert(batch[0] == 1);
        std::cout << "[PASS] 批量操作" << std::endl;
    }
    
    // Test 7: 关闭/重启
    {
        ThreadSafeQueue<int> q;
        q.shutdown();
        assert(q.is_shutdown());
        assert(!q.push(1)); // 关闭后入队失败
        q.restart();
        assert(q.push(2)); // 重启后成功
        std::cout << "[PASS] 关闭/重启" << std::endl;
    }
    
    // Test 8: 字符串类型
    {
        ThreadSafeQueue<std::string> q;
        q.push("Hello");
        q.push("World");
        auto s = q.try_pop();
        assert(s && *s == "Hello");
        std::cout << "[PASS] 字符串类型" << std::endl;
    }
    
    std::cout << "=== 所有测试通过 ===" << std::endl;
    return 0;
}