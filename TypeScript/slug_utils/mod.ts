/**
 * Slug Utils - URL Slug 生成工具
 * 
 * 功能：
 * - 将字符串转换为 URL 友好的 slug
 * - 支持中文拼音转换
 * - 支持多种配置选项
 * - 零外部依赖
 * 
 * @author AllToolkit
 * @date 2026-05-05
 */

/**
 * Slug 配置选项
 */
export interface SlugOptions {
  /** 分隔符，默认 '-' */
  separator?: string;
  /** 是否转换为小写，默认 true */
  lowercase?: boolean;
  /** 是否移除特殊字符，默认 true */
  removeSpecialChars?: boolean;
  /** 是否将中文转换为拼音，默认 false */
  convertChinese?: boolean;
  /** 最大长度，默认不限制 */
  maxLength?: number;
  /** 是否去除首尾分隔符，默认 true */
  trimSeparator?: boolean;
  /** 是否合并连续分隔符，默认 true */
  collapseSeparators?: boolean;
  /** 保留的字符（不会被移除） */
  preserveChars?: string[];
}

/**
 * 基础中文拼音映射表（常用字）
 */
const PINYIN_MAP: Record<string, string> = {
  // 常用字
  '你': 'ni', '好': 'hao', '我': 'wo', '是': 'shi', '的': 'de',
  '了': 'le', '不': 'bu', '在': 'zai', '有': 'you', '人': 'ren',
  '这': 'zhe', '中': 'zhong', '大': 'da', '为': 'wei', '上': 'shang',
  '个': 'ge', '国': 'guo', '和': 'he', '要': 'yao', '学': 'xue',
  '可': 'ke', '下': 'xia', '会': 'hui', '时': 'shi', '来': 'lai',
  '能': 'neng', '说': 'shuo', '生': 'sheng', '到': 'dao', '出': 'chu',
  '自': 'zi', '子': 'zi', '去': 'qu', '年': 'nian', '过': 'guo',
  '发': 'fa', '得': 'de', '作': 'zuo', '地': 'di', '后': 'hou',
  '成': 'cheng', '天': 'tian', '第': 'di', '对': 'dui', '多': 'duo',
  '小': 'xiao', '心': 'xin', '也': 'ye', '就': 'jiu', '么': 'me',
  '如': 'ru', '着': 'zhe', '想': 'xiang', '看': 'kan', '起': 'qi',
  '开': 'kai', '那': 'na', '里': 'li', '还': 'hai', '进': 'jin',
  '以': 'yi', '家': 'jia', '很': 'hen', '新': 'xin', '手': 'shou',
  '最': 'zui', '方': 'fang', '但': 'dan', '经': 'jing', '长': 'chang',
  '前': 'qian', '因': 'yin', '正': 'zheng', '点': 'dian', '度': 'du',
  '回': 'hui', '都': 'dou', '使': 'shi', '管': 'guan', '高': 'gao',
  // 数字
  '一': 'yi', '二': 'er', '三': 'san', '四': 'si', '五': 'wu',
  '六': 'liu', '七': 'qi', '八': 'ba', '九': 'jiu', '十': 'shi',
  '百': 'bai', '千': 'qian', '万': 'wan', '亿': 'yi',
  // 常用词
  '文': 'wen', '章': 'zhang', '标': 'biao', '题': 'ti', '测': 'ce',
  '试': 'shi', '链': 'lian', '接': 'jie', '码': 'ma', '码': 'ma',
  '序': 'xu', '程': 'cheng', '编': 'bian', '号': 'hao', '名': 'ming',
  '称': 'cheng', '简': 'jian', '介': 'jie', '绍': 'shao', '内': 'nei',
  '容': 'rong', '信': 'xin', '息': 'xi', '系': 'xi', '统': 'tong',
  '用': 'yong', '户': 'hu', '登': 'deng', '录': 'lu', '注': 'zhu',
  '册': 'ce', '搜': 'sou', '索': 'suo', '找': 'zhao', '查': 'cha',
  '询': 'xun', '问': 'wen', '答': 'da', '案': 'an', '问': 'wen',
  '题': 'ti', '解': 'jie', '决': 'jue', '方': 'fang', '法': 'fa',
  '技': 'ji', '术': 'shu', '开': 'kai', '源': 'yuan', '工': 'gong',
  '具': 'ju', '框': 'kuang', '架': 'jia', '前': 'qian', '端': 'duan',
  '后': 'hou', '服': 'fu', '务': 'wu', '器': 'qi', '数': 'shu',
  '据': 'ju', '库': 'ku', '配': 'pei', '置': 'zhi', '文': 'wen',
  '件': 'jian', '目': 'mu', '录': 'lu', '路': 'lu', '径': 'jing',
  '参': 'can', '数': 'shu', '值': 'zhi', '类': 'lei', '型': 'xing',
  '对': 'dui', '象': 'xiang', '组': 'zu', '列': 'lie', '表': 'biao',
  '格': 'ge', '式': 'shi', '件': 'jian', '请': 'qing', '求': 'qiu',
  '响': 'xiang', '应': 'ying', '错': 'cuo', '误': 'wu', '异': 'yi',
  '常': 'chang', '处': 'chu', '理': 'li', '调': 'diao', '试': 'shi',
  '日': 'ri', '志': 'zhi', '性': 'xing', '能': 'neng', '优': 'you',
  '化': 'hua', '安': 'an', '全': 'quan', '权': 'quan', '限': 'xian',
  '菜': 'cai', '单': 'dan', '按': 'an', '钮': 'niu', '链': 'lian',
  '接': 'jie', '图': 'tu', '片': 'pian', '视': 'shi', '频': 'pin',
  '音': 'yin', '乐': 'le', '下': 'xia', '载': 'zai', '上': 'shang',
  '传': 'chuan', '分': 'fen', '享': 'xiang', '评': 'ping', '论': 'lun',
  '点': 'dian', '赞': 'zan', '收': 'shou', '藏': 'cang', '关': 'guan',
  '注': 'zhu', '粉': 'fen', '丝': 'si', '消': 'xiao', '息': 'xi',
  '通': 'tong', '知': 'zhi', '提': 'ti', '醒': 'xing', '设': 'she',
  '置': 'zhi', '个': 'ge', '人': 'ren', '中': 'zhong', '心': 'xin',
  // 扩展常用词
  '博': 'bo', '客': 'ke', '新': 'xin', '闻': 'wen', '产': 'chan', '品': 'pin',
  '项': 'xiang', '目': 'mu', '团': 'tuan', '队': 'dui', '公': 'gong', '司': 'si',
  '职': 'zhi', '位': 'wei', '招': 'zhao', '聘': 'pin', '教': 'jiao', '育': 'yu',
  '培': 'pei', '训': 'xun', '活': 'huo', '动': 'dong', '比': 'bi', '赛': 'sai',
  '游': 'you', '戏': 'xi', '娱': 'yu', '乐': 'le', '电': 'dian', '影': 'ying',
  '书': 'shu', '籍': 'ji', '小': 'xiao', '说': 'shuo', '故': 'gu', '事': 'shi',
  '人': 'ren', '物': 'wu', '地': 'di', '理': 'li', '历': 'li', '史': 'shi',
  '科': 'ke', '学': 'xue', '自': 'zi', '然': 'ran', '社': 'she', '会': 'hui',
  '经': 'jing', '济': 'ji', '政': 'zheng', '治': 'zhi', '法': 'fa', '律': 'lv',
  '体': 'ti', '育': 'yu', '健': 'jian', '康': 'kang', '美': 'mei', '食': 'shi',
};

