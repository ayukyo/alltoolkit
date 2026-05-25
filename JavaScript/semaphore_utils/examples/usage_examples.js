/**
 * Semaphore Utils 使用示例
 * 
 * 展示如何在 JavaScript 异步环境中使用信号量工具进行并发控制
 */

const {
  Semaphore,
  Mutex,
  ReadWriteLock,
  CountDownLatch,
  CyclicBarrier,
  SemaphorePool
} = require('../mod.js');

// ==========================================
// 示例 1: Semaphore - 限制 API 并发请求数
// ==========================================

async function example1_semaphoreApiLimiter() {
  console.log('\n📌 示例 1: Semaphore - 限制 API 并发请求数\n');
  
  const apiLimiter = new Semaphore(3); // 最多同时3个请求
  const urls = Array.from({ length: 10 }, (_, i) => `https://api.example.com/data/${i + 1}`);
  
  const startTime = Date.now();
  
  const fetchWithLimit = async (url) => {
    await apiLimiter.acquire();
    console.log(`[开始] ${url} (并发: ${3 - apiLimiter.available}/${3})`);
    
    // 模拟 API 请求
    await new Promise(r => setTimeout(r, 500));
    
    console.log(`[完成] ${url}`);
    apiLimiter.release();
    return `Response from ${url}`;
  };
  
  const results = await Promise.all(urls.map(fetchWithLimit));
  
  const duration = Date.now() - startTime;
  console.log(`\n✅ 完成 ${results.length} 个请求，耗时 ${duration}ms`);
  console.log(`💡 说明: 10个请求，每次最多3个并发，约需 ${Math.ceil(10/3) * 500}ms`);
}

// ==========================================
// 示例 2: Mutex - 保护共享资源
// ==========================================

async function example2_mutexProtectSharedResource() {
  console.log('\n📌 示例 2: Mutex - 保护共享资源\n');
  
  const mutex = new Mutex();
  let bankBalance = 1000;
  
  const deposit = async (amount, name) => {
    await mutex.run(async () => {
      console.log(`[${name}] 准备存款 ${amount}，当前余额: ${bankBalance}`);
      const temp = bankBalance;
      await new Promise(r => setTimeout(r, 50)); // 模拟处理延迟
      bankBalance = temp + amount;
      console.log(`[${name}] 存款完成，余额: ${bankBalance}`);
    });
  };
  
  const withdraw = async (amount, name) => {
    await mutex.run(async () => {
      console.log(`[${name}] 准备取款 ${amount}，当前余额: ${bankBalance}`);
      if (bankBalance >= amount) {
        const temp = bankBalance;
        await new Promise(r => setTimeout(r, 50));
        bankBalance = temp - amount;
        console.log(`[${name}] 取款完成，余额: ${bankBalance}`);
      } else {
        console.log(`[${name}] 余额不足，取款失败`);
      }
    });
  };
  
  // 并发操作
  await Promise.all([
    deposit(200, '储户A'),
    withdraw(300, '储户B'),
    deposit(100, '储户C'),
    withdraw(150, '储户D'),
  ]);
  
  console.log(`\n✅ 最终余额: ${bankBalance}`);
  console.log('💡 说明: Mutex 确保所有操作串行执行，避免竞态条件');
}

// ==========================================
// 示例 3: ReadWriteLock - 缓存系统
// ==========================================

async function example3_readWriteLockCache() {
  console.log('\n📌 示例 3: ReadWriteLock - 缓存系统\n');
  
  const cache = new Map();
  const rwLock = new ReadWriteLock();
  
  const readCache = async (key) => {
    return await rwLock.read(async () => {
      console.log(`[读取] key="${key}"`);
      await new Promise(r => setTimeout(r, 50));
      return cache.get(key);
    });
  };
  
  const writeCache = async (key, value) => {
    await rwLock.write(async () => {
      console.log(`[写入] key="${key}", value="${value}"`);
      await new Promise(r => setTimeout(r, 100));
      cache.set(key, value);
    });
  };
  
  // 初始化一些数据
  await writeCache('user:1', 'Alice');
  await writeCache('user:2', 'Bob');
  
  console.log('\n--- 并发读取 ---');
  await Promise.all([
    readCache('user:1'),
    readCache('user:2'),
    readCache('user:1'),
    readCache('user:2'),
  ]);
  console.log('✅ 多个读取操作可以同时进行\n');
  
  console.log('--- 写入操作 ---');
  await Promise.all([
    writeCache('user:3', 'Charlie'),
    readCache('user:1'),
  ]);
  console.log('✅ 写入时，读取需要等待\n');
  
  console.log('💡 说明: ReadWriteLock 允许多读单写，提高读多写少场景的性能');
}

// ==========================================
// 示例 4: CountDownLatch - 等待多个服务启动
// ==========================================

async function example4_countDownLatchServiceStartup() {
  console.log('\n📌 示例 4: CountDownLatch - 等待多个服务启动\n');
  
  const latch = new CountDownLatch(4);
  const services = ['数据库', '缓存', '消息队列', 'API服务器'];
  
  const startService = async (name) => {
    console.log(`[启动中] ${name}...`);
    await new Promise(r => setTimeout(r, Math.random() * 500 + 200));
    console.log(`[已启动] ${name} ✓`);
    latch.countDown();
  };
  
  // 并行启动所有服务
  services.forEach(s => startService(s));
  
  console.log('⏳ 等待所有服务启动完成...\n');
  await latch.wait();
  
  console.log('\n✅ 所有服务启动完成！');
  console.log('💡 说明: CountDownLatch 用于等待一组事件完成');
}

