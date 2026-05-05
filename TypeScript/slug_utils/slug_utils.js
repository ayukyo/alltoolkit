/**
 * Slug Utils - URL Slug 生成工具 (JavaScript 版本)
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
 * 基础中文拼音映射表（常用字）
 */
const PINYIN_MAP = {
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
  '试': 'shi', '链': 'lian', '接': 'jie', '码': 'ma',
  '序': 'xu', '程': 'cheng', '编': 'bian', '号': 'hao', '名': 'ming',
  '称': 'cheng', '简': 'jian', '介': 'jie', '绍': 'shao', '内': 'nei',
  '容': 'rong', '信': 'xin', '息': 'xi', '系': 'xi', '统': 'tong',
  '用': 'yong', '户': 'hu', '登': 'deng', '录': 'lu', '注': 'zhu',
  '册': 'ce', '搜': 'sou', '索': 'suo', '找': 'zhao', '查': 'cha',
  '询': 'xun', '问': 'wen', '答': 'da', '案': 'an',
  '解': 'jie', '决': 'jue', '法': 'fa',
  '技': 'ji', '术': 'shu', '源': 'yuan', '工': 'gong',
  '具': 'ju', '框': 'kuang', '架': 'jia', '端': 'duan',
  '服': 'fu', '务': 'wu', '器': 'qi', '数': 'shu',
  '据': 'ju', '库': 'ku', '配': 'pei', '置': 'zhi',
  '件': 'jian', '目': 'mu', '路': 'lu', '径': 'jing',
  '参': 'can', '值': 'zhi', '类': 'lei', '型': 'xing',
  '象': 'xiang', '组': 'zu', '列': 'lie', '表': 'biao',
  '格': 'ge', '式': 'shi', '请': 'qing', '求': 'qiu',
  '响': 'xiang', '应': 'ying', '错': 'cuo', '误': 'wu', '异': 'yi',
  '常': 'chang', '处': 'chu', '理': 'li', '调': 'diao',
  '日': 'ri', '志': 'zhi', '性': 'xing', '优': 'you',
  '化': 'hua', '安': 'an', '全': 'quan', '权': 'quan', '限': 'xian',
  '菜': 'cai', '单': 'dan', '按': 'an', '钮': 'niu',
  '图': 'tu', '片': 'pian', '视': 'shi', '频': 'pin',
  '音': 'yin', '乐': 'le', '载': 'zai', '传': 'chuan',
  '分': 'fen', '享': 'xiang', '评': 'ping', '论': 'lun',
  '赞': 'zan', '收': 'shou', '藏': 'cang', '关': 'guan',
  '粉': 'fen', '丝': 'si', '消': 'xiao',
  '通': 'tong', '知': 'zhi', '提': 'ti', '醒': 'xing', '设': 'she',
  '博': 'bo', '客': 'ke', '新': 'xin', '闻': 'wen', '产': 'chan', '品': 'pin',
  '项': 'xiang', '团': 'tuan', '队': 'dui', '公': 'gong', '司': 'si',
  '职': 'zhi', '位': 'wei', '招': 'zhao', '聘': 'pin', '教': 'jiao', '育': 'yu',
  '培': 'pei', '训': 'xun', '活': 'huo', '动': 'dong', '比': 'bi', '赛': 'sai',
  '游': 'you', '戏': 'xi', '娱': 'yu', '电': 'dian', '影': 'ying',
  '书': 'shu', '籍': 'ji', '故': 'gu', '事': 'shi',
  '物': 'wu', '历': 'li', '史': 'shi',
  '科': 'ke', '自': 'zi', '然': 'ran', '社': 'she', '会': 'hui',
  '济': 'ji', '政': 'zheng', '治': 'zhi', '法': 'fa', '律': 'lv',
  '体': 'ti', '健': 'jian', '康': 'kang', '美': 'mei', '食': 'shi',
  // 扩展
  '智': 'zhi', '能': 'neng', '工': 'gong', '发': 'fa', '展': 'zhan',
  '历': 'li', '程': 'cheng', '入': 'ru', '门': 'men', '教': 'jiao',
  '深': 'shen', '度': 'du', '框': 'kuang', '架': 'jia', '对': 'dui',
  '比': 'bi', '析': 'xi', '然': 'ran', '语': 'yu', '言': 'yan',
  '处': 'chu', '实': 'shi', '战': 'zhan', '案': 'an', '例': 'li',
  '前': 'qian', '端': 'duan', '开': 'kai', '源': 'yuan',
  // 额外常用字
  '世': 'shi', '界': 'jie', '篇': 'pian', '人': 'ren',
};

