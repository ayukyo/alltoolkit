import { getAccessToken, sendC2CImageMessage, sendProactiveC2CMessage } from '/home/admin/.openclaw/extensions/qqbot/src/api.js';
import * as fs from 'fs';
import * as path from 'path';

// 常量定义
const DEFAULT_OPENID = 'BA6E8E0EE4A26B93A2929F566321D644';
const DEFAULT_IMAGE_URL = 'https://images.pexels.com/photos/36492702/pexels-photo-36492702.jpeg?cs=srgb&dl=pexels-vika-glitter-392079-36492702.jpg&fm=jpg';
const DEFAULT_TEXT = '今日壁纸推荐 🌸\n\n【气质美女 · 户外写真】\n分辨率：3064x4608';

interface QQBotConfig {
  appId?: string;
  clientSecret?: string;
}

interface AppConfig {
  channels?: {
    qqbot?: QQBotConfig;
  };
}

/**
 * 加载配置文件
 */
function loadConfig(): AppConfig {
  const configPath = path.join(process.env.HOME || '/home/admin', 'clawd', 'config.json');
  const configData = fs.readFileSync(configPath, 'utf-8');
  return JSON.parse(configData) as AppConfig;
}

/**
 * 获取QQBot配置
 */
function getQQBotConfig(config: AppConfig): Required<QQBotConfig> {
  const qqbot = config.channels?.qqbot;

  if (!qqbot?.appId || !qqbot?.clientSecret) {
    throw new Error('QQBot not configured: missing appId or clientSecret');
  }

  return {
    appId: qqbot.appId,
    clientSecret: qqbot.clientSecret,
  };
}

/**
 * 解析命令行参数
 */
function parseArgs(): { openid: string; imageUrl: string; text: string } {
  return {
    openid: process.argv[2] || DEFAULT_OPENID,
    imageUrl: process.argv[3] || DEFAULT_IMAGE_URL,
    text: process.argv[4] || DEFAULT_TEXT,
  };
}

/**
 * 发送壁纸消息
 */
async function sendWallpaper(
  appId: string,
  clientSecret: string,
  openid: string,
  imageUrl: string,
  text: string
): Promise<void> {
  console.log('Getting access token...');
  const token = await getAccessToken(appId, clientSecret);
  console.log('Got access token');

  // 发送图片
  console.log('Sending image to:', openid);
  const imageResult = await sendC2CImageMessage(token, openid, imageUrl);
  console.log('Image sent successfully, ID:', imageResult.id);

  // 发送文字
  console.log('Sending text...');
  const textResult = await sendProactiveC2CMessage(token, openid, text);
  console.log('Text sent, message ID:', textResult.id);
}

/**
 * 主函数
 */
async function main(): Promise<void> {
  const config = loadConfig();
  const { appId, clientSecret } = getQQBotConfig(config);
  const { openid, imageUrl, text } = parseArgs();

  await sendWallpaper(appId, clientSecret, openid, imageUrl, text);
}

// 执行主函数
main().catch((err: Error) => {
  console.error('Error:', err.message);
  process.exit(1);
});
