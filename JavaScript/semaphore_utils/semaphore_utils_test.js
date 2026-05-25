/**
 * Semaphore Utils 测试套件
 */

const {
  Semaphore,
  Mutex,
  ReadWriteLock,
  CountDownLatch,
  CyclicBarrier,
  SemaphorePool
} = require('./mod.js');

// 简单的测试框架
let passCount = 0;
let failCount = 0;
const testResults = [];

function assert(condition, message) {
  if (!condition) {
    throw new Error(message || 'Assertion failed');
  }
}

async function test(name, fn) {
  try {
    await fn();
    passCount++;
    testResults.push({ name, status: 'PASS' });
    console.log(`✅ ${name}`);
  } catch (error) {
    failCount++;
    testResults.push({ name, status: 'FAIL', error: error.message });
    console.log(`❌ ${name}: ${error.message}`);
  }
}

// ============ Semaphore 测试 ============

async function testSemaphoreBasic() {
  await test('Semaphore - 基本获取和释放', async () => {
    const sem = new Semaphore(3);
    assert(sem.available === 3, 'Initial permits should be 3');
    assert(sem.total === 3, 'Total permits should be 3');
    
    await sem.acquire();
    assert(sem.available === 2, 'After acquire, available should be 2');
    
    sem.release();
    assert(sem.available === 3, 'After release, available should be 3');
  });

  await test('Semaphore - tryAcquire', async () => {
    const sem = new Semaphore(2);
    assert(sem.tryAcquire() === true, 'First tryAcquire should succeed');
    assert(sem.tryAcquire() === true, 'Second tryAcquire should succeed');
    assert(sem.tryAcquire() === false, 'Third tryAcquire should fail');
    
    sem.release();
    assert(sem.tryAcquire() === true, 'After release, tryAcquire should succeed');
  });

  await test('Semaphore - 并发控制', async () => {
    const sem = new Semaphore(2);
    const results = [];
    
    const task = async (id) => {
      await sem.acquire();
      results.push(`start-${id}`);
      await new Promise(r => setTimeout(r, 50));
      results.push(`end-${id}`);
      sem.release();
    };
    
    await Promise.all([task(1), task(2), task(3), task(4)]);
    
    // 检查同时运行的任务不超过2个
    let maxConcurrent = 0;
    let current = 0;
    for (const r of results) {
      if (r.startsWith('start-')) current++;
      if (r.startsWith('end-')) current--;
      maxConcurrent = Math.max(maxConcurrent, current);
    }
    assert(maxConcurrent <= 2, 'Max concurrent should be <= 2');
  });

  await test('Semaphore - run 方法', async () => {
    const sem = new Semaphore(1);
    let executed = false;
    
    await sem.run(async () => {
      executed = true;
      return 42;
    });
    
    assert(executed, 'Function should have been executed');
    assert(sem.available === 1, 'Permit should be released after run');
  });

  await test('Semaphore - 超时', async () => {
    const sem = new Semaphore(1);
    await sem.acquire();
    
    try {
      await sem.acquire(100);
      assert(false, 'Should have thrown timeout error');
    } catch (error) {
      assert(error.message.includes('timeout'), 'Should throw timeout error');
    }
    
    sem.release();
  });
}

// ============ Mutex 测试 ============

async function testMutexBasic() {
  await test('Mutex - 基本锁定和解锁', async () => {
    const mutex = new Mutex();
    assert(mutex.isLocked === false, 'Initial state should be unlocked');
    
    await mutex.acquire();
    assert(mutex.isLocked === true, 'Should be locked after acquire');
    
    mutex.release();
    assert(mutex.isLocked === false, 'Should be unlocked after release');
  });

  await test('Mutex - tryAcquire', async () => {
    const mutex = new Mutex();
    assert(mutex.tryAcquire() === true, 'First tryAcquire should succeed');
    assert(mutex.isLocked === true, 'Should be locked');
    assert(mutex.tryAcquire() === false, 'Second tryAcquire should fail');
    
    mutex.release();
    assert(mutex.tryAcquire() === true, 'After release, tryAcquire should succeed');
    mutex.release();
  });

  await test('Mutex - 互斥访问', async () => {
    const mutex = new Mutex();
    let counter = 0;
    
    const task = async () => {
      await mutex.acquire();
      const temp = counter;
      await new Promise(r => setTimeout(r, 10));
      counter = temp + 1;
      mutex.release();
    };
    
    await Promise.all([task(), task(), task(), task(), task()]);
    assert(counter === 5, 'Counter should be 5 without race conditions');
  });

  await test('Mutex - run 方法', async () => {
    const mutex = new Mutex();
    const result = await mutex.run(async () => {
      assert(mutex.isLocked === true, 'Should be locked inside run');
      return 'success';
    });
    
    assert(result === 'success', 'Should return function result');
    assert(mutex.isLocked === false, 'Should be unlocked after run');
  });
}

