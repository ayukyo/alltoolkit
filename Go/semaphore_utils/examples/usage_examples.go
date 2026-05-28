// Package main 演示 semaphore_utils 的使用
package main

import (
	"context"
	"fmt"
	"sync"
	"sync/atomic"
	"time"

	semaphore "github.com/ayukyo/alltoolkit/Go/semaphore_utils"
)

func main() {
	fmt.Println("=== 信号量工具示例 ===")
	fmt.Println()

	// 示例1: 基础信号量
	basicSemaphoreExample()

	// 示例2: 并发控制
	concurrencyControlExample()

	// 示例3: 优先级信号量
	prioritySemaphoreExample()

	// 示例4: 读写信号量
	rwSemaphoreExample()

	// 示例5: 信号量池
	semaphorePoolExample()

	// 示例6: 资源池限制
	resourcePoolExample()

	// 示例7: API限流
	apiRateLimitExample()
}

// 示例1: 基础信号量使用
func basicSemaphoreExample() {
	fmt.Println("【示例1】基础信号量")
	fmt.Println("-------------------")

	// 创建容量为5的信号量
	s, err := semaphore.NewSemaphore(5)
	if err != nil {
		fmt.Printf("创建信号量失败: %v\n", err)
		return
	}

	fmt.Printf("信号量容量: %d, 可用: %d\n", s.Capacity(), s.Available())

	// 尝试获取
	if s.TryAcquire(3) {
		fmt.Println("✓ 成功获取 3 个资源")
		fmt.Printf("剩余可用: %d\n", s.Available())
	}

	// 获取失败
	if !s.TryAcquire(3) {
		fmt.Println("✗ 无法获取 3 个资源（仅剩 2 个）")
	}

	// 释放资源
	s.Release(2)
	fmt.Printf("释放 2 个后，可用: %d\n", s.Available())

	// 带超时获取
	if s.TryAcquireWithTimeout(1, 50*time.Millisecond) {
		fmt.Println("✓ 超时获取成功")
		s.Release(1)
	}

	s.Close()
	fmt.Printf("信号量已关闭: %v\n\n", s.IsClosed())
}

// 示例2: 并发控制
func concurrencyControlExample() {
	fmt.Println("【示例2】并发控制")
	fmt.Println("-------------------")

	s, _ := semaphore.NewSemaphore(3) // 最多3个并发

	var wg sync.WaitGroup
	var activeCount int32
	var maxActive int32

	for i := 1; i <= 10; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()

			// 获取信号量
			ctx := context.Background()
			if err := s.Acquire(ctx, 1); err != nil {
				fmt.Printf("任务 %d 获取失败: %v\n", id, err)
				return
			}
			defer s.Release(1)

			// 统计并发数
			current := atomic.AddInt32(&activeCount, 1)
			if current > maxActive {
				atomic.StoreInt32(&maxActive, current)
			}

			fmt.Printf("任务 %d 开始执行 (并发: %d)\n", id, current)
			time.Sleep(50 * time.Millisecond)

			atomic.AddInt32(&activeCount, -1)
			fmt.Printf("任务 %d 完成\n", id)
		}(i)
	}

	wg.Wait()
	fmt.Printf("最大并发数: %d (限制: 3)\n\n", maxActive)
}

// 示例3: 优先级信号量
func prioritySemaphoreExample() {
	fmt.Println("【示例3】优先级信号量")
	fmt.Println("-------------------")

	ps, _ := semaphore.NewPrioritySemaphore(1)

	// 先占用资源
	ctx := context.Background()
	ps.AcquireWithPriority(ctx, 1, 10)

	var wg sync.WaitGroup
	var order []int
	var mu sync.Mutex

	// 低优先级任务先排队
	wg.Add(1)
	go func() {
		defer wg.Done()
		ps.AcquireWithPriority(ctx, 1, 10) // 优先级 10 (低)
		mu.Lock()
		order = append(order, 10)
		mu.Unlock()
		time.Sleep(20 * time.Millisecond)
		ps.Release(1)
	}()

	// 高优先级任务后排队
	wg.Add(1)
	go func() {
		defer wg.Done()
		time.Sleep(10 * time.Millisecond) // 确保低优先级先排队
		ps.AcquireWithPriority(ctx, 1, 1) // 优先级 1 (高)
		mu.Lock()
		order = append(order, 1)
		mu.Unlock()
		time.Sleep(20 * time.Millisecond)
		ps.Release(1)
	}()

	time.Sleep(20 * time.Millisecond) // 等待排队
	ps.Release(1)                     // 释放初始占用

	wg.Wait()

	fmt.Printf("获取顺序: %v (预期: 高优先级先获取)\n\n", order)
}