/**
 * 将中文字符转换为拼音
 */
function chineseToPinyin(char: string): string {
  return PINYIN_MAP[char] || '';
}

/**
 * 检查是否为中文字符
 */
function isChinese(char: string): boolean {
  return /[\u4e00-\u9fff]/.test(char);
}

/**
 * 检查是否为有效字符（字母、数字、中文）
 */
function isValidChar(char: string): boolean {
  return /[a-zA-Z0-9\u4e00-\u9fff]/.test(char);
}

/**
 * 检查是否为分隔符字符
 */
function isSeparatorChar(char: string, separator: string): boolean {
  return char === separator || /[\s\-_~.]/.test(char);
}

/**
 * Slug 生成器类
 */
export class SlugGenerator {
  private options: Required<SlugOptions>;

  constructor(options: SlugOptions = {}) {
    this.options = {
      separator: options.separator ?? '-',
      lowercase: options.lowercase ?? true,
      removeSpecialChars: options.removeSpecialChars ?? true,
      convertChinese: options.convertChinese ?? false,
      maxLength: options.maxLength ?? 0,
      trimSeparator: options.trimSeparator ?? true,
      collapseSeparators: options.collapseSeparators ?? true,
      preserveChars: options.preserveChars ?? [],
    };
  }

  /**
   * 生成 slug
   * @param input 输入字符串
   * @returns 生成的 slug
   */
  generate(input: string): string {
    if (!input || input.trim() === '') {
      return '';
    }

    let result = input;
    const separator = this.options.separator;

    // 1. 转换中文为拼音
    if (this.options.convertChinese) {
      result = this.convertChineseToPinyin(result);
    }

    // 2. 应用大小写转换
    if (this.options.lowercase) {
      result = result.toLowerCase();
    }

    // 3. 处理特殊字符
    result = this.processSpecialChars(result);

    // 4. 替换空白字符为分隔符
    result = result.replace(/[\s_]+/g, separator);

    // 5. 合并连续分隔符
    if (this.options.collapseSeparators) {
      const escapedSep = this.escapeRegex(separator);
      result = result.replace(new RegExp(`${escapedSep}+`, 'g'), separator);
    }

    // 6. 去除首尾分隔符
    if (this.options.trimSeparator) {
      const escapedSep = this.escapeRegex(separator);
      result = result.replace(new RegExp(`^${escapedSep}+|${escapedSep}+$`, 'g'), '');
    }

    // 7. 限制长度
    if (this.options.maxLength > 0 && result.length > this.options.maxLength) {
      result = this.truncateAtSeparator(result, this.options.maxLength);
    }

    return result;
  }