// ============ ReadWriteLock 测试 ============

async function testReadWriteLock() {
  await test('ReadWriteLock - 多个读者可以同时读', async () => {
    const rwLock = new ReadWriteLock();
    let concurrentReaders = 0;
    let maxConcurrentReaders = 0;
    
    const reader = async () => {
      await rwLock.acquireRead();
      concurrentReaders++;
      maxConcurrentReaders = Math.max(maxConcurrentReaders, concurrentReaders);
      await new Promise(r => setTimeout(r, 50));
      concurrentReaders--;
      rwLock.releaseRead();
    };
    
    await Promise.all([reader(), reader(), reader()]);
    assert(maxConcurrentReaders === 3, 'All readers should be concurrent');
  });

  await test('ReadWriteLock - 写操作独占', async () => {
    const rwLock = new ReadWriteLock();
    let value = 0;
    
    const writer = async () => {
      await rwLock.acquireWrite();
      value++;
      await new Promise(r => setTimeout(r, 30));
      value++;
      rwLock.releaseWrite();
    };
    
    await Promise.all([writer(), writer(), writer()]);
    assert(value === 6, 'All writes should complete sequentially');
  });

  await test('ReadWriteLock - 读写互斥', async () => {
    const rwLock = new ReadWriteLock();
    const order = [];
    
    const reader = async () => {
      await rwLock.acquireRead();
      order.push('read-start');
      await new Promise(r => setTimeout(r, 30));
      order.push('read-end');
      rwLock.releaseRead();
    };
    
    const writer = async () => {
      await rwLock.acquireWrite();
      order.push('write-start');
      await new Promise(r => setTimeout(r, 30));
      order.push('write-end');
      rwLock.releaseWrite();
    };
    
    // 先获取读锁，然后尝试写
    const readerPromise = reader();
    await new Promise(r => setTimeout(r, 10)); // 确保读锁先获取
    
    await Promise.all([readerPromise, writer()]);
    
    // 检查读写没有重叠
    const readStart = order.indexOf('read-start');
    const readEnd = order.indexOf('read-end');
    const writeStart = order.indexOf('write-start');
    const writeEnd = order.indexOf('write-end');
    
    assert(writeStart > readEnd || readStart > writeEnd, 'Read and write should not overlap');
  });

  await test('ReadWriteLock - read 和 write 方法', async () => {
    const rwLock = new ReadWriteLock();
    const data = { value: 0 };
    
    await rwLock.read(async () => {
      assert(data.value === 0, 'Read should see initial value');
    });
    
    await rwLock.write(async () => {
      data.value = 42;
    });
    
    await rwLock.read(async () => {
      assert(data.value === 42, 'Read should see updated value');
    });
  });
}

// ============ CountDownLatch 测试 ============