// ==========================================
// 示例 5: CyclicBarrier - 并行任务同步点
// ==========================================

async function example5_cyclicBarrierParallelTasks() {
  console.log('\n📌 示例 5: CyclicBarrier - 并行任务同步点\n');
  
  const NUM_WORKERS = 3;
  const barrier = new CyclicBarrier(NUM_WORKERS);
  
  const worker = async (id) => {
    // 第一阶段
    console.log(`[Worker ${id}] 执行第一阶段任务...`);
    await new Promise(r => setTimeout(r, Math.random() * 300 + 100));
    console.log(`[Worker ${id}] 第一阶段完成，等待其他 worker...`);
    
    await barrier.await();
    console.log(`[Worker ${id}] 所有 worker 第一阶段完成，开始第二阶段`);
    
    // 第二阶段
    await new Promise(r => setTimeout(r, Math.random() * 300 + 100));
    console.log(`[Worker ${id}] 第二阶段完成，等待其他 worker...`);
    
    await barrier.await();
    console.log(`[Worker ${id}] 所有 worker 第二阶段完成！`);
  };
  
  await Promise.all(Array.from({ length: NUM_WORKERS }, (_, i) => worker(i + 1)));
  
  console.log('\n✅ 所有任务完成！');
  console.log('💡 说明: CyclicBarrier 让多个任务在屏障点同步，可重复使用');
}

// ==========================================
// 示例 6: SemaphorePool - 动态资源池
// ==========================================

async function example6_semaphorePoolDynamicResources() {
  console.log('\n📌 示例 6: SemaphorePool - 动态资源池\n');
  
  const pool = new SemaphorePool(2);
  console.log('初始池大小: 2');
  
  const task = async (id) => {
    await pool.acquire();
    console.log(`[任务 ${id}] 获取资源 (剩余: ${pool.getStatus().available})`);
    await new Promise(r => setTimeout(r, 200));
    pool.release();
    console.log(`[任务 ${id}] 释放资源`);
  };
  
  // 先执行2个任务（刚好用完初始资源）
  console.log('--- 执行前两个任务 ---');
  await Promise.all([task(1), task(2)]);
  
  // 扩容后再执行更多任务
  console.log('\n--- 扩容到 4 个资源 ---');
  pool.expand(2);
  console.log(`扩容后池大小: ${pool.getStatus().totalPermits}`);
  
  console.log('\n--- 并发执行 4 个任务 ---');
  await Promise.all([task(3), task(4), task(5), task(6)]);
  
  console.log('\n💡 说明: SemaphorePool 支持运行时动态扩容');
}

// ==========================================
// 示例 7: 超时控制
// ==========================================

async function example7_timeoutHandling() {
  console.log('\n📌 示例 7: 超时控制\n');
  
  const semaphore = new Semaphore(1);
  
  // 先获取许可
  await semaphore.acquire();
  console.log('许可已被获取');
  
  console.log('尝试获取许可（超时 1 秒）...');
  try {
    await semaphore.acquire(1000);
    console.log('获取成功');
  } catch (error) {
    console.log(`❌ 超时错误: ${error.message}`);
  }
  
  semaphore.release();
  console.log('许可已释放');
  
  console.log('\n💡 说明: 所有同步原语都支持超时参数');
}

// ==========================================
// 示例 8: 实际应用 - 批量下载器
// ==========================================

async function example8_batchDownloader() {
  console.log('\n📌 示例 8: 实际应用 - 批量下载器\n');
  
  const MAX_CONCURRENT = 2;
  const semaphore = new Semaphore(MAX_CONCURRENT);
  
  const downloadFile = async (filename) => {
    return semaphore.run(async () => {
      console.log(`📥 开始下载: ${filename}`);
      await new Promise(r => setTimeout(r, 300 + Math.random() * 200));
      console.log(`✅ 下载完成: ${filename}`);
      return { filename, size: Math.floor(Math.random() * 1000) + 100 };
    });
  };
  
  const files = [
    'document.pdf',
    'image.png',
    'video.mp4',
    'audio.mp3',
    'data.json'
  ];
  
  console.log(`开始下载 ${files.length} 个文件（最大并发: ${MAX_CONCURRENT}）\n`);
  
  const results = await Promise.all(files.map(downloadFile));
  
  console.log('\n📄 下载结果:');
  results.forEach(r => {
    console.log(`  ${r.filename}: ${r.size}KB`);
  });
}

// ==========================================
// 运行所有示例
// ==========================================

async function main() {
  console.log('╔══════════════════════════════════════════╗');
  console.log('║    Semaphore Utils 使用示例集            ║');
  console.log('║    JavaScript 并发控制工具               ║');
  console.log('╚══════════════════════════════════════════╝');
  
  await example1_semaphoreApiLimiter();
  await example2_mutexProtectSharedResource();
  await example3_readWriteLockCache();
  await example4_countDownLatchServiceStartup();
  await example5_cyclicBarrierParallelTasks();
  await example6_semaphorePoolDynamicResources();
  await example7_timeoutHandling();
  await example8_batchDownloader();
  
  console.log('\n' + '═'.repeat(50));
  console.log('所有示例执行完成！\n');
}

main().catch(console.error);