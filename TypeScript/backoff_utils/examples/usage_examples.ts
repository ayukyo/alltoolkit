/**
 * Backoff Utils 使用示例
 * 
 * 展示各种退避策略的实际应用场景
 * 
 * @author AllToolkit Generator
 * @date 2026-05-03
 */

import {
  ExponentialBackoff,
  LinearBackoff,
  ConstantBackoff,
  FullJitterBackoff,
  EqualJitterBackoff,
  DecorrelatedJitterBackoff,
  FibonacciBackoff,
  PolynomialBackoff,
  RetryExecutor,
  withRetry,
  retryBatch,
  createStrategy,
  calculateBackoffSequence,
  backoffWait
} from '../mod';

// ==================== 基础用法 ====================

/**
 * 示例1: 基础指数退避
 */
function basicExponentialBackoff() {
  console.log('\n📌 示例1: 基础指数退避');
  console.log('─'.repeat(40));

  const backoff = new ExponentialBackoff({
    initialDelay: 100,    // 初始延迟 100ms
    maxDelay: 10000,       // 最大延迟 10s
    maxRetries: 5          // 最多重试 5 次
  });

  console.log('重试序列:');
  while (true) {
    const result = backoff.next();
    if (!result.shouldRetry) {
      console.log(`  ❌ 重试次数已用尽`);
      break;
    }
    console.log(`  第 ${result.attempt} 次: 延迟 ${result.delay}ms`);
  }
}

/**
 * 示例2: 带抖动的指数退避
 */
function exponentialBackoffWithJitter() {
  console.log('\n📌 示例2: 带抖动的指数退避');
  console.log('─'.repeat(40));

  const backoff = new ExponentialBackoff({
    initialDelay: 100,
    maxDelay: 10000,
    jitter: true,         // 启用抖动
    jitterFactor: 0.3      // 抖动因子 30%
  });

  console.log('带抖动的重试序列:');
  for (let i = 0; i < 5; i++) {
    const result = backoff.next();
    console.log(`  第 ${result.attempt} 次: 延迟 ${result.delay}ms`);
  }
}

// ==================== 不同退避策略对比 ====================

/**
 * 示例3: 比较不同退避策略
 */
function compareStrategies() {
  console.log('\n📌 示例3: 不同退避策略对比');
  console.log('─'.repeat(40));

  const strategies = {
    '指数退避': new ExponentialBackoff({ initialDelay: 100, maxDelay: 5000 }),
    '线性退避': new LinearBackoff({ initialDelay: 100, maxDelay: 5000, increment: 200 }),
    '恒定退避': new ConstantBackoff({ initialDelay: 500, maxDelay: 5000 }),
    '斐波那契退避': new FibonacciBackoff({ initialDelay: 100, maxDelay: 5000 }),
    '多项式退避(幂=2)': new PolynomialBackoff({ initialDelay: 100, maxDelay: 5000, power: 2 })
  };

  console.log('各策略前 5 次重试延迟对比:\n');
  
  // 打印表头
  const headers = Object.keys(strategies);
  console.log('次数 | ' + headers.map(h => h.padEnd(12)).join(' | '));
  console.log('─'.repeat(70));

  // 打印每次重试的延迟
  for (let i = 1; i <= 5; i++) {
    const delays = headers.map(name => {
      const strategy = strategies[name as keyof typeof strategies];
      // 重置并前进到第 i 次
      strategy.reset();
      for (let j = 1; j < i; j++) strategy.next();
      return strategy.next().delay;
    });
    console.log(`  ${i}  | ` + delays.map(d => String(d + 'ms').padEnd(12)).join(' | '));
  }
}

// ==================== 抖动策略对比 ====================

/**
 * 示例4: 不同抖动策略对比
 */