async function testCountDownLatch() {
  await test('CountDownLatch - 等待多个任务完成', async () => {
    const latch = new CountDownLatch(3);
    assert(latch.count === 3, 'Initial count should be 3');
    
    let completed = false;
    const waitPromise = latch.wait().then(() => {
      completed = true;
    });
    
    assert(completed === false, 'Should not be completed initially');
    
    latch.countDown();
    assert(latch.count === 2, 'Count should be 2 after first countDown');
    
    latch.countDown();
    assert(latch.count === 1, 'Count should be 1 after second countDown');
    
    latch.countDown();
    assert(latch.count === 0, 'Count should be 0 after third countDown');
    
    await waitPromise;
    assert(completed === true, 'Should be completed after all countDown');
  });

  await test('CountDownLatch - 零计数立即返回', async () => {
    const latch = new CountDownLatch(0);
    assert(latch.count === 0, 'Initial count should be 0');
    
    let completed = false;
    await latch.wait();
    completed = true;
    
    assert(completed === true, 'Should complete immediately when count is 0');
  });

  await test('CountDownLatch - 超时', async () => {
    const latch = new CountDownLatch(5);
    
    try {
      await latch.wait(100);
      assert(false, 'Should have thrown timeout error');
    } catch (error) {
      assert(error.message.includes('timeout'), 'Should throw timeout error');
    }
  });
}

// ============ CyclicBarrier 测试 ============

async function testCyclicBarrier() {
  await test('CyclicBarrier - 等待所有参与者', async () => {
    const barrier = new CyclicBarrier(3);
    const arrivalOrder = [];
    
    const participant = async (id) => {
      await new Promise(r => setTimeout(r, id * 30));
      arrivalOrder.push(id);
      await barrier.await();
      return id;
    };
    
    await Promise.all([participant(1), participant(2), participant(3)]);
    assert(arrivalOrder.length === 3, 'All participants should have arrived');
    assert(barrier.waiting === 0, 'No one should be waiting');
  });

  await test('CyclicBarrier - 可重用', async () => {
    const barrier = new CyclicBarrier(2);
    
    // 第一轮
    let round = 0;
    const p1 = async () => {
      await barrier.await();
      round++;
      await barrier.await();
      round++;
    };
    
    const p2 = async () => {
      await barrier.await();
      await new Promise(r => setTimeout(r, 10));
      await barrier.await();
    };
    
    await Promise.all([p1(), p2()]);
    assert(round === 2, 'Should complete both rounds');
    assert(barrier.isBroken === false, 'Barrier should not be broken');
  });

  await test('CyclicBarrier - 重置', async () => {
    const barrier = new CyclicBarrier(3);
    
    barrier.reset();
    assert(barrier.isBroken === false, 'Should not be broken after reset');
    assert(barrier.waiting === 0, 'Should have no waiting participants');
  });
}

// ============ SemaphorePool 测试 ============

async function testSemaphorePool() {
  await test('SemaphorePool - 基本操作', async () => {
    const pool = new SemaphorePool(5);
    const status = pool.getStatus();
    
    assert(status.total === 5, 'Initial permits should be 5');
    assert(status.available === 5, 'Available should be 5');
  });

  await test('SemaphorePool - 动态扩容', async () => {
    const pool = new SemaphorePool(2);
    
    await pool.acquire();
    await pool.acquire();
    
    // 此时没有可用许可
    const beforeExpand = pool.getStatus();
    assert(beforeExpand.available === 0, 'No permits before expand');
    
    // 扩容
    pool.expand(2);
    const afterExpand = pool.getStatus();
    assert(afterExpand.totalPermits === 4, 'Total should be 4 after expand');
    assert(afterExpand.available === 2, 'Available should be 2 after expand');
    
    // 现在可以再获取
    await pool.acquire();
    pool.release();
  });
}

// ============ 运行所有测试 ============

async function runAllTests() {
  console.log('\n🧪 Semaphore Utils 测试套件\n');
  console.log('='.repeat(50));
  
  await testSemaphoreBasic();
  console.log('-'.repeat(50));
  
  await testMutexBasic();
  console.log('-'.repeat(50));
  
  await testReadWriteLock();
  console.log('-'.repeat(50));
  
  await testCountDownLatch();
  console.log('-'.repeat(50));
  
  await testCyclicBarrier();
  console.log('-'.repeat(50));
  
  await testSemaphorePool();
  console.log('='.repeat(50));
  
  console.log(`\n📊 测试结果: ${passCount} 通过, ${failCount} 失败\n`);
  
  if (failCount > 0) {
    console.log('失败的测试:');
    testResults
      .filter(r => r.status === 'FAIL')
      .forEach(r => console.log(`  - ${r.name}: ${r.error}`));
    process.exit(1);
  }
  
  return { passCount, failCount };
}

runAllTests();