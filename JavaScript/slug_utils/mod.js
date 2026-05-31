/**
 * slug_utils - URL-friendly Slug Generation Module
 * 
 * Zero-dependency JavaScript module for generating URL-friendly slugs.
 * Supports multiple languages, custom separators, case conversion, and more.
 * 
 * @author AllToolkit
 * @license MIT
 * @version 1.0.0
 */

/**
 * Default configuration for slug generation
 */
const DEFAULT_CONFIG = {
  separator: '-',
  lowercase: true,
  maxLength: null,
  trim: true,
  removeStopwords: false,
  stopwords: ['a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'],
  preserveLeadingUnderscore: false,
  preserveLeadingDash: false,
  preserveCase: false,
  strict: false,
  customReplacements: {}
};

/**
 * Character mappings for transliteration
 */
const CHAR_MAPPINGS = {
  // Latin
  'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A', 'Å': 'A', 'Æ': 'AE', 'Ç': 'C',
  'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E', 'Ì': 'I', 'Í': 'I', 'Î': 'I', 'Ï': 'I',
  'Ð': 'D', 'Ñ': 'N', 'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O', 'Ø': 'O',
  'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U', 'Ý': 'Y', 'Þ': 'TH', 'ß': 'ss',
  'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a', 'æ': 'ae', 'ç': 'c',
  'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e', 'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i',
  'ð': 'd', 'ñ': 'n', 'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'ø': 'o',
  'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u', 'ý': 'y', 'þ': 'th', 'ÿ': 'y',
  
  // Greek
  'α': 'a', 'β': 'b', 'γ': 'g', 'δ': 'd', 'ε': 'e', 'ζ': 'z', 'η': 'h', 'θ': 'th',
  'ι': 'i', 'κ': 'k', 'λ': 'l', 'μ': 'm', 'ν': 'n', 'ξ': 'x', 'ο': 'o', 'π': 'p',
  'ρ': 'r', 'σ': 's', 'τ': 't', 'υ': 'u', 'φ': 'ph', 'χ': 'ch', 'ψ': 'ps', 'ω': 'o',
  'Α': 'A', 'Β': 'B', 'Γ': 'G', 'Δ': 'D', 'Ε': 'E', 'Ζ': 'Z', 'Η': 'H', 'Θ': 'TH',
  'Ι': 'I', 'Κ': 'K', 'Λ': 'L', 'Μ': 'M', 'Ν': 'N', 'Ξ': 'X', 'Ο': 'O', 'Π': 'P',
  'Ρ': 'R', 'Σ': 'S', 'Τ': 'T', 'Υ': 'U', 'Φ': 'PH', 'Χ': 'CH', 'Ψ': 'PS', 'Ω': 'O',
  
  // Cyrillic
  'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh',
  'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
  'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c',
  'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'e', 'ю': 'yu',
  'я': 'ya',
  'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'ZH',
  'З': 'Z', 'И': 'I', 'Й': 'J', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O',
  'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'C',
  'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SCH', 'Ь': '', 'Ы': 'Y', 'Ъ': '', 'Э': 'E', 'Ю': 'YU',
  'Я': 'YA',
  
  // CJK (simplified Chinese romanization - pinyin)
  '啊': 'a', '阿': 'a', '爱': 'ai', '安': 'an', '暗': 'an',
  '吧': 'ba', '把': 'ba', '八': 'ba', '巴': 'ba', '白': 'bai', '百': 'bai', '拜': 'bai',
  '班': 'ban', '半': 'ban', '办': 'ban', '帮': 'bang', '包': 'bao', '保': 'bao', '报': 'bao',
  '北': 'bei', '被': 'bei', '备': 'bei', '本': 'ben', '比': 'bi', '笔': 'bi', '必': 'bi',
  '边': 'bian', '变': 'bian', '便': 'bian', '别': 'bie', '病': 'bing', '不': 'bu', '步': 'bu',
  '才': 'cai', '彩': 'cai', '菜': 'cai', '参': 'can', '草': 'cao', '层': 'ceng', '查': 'cha',
  '茶': 'cha', '差': 'cha', '常': 'chang', '场': 'chang', '唱': 'chang', '车': 'che',
  '称': 'cheng', '成': 'cheng', '城': 'cheng', '吃': 'chi', '持': 'chi', '充': 'chong', '出': 'chu',
  '除': 'chu', '处': 'chu', '传': 'chuan', '春': 'chun', '词': 'ci', '次': 'ci', '从': 'cong',
  '村': 'cun', '错': 'cuo', '打': 'da', '大': 'da', '带': 'dai', '代': 'dai', '单': 'dan',
  '但': 'dan', '蛋': 'dan', '当': 'dang', '党': 'dang', '到': 'dao', '道': 'dao', '得': 'de',
  '的': 'de', '等': 'deng', '低': 'di', '底': 'di', '点': 'dian', '电': 'dian', '定': 'ding',
  '冬': 'dong', '东': 'dong', '懂': 'dong', '动': 'dong', '都': 'dou', '读': 'du', '短': 'duan',
  '段': 'duan', '对': 'dui', '多': 'duo', '额': 'e', '恶': 'e', '儿': 'er', '而': 'er',
  '发': 'fa', '法': 'fa', '反': 'fan', '饭': 'fan', '方': 'fang', '房': 'fang', '放': 'fang',
  '飞': 'fei', '非': 'fei', '费': 'fei', '分': 'fen', '份': 'fen', '风': 'feng', '服': 'fu',
  '福': 'fu', '父': 'fu', '付': 'fu', '复': 'fu', '该': 'gai', '感': 'gan', '刚': 'gang',
  '高': 'gao', '告': 'gao', '歌': 'ge', '个': 'ge', '给': 'gei', '跟': 'gen', '根': 'gen',
  '工': 'gong', '公': 'gong', '共': 'gong', '狗': 'gou', '够': 'gou', '古': 'gu', '故': 'gu',
  '瓜': 'gua', '挂': 'gua', '关': 'guan', '管': 'guan', '光': 'guang', '广': 'guang', '贵': 'gui',
  '国': 'guo', '过': 'guo', '还': 'hai', '孩': 'hai', '海': 'hai', '害': 'hai', '汉': 'han',
  '号': 'hao', '好': 'hao', '喝': 'he', '合': 'he', '何': 'he', '和': 'he', '河': 'he',
  '黑': 'hei', '很': 'hen', '红': 'hong', '后': 'hou', '候': 'hou', '呼': 'hu', '湖': 'hu',
  '虎': 'hu', '护': 'hu', '花': 'hua', '化': 'hua', '话': 'hua', '坏': 'huai', '换': 'huan',
  '黄': 'huang', '回': 'hui', '会': 'hui', '婚': 'hun', '活': 'huo', '火': 'huo', '或': 'huo',
  '机': 'ji', '基': 'ji', '鸡': 'ji', '级': 'ji', '极': 'ji', '几': 'ji', '己': 'ji',
  '技': 'ji', '季': 'ji', '继': 'ji', '济': 'ji', '家': 'jia', '加': 'jia', '价': 'jia',
  '架': 'jia', '件': 'jian', '建': 'jian', '江': 'jiang', '讲': 'jiang', '交': 'jiao', '角': 'jiao',
  '脚': 'jiao', '叫': 'jiao', '街': 'jie', '节': 'jie', '姐': 'jie', '今': 'jin', '金': 'jin',
  '近': 'jin', '进': 'jin', '京': 'jing', '经': 'jing', '精': 'jing', '井': 'jing', '静': 'jing',
  '九': 'jiu', '酒': 'jiu', '久': 'jiu', '旧': 'jiu', '就': 'jiu', '举': 'ju', '句': 'ju',
  '剧': 'ju', '聚': 'ju', '决': 'jue', '觉': 'jue', '军': 'jun', '开': 'kai', '看': 'kan',
  '考': 'kao', '靠': 'kao', '科': 'ke', '可': 'ke', '课': 'ke', '刻': 'ke', '客': 'ke',
  '空': 'kong', '口': 'kou', '哭': 'ku', '苦': 'ku', '快': 'kuai', '块': 'kuai',
  '况': 'kuang', '困': 'kun', '拉': 'la', '来': 'lai', '蓝': 'lan', '老': 'lao', '乐': 'le',
  '累': 'lei', '冷': 'leng', '离': 'li', '里': 'li', '理': 'li', '礼': 'li', '力': 'li',
  '历': 'li', '立': 'li', '利': 'li', '连': 'lian', '脸': 'lian', '练': 'lian', '凉': 'liang',
  '两': 'liang', '亮': 'liang', '量': 'liang', '林': 'lin', '零': 'ling', '领': 'ling', '另': 'ling',
  '留': 'liu', '流': 'liu', '六': 'liu', '龙': 'long', '楼': 'lou', '陆': 'lu', '路': 'lu',
  '旅': 'lv', '绿': 'lv', '妈': 'ma', '马': 'ma', '吗': 'ma', '买': 'mai', '卖': 'mai',
  '慢': 'man', '满': 'man', '忙': 'mang', '毛': 'mao', '没': 'mei', '每': 'mei', '美': 'mei',
  '妹': 'mei', '门': 'men', '们': 'men', '米': 'mi', '面': 'mian', '民': 'min', '明': 'ming',
  '名': 'ming', '命': 'ming', '母': 'mu', '木': 'mu', '目': 'mu', '拿': 'na', '哪': 'na',
  '那': 'na', '奶': 'nai', '男': 'nan', '南': 'nan', '呢': 'ne', '内': 'nei', '能': 'neng',
  '你': 'ni', '年': 'nian', '念': 'nian', '鸟': 'niao', '您': 'nin', '牛': 'niu', '农': 'nong',
  '女': 'nv', '暖': 'nuan', '怕': 'pa', '拍': 'pai', '派': 'pai', '盘': 'pan', '跑': 'pao',
  '朋': 'peng', '皮': 'pi', '片': 'pian', '漂': 'piao', '票': 'piao', '品': 'pin', '平': 'ping',
  '苹': 'ping', '破': 'po', '普': 'pu', '七': 'qi', '期': 'qi', '其': 'qi', '奇': 'qi',
  '骑': 'qi', '起': 'qi', '气': 'qi', '汽': 'qi', '器': 'qi', '企': 'qi', '棋': 'qi',
  '千': 'qian', '前': 'qian', '钱': 'qian', '浅': 'qian', '强': 'qiang', '墙': 'qiang', '桥': 'qiao',
  '巧': 'qiao', '青': 'qing', '轻': 'qing', '清': 'qing', '晴': 'qing', '情': 'qing', '请': 'qing',
  '秋': 'qiu', '球': 'qiu', '求': 'qiu', '区': 'qu', '去': 'qu', '全': 'quan', '却': 'que',
  '群': 'qun', '然': 'ran', '让': 'rang', '热': 're', '人': 'ren', '认': 'ren', '日': 'ri',
  '容': 'rong', '肉': 'rou', '如': 'ru', '入': 'ru', '软': 'ruan', '若': 'ruo', '三': 'san',
  '色': 'se', '山': 'shan', '上': 'shang', '少': 'shao', '社': 'she', '身': 'shen', '深': 'shen',
  '什': 'shen', '生': 'sheng', '声': 'sheng', '师': 'shi', '十': 'shi', '时': 'shi', '实': 'shi',
  '食': 'shi', '始': 'shi', '使': 'shi', '世': 'shi', '市': 'shi', '事': 'shi', '是': 'shi',
  '室': 'shi', '试': 'shi', '视': 'shi', '收': 'shou', '手': 'shou', '首': 'shou', '受': 'shou',
  '书': 'shu', '树': 'shu', '术': 'shu', '束': 'shu', '数': 'shu', '双': 'shuang', '水': 'shui',
  '睡': 'shui', '顺': 'shun', '思': 'si', '死': 'si', '四': 'si', '送': 'song', '诉': 'su',
  '速': 'su', '算': 'suan', '虽': 'sui', '岁': 'sui', '所': 'suo', '他': 'ta', '她': 'ta',
  '它': 'ta', '台': 'tai', '太': 'tai', '态': 'tai', '谈': 'tan', '汤': 'tang', '糖': 'tang',
  '特': 'te', '疼': 'teng', '提': 'ti', '题': 'ti', '体': 'ti', '天': 'tian', '田': 'tian',
  '条': 'tiao', '铁': 'tie', '听': 'ting', '停': 'ting', '通': 'tong', '同': 'tong', '头': 'tou',
  '图': 'tu', '土': 'tu', '团': 'tuan', '推': 'tui', '腿': 'tui', '外': 'wai', '完': 'wan',
  '玩': 'wan', '晚': 'wan', '万': 'wan', '王': 'wang', '往': 'wang', '网': 'wang', '望': 'wang',
  '危': 'wei', '位': 'wei', '文': 'wen', '问': 'wen', '我': 'wo', '屋': 'wu', '五': 'wu',
  '午': 'wu', '物': 'wu', '务': 'wu', '西': 'xi', '吸': 'xi', '息': 'xi', '希': 'xi',
  '习': 'xi', '洗': 'xi', '系': 'xi', '细': 'xi', '下': 'xia', '夏': 'xia', '先': 'xian',
  '现': 'xian', '线': 'xian', '相': 'xiang', '想': 'xiang', '向': 'xiang', '象': 'xiang', '像': 'xiang',
  '小': 'xiao', '校': 'xiao', '笑': 'xiao', '些': 'xie', '写': 'xie', '谢': 'xie', '心': 'xin',
  '新': 'xin', '信': 'xin', '兴': 'xing', '星': 'xing', '行': 'xing', '形': 'xing', '醒': 'xing',
  '姓': 'xing', '休': 'xiu', '修': 'xiu', '需': 'xu', '许': 'xu', '学': 'xue', '雪': 'xue',
  '讯': 'xun', '迅': 'xun', '压': 'ya', '牙': 'ya', '亚': 'ya', '烟': 'yan', '言': 'yan',
  '研': 'yan', '眼': 'yan', '演': 'yan', '阳': 'yang', '养': 'yang', '样': 'yang', '药': 'yao',
  '要': 'yao', '爷': 'ye', '也': 'ye', '夜': 'ye', '业': 'ye', '叶': 'ye', '页': 'ye',
  '一': 'yi', '医': 'yi', '衣': 'yi', '以': 'yi', '已': 'yi', '意': 'yi', '易': 'yi',
  '因': 'yin', '音': 'yin', '银': 'yin', '印': 'yin', '英': 'ying', '影': 'ying', '应': 'ying',
  '用': 'yong', '永': 'yong', '涌': 'yong', '泳': 'yong', '勇': 'yong', '优': 'you',
  '由': 'you', '油': 'you', '游': 'you', '友': 'you', '有': 'you', '又': 'you', '右': 'you',
  '鱼': 'yu', '雨': 'yu', '语': 'yu', '元': 'yuan', '原': 'yuan', '园': 'yuan', '圆': 'yuan',
  '远': 'yuan', '院': 'yuan', '愿': 'yuan', '月': 'yue', '越': 'yue', '云': 'yun', '运': 'yun',
  '在': 'zai', '再': 'zai', '早': 'zao', '怎': 'zen', '站': 'zhan', '张': 'zhang', '找': 'zhao',
  '照': 'zhao', '者': 'zhe', '这': 'zhe', '真': 'zhen', '正': 'zheng', '政': 'zheng', '知': 'zhi',
  '之': 'zhi', '只': 'zhi', '纸': 'zhi', '指': 'zhi', '至': 'zhi', '治': 'zhi', '中': 'zhong',
  '钟': 'zhong', '周': 'zhou', '州': 'zhou', '主': 'zhu', '住': 'zhu', '注': 'zhu', '祝': 'zhu',
  '准': 'zhun', '字': 'zi', '自': 'zi', '走': 'zou', '租': 'zu', '足': 'zu', '组': 'zu',
  '祖': 'zu', '最': 'zui', '昨': 'zuo', '左': 'zuo', '作': 'zuo', '做': 'zuo', '坐': 'zuo',
  
  // Japanese (Hiragana/Katakana romanization)
  'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
  'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
  'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
  'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
  'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
  'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
  'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
  'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
  'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
  'わ': 'wa', 'を': 'wo', 'ん': 'n',
  'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
  'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
  'だ': 'da', 'ぢ': 'di', 'づ': 'du', 'で': 'de', 'ど': 'do',
  'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
  'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',
  'ア': 'a', 'イ': 'i', 'ウ': 'u', 'エ': 'e', 'オ': 'o',
  'カ': 'ka', 'キ': 'ki', 'ク': 'ku', 'ケ': 'ke', 'コ': 'ko',
  'サ': 'sa', 'シ': 'shi', 'ス': 'su', 'セ': 'se', 'ソ': 'so',
  'タ': 'ta', 'チ': 'chi', 'ツ': 'tsu', 'テ': 'te', 'ト': 'to',
  'ナ': 'na', 'ニ': 'ni', 'ヌ': 'nu', 'ネ': 'ne', 'ノ': 'no',
  'ハ': 'ha', 'ヒ': 'hi', 'フ': 'fu', 'ヘ': 'he', 'ホ': 'ho',
  'マ': 'ma', 'ミ': 'mi', 'ム': 'mu', 'メ': 'me', 'モ': 'mo',
  'ヤ': 'ya', 'ユ': 'yu', 'ヨ': 'yo',
  'ラ': 'ra', 'リ': 'ri', 'ル': 'ru', 'レ': 're', 'ロ': 'ro',
  'ワ': 'wa', 'ヲ': 'wo', 'ン': 'n',
  
  // Korean (Hangul romanization)
  '가': 'ga', '나': 'na', '다': 'da', '라': 'ra', '마': 'ma',
  '바': 'ba', '사': 'sa', '아': 'a', '자': 'ja', '차': 'cha',
  '카': 'ka', '타': 'ta', '파': 'pa', '하': 'ha',
  '거': 'geo', '너': 'neo', '더': 'deo', '러': 'reo', '머': 'meo', '버': 'beo', '서': 'seo', '저': 'jeo',
  '고': 'go', '노': 'no', 'do': 'do', '로': 'ro', '모': 'mo', '보': 'bo', '소': 'so', '조': 'jo',
  '구': 'gu', '누': 'nu', '두': 'du', '루': 'ru', '무': 'mu', '부': 'bu', '수': 'su', '주': 'ju',
  '그': 'geu', '느': 'neu', '드': 'deu', '르': 'reu', '므': 'meu', '브': 'beu', '스': 'seu', '즈': 'jeu',
  '위': 'wi', '의': 'ui', '가': 'ga', '카': 'ka', '타': 'ta', '파': 'pa',
  
  // Thai (simplified)
  'ก': 'k', 'ข': 'kh', 'ค': 'kh', 'ง': 'ng', 'จ': 'ch', 'ฉ': 'ch', 'ช': 'ch', 'ซ': 's',
  'ด': 'd', 'ต': 't', 'ถ': 'th', 'ท': 'th', 'น': 'n', 'บ': 'b', 'ป': 'p', 'พ': 'ph', 'ฟ': 'f',
  'ม': 'm', 'ย': 'y', 'ร': 'r', 'ล': 'l', 'ว': 'w', 'ส': 's', 'ห': 'h', 'อ': '',
  'ฮ': 'h', 'ะ': 'a', 'า': 'a', 'ิ': 'i', 'ี': 'i', 'ึ': 'ue', 'ื': 'ue', 'ุ': 'u', 'ู': 'u',
  'เ': 'e', 'แ': 'ae', 'โ': 'o', 'ใ': 'ai', 'ไ': 'ai',
  
  // Arabic (simplified)
  'ا': 'a', 'ب': 'b', 'ت': 't', 'ث': 'th', 'ج': 'j', 'ح': 'h', 'خ': 'kh', 'د': 'd',
  'ذ': 'dh', 'ر': 'r', 'ز': 'z', 'س': 's', 'ش': 'sh', 'ص': 's', 'ض': 'd', 'ط': 't',
  'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'q', 'ك': 'k', 'ل': 'l', 'م': 'm',
  'ن': 'n', 'ه': 'h', 'و': 'w', 'ي': 'y',
  
  // Vietnamese (diacritics)
  'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
  'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
  'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
  'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
  'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
  'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
  'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
  'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
  'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
  'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
  'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
  'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
  'đ': 'd', 'Đ': 'D',
  
  // Special currency/symbols
  '€': 'euro', '£': 'pound', '¥': 'yen', '¢': 'cent', '®': 'r', '©': 'c', '™': 'tm',
  '…': '...', '•': '-', '∞': 'infinity', '≠': 'not-equal', '≤': 'less-equal', '≥': 'greater-equal'
};