function compareJitterStrategies() {
  console.log('\n📌 示例4: 抖动策略对比');
  console.log('─'.repeat(40));

  const strategies = {
    '完全抖动': () => new FullJitterBackoff({ initialDelay: 100, maxDelay: 5000 }),
    '等抖动': () => new EqualJitterBackoff({ initialDelay: 100, maxDelay: 5000 }),
    '装饰抖动': () => new DecorrelatedJitterBackoff({ initialDelay: 100, maxDelay: 5000 })
  };

  console.log('各抖动策略第 3 次重试的延迟分布 (10 次采样):\n');
  
  for (const [name, createStrategy] of Object.entries(strategies)) {
    const delays: number[] = [];
    for (let i = 0; i < 10; i++) {
      const strategy = createStrategy();
      strategy.next();
      strategy.next();
      delays.push(strategy.next().delay);
    }
    console.log(`${name}:`);
    console.log(`  最小: ${Math.min(...delays)}ms`);
    console.log(`  最大: ${Math.max(...delays)}ms`);
    console.log(`  平均: ${Math.round(delays.reduce((a, b) => a + b) / delays.length)}ms`);
    console.log(`  值: ${delays.join(', ')}ms`);
    console.log();
  }
}

// ==================== 实际应用场景 ====================

/**
 * 示例5: API 请求重试
 */
async function apiRequestRetry() {
  console.log('\n📌 示例5: API 请求重试');
  console.log('─'.repeat(40));

  // 模拟一个不稳定的 API
  let callCount = 0;
  const unstableApi = async (): Promise<string> => {
    callCount++;
    console.log(`  📡 API 调用 #${callCount}`);
    
    // 前 3 次调用失败，第 4 次成功
    if (callCount < 4) {
      console.log(`  ❌ 请求失败 (模拟错误)`);
      throw new Error('Service Unavailable');
    }
    console.log(`  ✅ 请求成功`);
    return 'Success!';
  };

  // 创建重试执行器
  const strategy = new ExponentialBackoff({
    initialDelay: 100,
    maxDelay: 5000,
    maxRetries: 5
  });

  const executor = new RetryExecutor(strategy);

  console.log('开始调用 API...');
  const result = await executor.execute(unstableApi);
  
  console.log(`\n结果: ${result.success ? '成功' : '失败'}`);
  console.log(`重试次数: ${result.attempts}`);
  console.log(`总延迟: ${result.totalDelay}ms`);
  if (result.result) {
    console.log(`返回值: ${result.result}`);
  }
}

/**
 * 示例6: 数据库重连
 */
async function databaseReconnect() {
  console.log('\n📌 示例6: 数据库重连');
  console.log('─'.repeat(40));

  // 模拟数据库连接
  let connectionAttempts = 0;
  const connectToDatabase = async (): Promise<{ connected: boolean }> => {
    connectionAttempts++;
    console.log(`  🔌 连接尝试 #${connectionAttempts}`);
    
    // 模拟连接延迟
    await new Promise(r => setTimeout(r, 50));
    
    if (connectionAttempts < 3) {
      throw new Error('Connection timeout');
    }
    
    return { connected: true };
  };

  // 使用装饰抖动策略（更适合重连场景）
  const strategy = new DecorrelatedJitterBackoff({
    initialDelay: 500,    // 最小等待 500ms
    maxDelay: 30000,      // 最大等待 30s
    maxRetries: 10
  });

  const executor = new RetryExecutor(strategy, {
    shouldRetryOn: (err) => {
      // 只重试连接超时错误
      if (err.message.includes('timeout')) {
        console.log(`  ⚠️ ${err.message}，准备重试...`);
        return true;
      }
      return false;
    }
  });

  const result = await executor.execute(connectToDatabase);
  
  if (result.success) {
    console.log(`✅ 数据库连接成功！`);
  } else {
    console.log(`❌ 数据库连接失败: ${result.error?.message}`);
  }
}

/**
 * 示例7: 批量请求限流重试
 */