// 示例4: 读写信号量
func rwSemaphoreExample() {
	fmt.Println("【示例4】读写信号量")
	fmt.Println("-------------------")

	rw, _ := semaphore.NewRWSemaphore(1)

	// 多个读操作可以并发
	var wg sync.WaitGroup
	for i := 1; i <= 3; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			ctx := context.Background()
			rw.AcquireRead(ctx)
			defer rw.ReleaseRead()

			fmt.Printf("读取者 %d 正在读取...\n", id)
			time.Sleep(50 * time.Millisecond)
			fmt.Printf("读取者 %d 读取完成\n", id)
		}(i)
	}

	wg.Wait()
	fmt.Println()

	// 写操作独占
	fmt.Println("写入者正在写入...")
	ctx := context.Background()
	rw.AcquireWrite(ctx)
	fmt.Println("写入者获得写锁")
	time.Sleep(50 * time.Millisecond)
	rw.ReleaseWrite()
	fmt.Println("写入者完成\n")
}

// 示例5: 信号量池
func semaphorePoolExample() {
	fmt.Println("【示例5】信号量池")
	fmt.Println("-------------------")

	pool := semaphore.NewSemaphorePool()

	// 为不同资源创建信号量
	dbSem, _ := pool.GetOrCreate("database", 10)
	apiSem, _ := pool.GetOrCreate("api", 5)

	fmt.Printf("信号量池管理: %v\n", pool.Names())

	// 使用数据库信号量
	if dbSem.TryAcquire(1) {
		fmt.Println("✓ 获取数据库连接")
		dbSem.Release(1)
	}

	// 使用 API 信号量
	if apiSem.TryAcquire(1) {
		fmt.Println("✓ 获取 API 资源")
		apiSem.Release(1)
	}

	// 移除某个信号量
	pool.Remove("database")
	fmt.Printf("移除后: %v\n\n", pool.Names())

	pool.CloseAll()
}

// 示例6: 资源池限制
func resourcePoolExample() {
	fmt.Println("【示例6】资源池限制")
	fmt.Println("-------------------")

	// 模拟数据库连接池
	connectionPool, _ := semaphore.NewSemaphore(5) // 最多5个连接

	var wg sync.WaitGroup

	for i := 1; i <= 8; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()

			// 获取连接
			ctx := context.Background()
			if err := connectionPool.Acquire(ctx, 1); err != nil {
				fmt.Printf("请求 %d 获取连接失败: %v\n", id, err)
				return
			}
			defer connectionPool.Release(1)

			fmt.Printf("请求 %d 获得连接，正在处理...\n", id)
			time.Sleep(100 * time.Millisecond)
			fmt.Printf("请求 %d 处理完成，释放连接\n", id)
		}(i)
	}

	wg.Wait()
	fmt.Printf("连接池状态 - 可用: %d/%d\n\n",
		connectionPool.Available(), connectionPool.Capacity())
}

// 示例7: API限流
func apiRateLimitExample() {
	fmt.Println("【示例7】API限流")
	fmt.Println("-------------------")

	// 创建限流器：最大10个令牌，每秒补充5个
	rl, _ := semaphore.NewRateLimiter(10, 5)

	var wg sync.WaitGroup
	var successCount int32
	var blockedCount int32

	for i := 1; i <= 20; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()

			if rl.TryAcquire(1) {
				atomic.AddInt32(&successCount, 1)
				fmt.Printf("请求 %d 发送成功\n", id)
				time.Sleep(100 * time.Millisecond)
			} else {
				atomic.AddInt32(&blockedCount, 1)
				fmt.Printf("请求 %d 被限流\n", id)
			}
		}(i)
	}

	wg.Wait()

	fmt.Printf("\n统计:\n")
	fmt.Printf("- 总请求: 20\n")
	fmt.Printf("- 成功: %d\n", successCount)
	fmt.Printf("- 限流: %d\n", blockedCount)
	fmt.Printf("- 当前可用: %d\n\n", rl.Available())
}