  /**
   * 转换中文为拼音
   */
  private convertChineseToPinyin(input: string): string {
    let result = '';
    for (const char of input) {
      if (isChinese(char)) {
        const pinyin = chineseToPinyin(char);
        if (pinyin) {
          result += pinyin + '-';
        } else {
          // 未找到映射，保留原字符或移除
          result += '';
        }
      } else {
        result += char;
      }
    }
    return result;
  }

  /**
   * 处理特殊字符
   */
  private processSpecialChars(input: string): string {
    const preserveSet = new Set(this.options.preserveChars);
    let result = '';

    for (const char of input) {
      if (isValidChar(char) || preserveSet.has(char) || char === this.options.separator) {
        result += char;
      } else if (this.options.removeSpecialChars) {
        // 移除特殊字符，替换为分隔符
        result += this.options.separator;
      } else {
        // 保留特殊字符
        result += char;
      }
    }

    return result;
  }

  /**
   * 转义正则表达式特殊字符
   */
  private escapeRegex(str: string): string {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  /**
   * 在分隔符处截断字符串
   */
  private truncateAtSeparator(input: string, maxLength: number): string {
    if (input.length <= maxLength) {
      return input;
    }

    const escapedSep = this.escapeRegex(this.options.separator);
    // 找到最后一个分隔符的位置
    const lastSeparatorIndex = input.lastIndexOf(this.options.separator, maxLength);
    
    if (lastSeparatorIndex > maxLength * 0.5) {
      return input.substring(0, lastSeparatorIndex);
    }
    
    return input.substring(0, maxLength).replace(new RegExp(`${escapedSep}+$`), '');
  }
}

/**
 * 快速生成 slug
 */
export function slugify(input: string, options?: SlugOptions): string {
  const generator = new SlugGenerator(options);
  return generator.generate(input);
}

/**
 * 从字符串生成唯一的 slug（带计数器）
 */
export function slugifyUnique(input: string, existingSlugs: Set<string>, options?: SlugOptions): string {
  const generator = new SlugGenerator(options);
  let slug = generator.generate(input);
  let counter = 1;
  let uniqueSlug = slug;

  while (existingSlugs.has(uniqueSlug)) {
    uniqueSlug = `${slug}-${counter}`;
    counter++;
  }

  return uniqueSlug;
}

/**
 * 验证 slug 是否有效
 */
export function isValidSlug(slug: string, separator: string = '-'): boolean {
  if (!slug || slug.length === 0) {
    return false;
  }

  // 检查是否只包含允许的字符
  const pattern = new RegExp(`^[a-z0-9${separator.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}]+$`, 'i');
  if (!pattern.test(slug)) {
    return false;
  }

  // 检查首尾是否为分隔符
  if (slug.startsWith(separator) || slug.endsWith(separator)) {
    return false;
  }

  // 检查是否有连续分隔符
  const escapedSep = separator.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  if (new RegExp(`${escapedSep}${escapedSep}`).test(slug)) {
    return false;
  }

  return true;
}

/**
 * 从 URL 中提取 slug
 */
export function extractSlugFromUrl(url: string): string {
  try {
    const urlObj = new URL(url);
    const pathParts = urlObj.pathname.split('/').filter(Boolean);
    if (pathParts.length > 0) {
      const lastPart = pathParts[pathParts.length - 1];
      // 移除文件扩展名
      const dotIndex = lastPart.lastIndexOf('.');
      return dotIndex > 0 ? lastPart.substring(0, dotIndex) : lastPart;
    }
    return '';
  } catch {
    return '';
  }
}

/**
 * 批量生成 slug
 */
export function slugifyBatch(inputs: string[], options?: SlugOptions): string[] {
  const generator = new SlugGenerator(options);
  return inputs.map(input => generator.generate(input));
}

/**
 * 将 slug 转换回可读标题
 */
export function slugToTitle(slug: string, separator: string = '-'): string {
  if (!slug) return '';
  
  return slug
    .split(separator)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
}

// 默认导出
export default {
  SlugGenerator,
  slugify,
  slugifyUnique,
  isValidSlug,
  extractSlugFromUrl,
  slugifyBatch,
  slugToTitle,
};