async function batchRequestsWithRetry() {
  console.log('\n📌 示例7: 批量请求限流重试');
  console.log('─'.repeat(40));

  const items = ['item1', 'item2', 'item3', 'item4', 'item5'];
  
  // 模拟处理单个项目的函数
  const processItem = async (item: string): Promise<string> => {
    console.log(`  处理 ${item}...`);
    
    // 随机失败
    if (Math.random() < 0.3) {
      throw new Error(`Failed to process ${item}`);
    }
    
    return `processed_${item}`;
  };

  const results = await retryBatch(
    items,
    processItem,
    {
      initialDelay: 100,
      maxDelay: 2000,
      maxRetries: 3
    }
  );

  console.log('\n结果:');
  results.forEach((r, i) => {
    if (r.success) {
      console.log(`  ✅ ${items[i]}: ${r.result}`);
    } else {
      console.log(`  ❌ ${items[i]}: ${r.error?.message}`);
    }
  });
}

/**
 * 示例8: 使用函数包装器
 */
async function functionWrapper() {
  console.log('\n📌 示例8: 使用函数包装器');
  console.log('─'.repeat(40));

  // 原始函数
  const fetchData = async (id: number): Promise<string> => {
    console.log(`  获取数据 ID=${id}`);
    if (Math.random() < 0.5) {
      throw new Error('Network error');
    }
    return `Data for ID=${id}`;
  };

  // 包装成带重试的函数
  const fetchWithRetry = withRetry(fetchData, {
    initialDelay: 100,
    maxDelay: 2000,
    maxRetries: 3
  });

  try {
    const result = await fetchWithRetry(42);
    console.log(`✅ 结果: ${result}`);
  } catch (err) {
    console.log(`❌ 失败: ${(err as Error).message}`);
  }
}

// ==================== 工具函数使用 ====================

/**
 * 示例9: 预览退避序列
 */
function previewBackoffSequence() {
  console.log('\n📌 示例9: 预览退避序列');
  console.log('─'.repeat(40));

  const sequence = calculateBackoffSequence(
    { initialDelay: 100, maxDelay: 30000, type: 'exponential' },
    10
  );

  console.log('指数退避序列 (前 10 次):');
  sequence.forEach((delay, i) => {
    console.log(`  第 ${i + 1} 次: ${delay}ms (${(delay / 1000).toFixed(2)}s)`);
  });
}

/**
 * 示例10: 工厂方法创建策略
 */
function factoryMethodExample() {
  console.log('\n📌 示例10: 工厂方法创建策略');
  console.log('─'.repeat(40));

  const strategyTypes = ['exponential', 'linear', 'constant', 'fullJitter', 'fibonacci'] as const;

  console.log('使用工厂方法创建不同策略:\n');
  
  for (const type of strategyTypes) {
    const strategy = createStrategy({
      initialDelay: 100,
      maxDelay: 5000,
      maxRetries: 5,
      type
    });

    const delays: number[] = [];
    for (let i = 0; i < 3; i++) {
      delays.push(strategy.next().delay);
    }

    console.log(`${type.padEnd(15)}: ${delays.map(d => d + 'ms').join(' → ')}`);
  }
}

// ==================== 主函数 ====================

async function main() {
  console.log('╔════════════════════════════════════════════╗');
  console.log('║      Backoff Utils 使用示例                 ║');
  console.log('║      TypeScript 版本                        ║');
  console.log('╚════════════════════════════════════════════╝');

  // 同步示例
  basicExponentialBackoff();
  exponentialBackoffWithJitter();
  compareStrategies();
  compareJitterStrategies();
  previewBackoffSequence();
  factoryMethodExample();

  // 异步示例
  await apiRequestRetry();
  await databaseReconnect();
  
  await batchRequestsWithRetry();
  await functionWrapper();

  console.log('\n✅ 所有示例运行完成！');
}

// 导出以供测试
export { main };

// 运行
main().catch(console.error);