/**
 * 检查是否为中文字符
 */
function isChinese(char) {
  return /[\u4e00-\u9fff]/.test(char);
}

/**
 * 将中文字符转换为拼音
 */
function chineseToPinyin(char) {
  return PINYIN_MAP[char] || '';
}

/**
 * 检查是否为有效字符（字母、数字、中文）
 */
function isValidChar(char) {
  return /[a-zA-Z0-9\u4e00-\u9fff]/.test(char);
}

/**
 * 检查是否为分隔符字符
 */
function isSeparatorChar(char, separator) {
  return char === separator || /[\s\-_~.]/.test(char);
}

/**
 * 转义正则表达式特殊字符
 */
function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Slug 生成器类
 */
class SlugGenerator {
  constructor(options = {}) {
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
   */
  generate(input) {
    if (!input || input.trim() === '') {
      return '';
    }

    let result = input;
    const separator = this.options.separator;
    const preserveSet = new Set(this.options.preserveChars);

    // 1. 转换中文为拼音
    if (this.options.convertChinese) {
      result = this.convertChineseToPinyin(result);
    }

    // 2. 处理特殊字符（在大小写转换之前）
    result = this.processSpecialChars(result);

    // 3. 应用大小写转换
    if (this.options.lowercase) {
      result = result.toLowerCase();
    }

    // 4. 替换空白字符为分隔符（但不替换保留字符）
    if (!preserveSet.has('_')) {
      result = result.replace(/[\s_]+/g, separator);
    } else {
      result = result.replace(/[\s]+/g, separator);
    }

    // 5. 合并连续分隔符
    if (this.options.collapseSeparators) {
      const escapedSep = escapeRegex(separator);
      result = result.replace(new RegExp(`${escapedSep}+`, 'g'), separator);
    }

    // 6. 去除首尾分隔符
    if (this.options.trimSeparator) {
      const escapedSep = escapeRegex(separator);
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
  convertChineseToPinyin(input) {
    let result = '';
    for (const char of input) {
      if (isChinese(char)) {
        const pinyin = chineseToPinyin(char);
        if (pinyin) {
          result += pinyin + '-';
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
  processSpecialChars(input) {
    const preserveSet = new Set(this.options.preserveChars);
    let result = '';

    for (const char of input) {
      if (isValidChar(char) || preserveSet.has(char) || char === this.options.separator) {
        result += char;
      } else if (char === '\'' || char === '`') {
        // 撇号直接跳过，不添加分隔符
        continue;
      } else if (this.options.removeSpecialChars) {
        result += this.options.separator;
      } else {
        result += char;
      }
    }

    return result;
  }

  /**
   * 在分隔符处截断字符串
   */
  truncateAtSeparator(input, maxLength) {
    if (input.length <= maxLength) {
      return input;
    }

    const escapedSep = escapeRegex(this.options.separator);
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
function slugify(input, options) {
  const generator = new SlugGenerator(options);
  return generator.generate(input);
}

/**
 * 从字符串生成唯一的 slug（带计数器）
 */
function slugifyUnique(input, existingSlugs, options) {
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
function isValidSlug(slug, separator = '-') {
  if (!slug || slug.length === 0) {
    return false;
  }

  const pattern = new RegExp(`^[a-z0-9${escapeRegex(separator)}]+$`, 'i');
  if (!pattern.test(slug)) {
    return false;
  }

  if (slug.startsWith(separator) || slug.endsWith(separator)) {
    return false;
  }

  const escapedSep = escapeRegex(separator);
  if (new RegExp(`${escapedSep}${escapedSep}`).test(slug)) {
    return false;
  }

  return true;
}

/**
 * 从 URL 中提取 slug
 */
function extractSlugFromUrl(url) {
  try {
    const urlObj = new URL(url);
    const pathParts = urlObj.pathname.split('/').filter(Boolean);
    if (pathParts.length > 0) {
      const lastPart = pathParts[pathParts.length - 1];
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
function slugifyBatch(inputs, options) {
  const generator = new SlugGenerator(options);
  return inputs.map(input => generator.generate(input));
}

/**
 * 将 slug 转换回可读标题
 */
function slugToTitle(slug, separator = '-') {
  if (!slug) return '';
  
  return slug
    .split(separator)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
}

// 导出
module.exports = {
  SlugGenerator,
  slugify,
  slugifyUnique,
  isValidSlug,
  extractSlugFromUrl,
  slugifyBatch,
  slugToTitle,
};