/**
 * Escape special regex characters
 * @param {string} string - String to escape
 * @returns {string} Escaped string
 */
function escapeRegex(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Merge user config with defaults
 * @param {Object} options - User options
 * @returns {Object} Merged config
 */
function mergeConfig(options = {}) {
  return {
    ...DEFAULT_CONFIG,
    ...options,
    stopwords: options.stopwords || DEFAULT_CONFIG.stopwords,
    customReplacements: options.customReplacements || DEFAULT_CONFIG.customReplacements
  };
}

/**
 * Transliterate characters to ASCII/Latin
 * @param {string} text - Text to transliterate
 * @returns {string} Transliterated text
 */
function transliterate(text) {
  let result = '';
  for (const char of text) {
    if (CHAR_MAPPINGS[char] !== undefined) {
      result += CHAR_MAPPINGS[char];
    } else {
      result += char;
    }
  }
  return result;
}

/**
 * Apply custom replacements
 * @param {string} text - Text to process
 * @param {Object} replacements - Custom replacement map
 * @returns {string} Processed text
 */
function applyCustomReplacements(text, replacements) {
  let result = text;
  for (const [from, to] of Object.entries(replacements)) {
    const regex = new RegExp(escapeRegex(from), 'gi');
    result = result.replace(regex, to);
  }
  return result;
}

/**
 * Remove stopwords from text
 * @param {string} text - Text to process
 * @param {string[]} stopwords - Array of stopwords
 * @param {string} separator - Separator character
 * @returns {string} Processed text
 */
function removeStopwords(text, stopwords, separator) {
  if (!stopwords || stopwords.length === 0) return text;
  const words = text.split(separator);
  return words.filter(word => !stopwords.includes(word.toLowerCase())).join(separator);
}

/**
 * Truncate slug at word boundaries
 * @param {string} text - Slug to truncate
 * @param {number} maxLength - Maximum length
 * @param {string} separator - Separator character
 * @returns {string} Truncated slug
 */
function truncateAtWordBoundary(text, maxLength, separator) {
  if (text.length <= maxLength) return text;
  
  let truncated = text.substring(0, maxLength);
  const lastSeparator = truncated.lastIndexOf(separator);
  
  if (lastSeparator > maxLength * 0.4) {
    truncated = truncated.substring(0, lastSeparator);
  }
  
  return truncated;
}

/**
 * Generate a URL-friendly slug from text
 * @param {string} text - Text to slugify
 * @param {Object|string} [options] - Options object or separator string
 * @returns {string} Generated slug
 */
function slugify(text, options = {}) {
  // Handle shorthand separator argument
  if (typeof options === 'string') {
    options = { separator: options };
  }
  
  const config = mergeConfig(options);
  
  if (!text || typeof text !== 'string') {
    return '';
  }
  
  let slug = text;
  
  // Apply custom replacements first
  if (config.customReplacements && Object.keys(config.customReplacements).length > 0) {
    slug = applyCustomReplacements(slug, config.customReplacements);
  }
  
  // Transliterate special characters
  slug = transliterate(slug);
  
  // Convert to lowercase if configured (lowercase: false preserves case)
  if (config.lowercase !== false) {
    slug = slug.toLowerCase();
  }
  
  // Remove non-word characters (keep underscores, hyphens, dots, tildes as they're valid in URLs)
  if (config.strict) {
    slug = slug.replace(/[^\w\s\-]/g, '');
  } else {
    slug = slug.replace(/[^\w\s\-\._~]/g, '');
  }
  
  // Replace whitespace with separator
  const sep = config.separator === '' ? '-' : config.separator;
  slug = slug.replace(/\s+/g, sep);
  
  // Remove leading/trailing separators
  if (config.trim) {
    slug = slug.replace(/^[\-\._]+/, '');
    slug = slug.replace(/[\-\._]+$/, '');
  }
  
  // Collapse multiple separators
  if (sep !== '') {
    const sepEscaped = escapeRegex(sep);
    slug = slug.replace(new RegExp(`${sepEscaped}+`, 'g'), sep);
  }
  
  // Remove stopwords if configured
  if (config.removeStopwords) {
    slug = removeStopwords(slug, config.stopwords, sep);
  }
  
  // Truncate at word boundary if max length specified
  if (config.maxLength && config.maxLength > 0) {
    const originalSlug = slug;
    slug = truncateAtWordBoundary(slug, config.maxLength, sep);
    // Re-trim after truncation
    if (config.trim) {
      slug = slug.replace(/^[\-\._]+/, '');
      slug = slug.replace(/[\-\._]+$/, '');
    }
    // If truncation made it worse (edge case), use direct truncation
    if (slug.length === 0 && originalSlug.length > config.maxLength) {
      slug = originalSlug.substring(0, config.maxLength);
    }
  }
  
  return slug;
}

/**
 * Validate a slug
 * @param {string} slug - Slug to validate
 * @param {Object} [options] - Validation options
 * @returns {Object} Validation result { valid: boolean, errors: string[] }
 */
function validateSlug(slug, options = {}) {
  const errors = [];
  
  if (!slug || typeof slug !== 'string') {
    return { valid: false, errors: ['Slug must be a non-empty string'] };
  }
  
  const config = mergeConfig(options);
  
  // Check if empty after trimming
  if (slug.trim() === '') {
    errors.push('Slug cannot be empty or contain only whitespace');
  }
  
  // Check for invalid characters (anything not word chars, hyphens, underscores, dots, tildes)
  if (!/^[\w\-\._~]+$/.test(slug)) {
    errors.push('Slug contains invalid characters. Only letters, numbers, hyphens, underscores, dots, and tildes are allowed');
  }
  
  // Check for leading separators
  if (/^[\-\._]+/.test(slug)) {
    errors.push('Slug should not start with separators');
  }
  
  // Check for trailing separators
  if (/[\-\._]+$/.test(slug)) {
    errors.push('Slug should not end with separators');
  }
  
  // Check for consecutive separators
  const sep = config.separator === '' ? '-' : config.separator;
  const sepEscaped = escapeRegex(sep);
  const consecPattern = new RegExp(`${sepEscaped}{2,}`);
  if (consecPattern.test(slug)) {
    errors.push('Slug should not contain consecutive separators');
  }
  
  // Check length
  if (slug.length > 255) {
    errors.push('Slug exceeds maximum length of 255 characters');
  }
  
  if (options.maxLength && slug.length > options.maxLength) {
    errors.push(`Slug exceeds specified maximum length of ${options.maxLength} characters`);
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
}

/**
 * Generate a unique slug by appending a number if collision detected
 * @param {string} text - Original text to slugify
 * @param {Function} isUnique - Function that checks if slug exists (async)
 * @param {Object} [options] - Slugify options
 * @returns {Promise<string>} Unique slug
 */
async function uniqueSlugify(text, isUnique, options = {}) {
  const config = mergeConfig(options);
  let slug = slugify(text, options);
  
  if (await isUnique(slug)) {
    let counter = 2;
    while (counter <= 10000) {
      const suffix = `${config.separator}${counter}`;
      let candidate = slug;
      const maxBaseLength = config.maxLength ? config.maxLength - suffix.length : 255 - suffix.length;
      
      if (candidate.length > maxBaseLength) {
        candidate = candidate.substring(0, maxBaseLength);
      }
      
      candidate = `${candidate}${suffix}`;
      
      if (await isUnique(candidate)) {
        return candidate;
      }
      counter++;
    }
    throw new Error('Unable to generate unique slug after 10000 attempts');
  }
  
  return slug;
}

/**
 * Generate a unique slug (synchronous version)
 * @param {string} text - Original text to slugify
 * @param {Function} isUnique - Function that checks if slug exists (sync)
 * @param {Object} [options] - Slugify options
 * @returns {string} Unique slug
 */
function uniqueSlugifySync(text, isUnique, options = {}) {
  const config = mergeConfig(options);
  let slug = slugify(text, options);
  
  if (!isUnique(slug)) {
    let counter = 2;
    while (counter <= 10000) {
      const suffix = `${config.separator}${counter}`;
      let candidate = slug;
      const maxBaseLength = config.maxLength ? config.maxLength - suffix.length : 255 - suffix.length;
      
      if (candidate.length > maxBaseLength) {
        candidate = candidate.substring(0, maxBaseLength);
      }
      
      candidate = `${candidate}${suffix}`;
      
      if (isUnique(candidate)) {
        return candidate;
      }
      counter++;
    }
    throw new Error('Unable to generate unique slug after 10000 attempts');
  }
  
  return slug;
}

/**
 * Convert a slug back to a readable title
 * @param {string} slug - Slug to convert
 * @param {Object} [options] - Options
 * @returns {string} Title string
 */
function unslugify(slug, options = {}) {
  if (!slug || typeof slug !== 'string') {
    return '';
  }
  
  const config = mergeConfig(options);
  const sep = config.separator === '' ? '-' : config.separator;
  
  return slug
    .split(sep)
    .filter(Boolean)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
}

/**
 * Extract slugs from text
 * @param {string} text - Text containing slugs
 * @param {Object} [options] - Options
 * @returns {string[]} Array of found slugs
 */
function extractSlugs(text, options = {}) {
  if (!text || typeof text !== 'string') {
    return [];
  }
  
  // Match sequences of word characters separated by non-word characters
  const matches = text.match(/[\w]+(?:[-_][\w]+)+/g) || [];
  
  return matches.map(slug => slugify(slug, options));
}

/**
 * Create a slug from multiple words/segments
 * @param {...(string|string[])} parts - Words or array of words
 * @returns {string} Combined slug
 */
function joinSlug(...parts) {
  const flat = parts.flat().filter(Boolean);
  return slugify(flat.join(' '));
}

/**
 * Parse a slug into its component parts
 * @param {string} slug - Slug to parse
 * @param {Object} [options] - Options
 * @returns {string[]} Array of slug parts
 */
function parseSlug(slug, options = {}) {
  if (!slug || typeof slug !== 'string') {
    return [];
  }
  
  const config = mergeConfig(options);
  const sep = config.separator === '' ? '-' : config.separator;
  return slug.split(sep).filter(Boolean);
}

/**
 * Convert options to URL query string format
 * @param {Object} options - Slugify options
 * @returns {string} Query string
 */
function optionsToQueryString(options) {
  const params = [];
  
  if (options.separator && options.separator !== DEFAULT_CONFIG.separator) {
    params.push(`separator=${encodeURIComponent(options.separator)}`);
  }
  if (options.lowercase === false) {
    params.push('lowercase=false');
  }
  if (options.maxLength) {
    params.push(`maxLength=${options.maxLength}`);
  }
  if (options.trim === false) {
    params.push('trim=false');
  }
  
  return params.join('&');
}

// Export functions
module.exports = {
  slugify,
  validateSlug,
  uniqueSlugify,
  uniqueSlugifySync,
  unslugify,
  extractSlugs,
  joinSlug,
  parseSlug,
  optionsToQueryString,
  
  // Expose for customization
  DEFAULT_CONFIG,
  CHAR_MAPPINGS,
  
  // Version info
  VERSION: '1.0.0',
  AUTHOR: 'AllToolkit'
};
