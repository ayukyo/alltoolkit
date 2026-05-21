/**
 * AllToolkit - Swift Pinyin Utilities
 *
 * 拼音转换工具类，支持将中文汉字转换为拼音。
 * 零依赖，仅使用 Swift 标准库。
 * 支持 iOS 13.0+, macOS 10.15+, watchOS 6.0+, tvOS 13.0+
 *
 * @author AllToolkit
 * @version 1.0.0
 */

import Foundation

// MARK: - 拼音工具类

/// 拼音转换工具类
public struct PinyinUtils {
    
    // MARK: - 拼音映射表
    
    /// 常用汉字拼音映射表（Unicode 范围：4E00-9FFF）
    /// 格式：[Unicode 值: (拼音, 带声调拼音)]
    private static let pinyinMap: [UInt32: (String, String)] = {
        let mapping: [(String, String, String)] = [
            // 常用汉字拼音映射（声调：1=阴平, 2=阳平, 3=上声, 4=去声）
            // A
            ("阿", "a", "ā"), ("啊", "a", "á"), ("哎", "ai", "āi"), ("哀", "ai", "āi"),
            ("爱", "ai", "ài"), ("安", "an", "ān"), ("按", "an", "àn"), ("暗", "an", "àn"),
            
            // B
            ("八", "ba", "bā"), ("爸", "ba", "bà"), ("白", "bai", "bái"), ("百", "bai", "bǎi"),
            ("班", "ban", "bān"), ("般", "ban", "bān"), ("板", "ban", "bǎn"), ("办", "ban", "bàn"),
            ("帮", "bang", "bāng"), ("包", "bao", "bāo"), ("保", "bao", "bǎo"), ("报", "bao", "bào"),
            ("北", "bei", "běi"), ("被", "bei", "bèi"), ("本", "ben", "běn"), ("比", "bi", "bǐ"),
            ("必", "bi", "bì"), ("边", "bian", "biān"), ("变", "bian", "biàn"), ("便", "bian", "biàn"),
            ("表", "biao", "biǎo"), ("别", "bie", "bié"), ("兵", "bing", "bīng"), ("并", "bing", "bìng"),
            ("病", "bing", "bìng"), ("不", "bu", "bù"),
            
            // C
            ("才", "cai", "cái"), ("材", "cai", "cái"), ("采", "cai", "cǎi"), ("菜", "cai", "cài"),
            ("参", "can", "cān"), ("餐", "can", "cān"), ("草", "cao", "cǎo"), ("层", "ceng", "céng"),
            ("茶", "cha", "chá"), ("查", "cha", "chá"), ("差", "cha", "chà"), ("长", "chang", "cháng"),
            ("常", "chang", "cháng"), ("厂", "chang", "chǎng"), ("场", "chang", "chǎng"),
            ("车", "che", "chē"), ("成", "cheng", "chéng"), ("城", "cheng", "chéng"), ("程", "cheng", "chéng"),
            ("吃", "chi", "chī"), ("尺", "chi", "chǐ"), ("出", "chu", "chū"), ("初", "chu", "chū"),
            ("处", "chu", "chù"), ("穿", "chuan", "chuān"), ("传", "chuan", "chuán"), ("船", "chuan", "chuán"),
            ("窗", "chuang", "chuāng"), ("床", "chuang", "chuáng"), ("创", "chuang", "chuàng"),
            ("春", "chun", "chūn"), ("词", "ci", "cí"), ("次", "ci", "cì"), ("从", "cong", "cóng"),
            ("村", "cun", "cūn"), ("存", "cun", "cún"), ("错", "cuo", "cuò"),
            
            // D
            ("达", "da", "dá"), ("大", "da", "dà"), ("代", "dai", "dài"), ("带", "dai", "dài"),
            ("待", "dai", "dài"), ("单", "dan", "dān"), ("但", "dan", "dàn"), ("当", "dang", "dāng"),
            ("党", "dang", "dǎng"), ("到", "dao", "dào"), ("道", "dao", "dào"), ("得", "de", "dé"),
            ("的", "de", "de"), ("地", "di", "dì"), ("点", "dian", "diǎn"), ("电", "dian", "diàn"),
            ("店", "dian", "diàn"), ("调", "diao", "diào"), ("定", "ding", "dìng"), ("东", "dong", "dōng"),
            ("动", "dong", "dòng"), ("都", "dou", "dōu"), ("度", "du", "dù"), ("短", "duan", "duǎn"),
            ("段", "duan", "duàn"), ("对", "dui", "duì"), ("多", "duo", "duō"),
            
            // E
            ("儿", "er", "ér"), ("而", "er", "ér"), ("二", "er", "èr"),
            
            // F
            ("发", "fa", "fā"), ("法", "fa", "fǎ"), ("反", "fan", "fǎn"), ("饭", "fan", "fàn"),
            ("方", "fang", "fāng"), ("房", "fang", "fáng"), ("放", "fang", "fàng"), ("非", "fei", "fēi"),
            ("飞", "fei", "fēi"), ("分", "fen", "fēn"), ("风", "feng", "fēng"), ("服", "fu", "fú"),
            ("福", "fu", "fú"), ("父", "fu", "fù"), ("负", "fu", "fù"), ("复", "fu", "fù"),
            
            // G
            ("该", "gai", "gāi"), ("改", "gai", "gǎi"), ("干", "gan", "gān"), ("感", "gan", "gǎn"),
            ("刚", "gang", "gāng"), ("高", "gao", "gāo"), ("告", "gao", "gào"), ("哥", "ge", "gē"),
            ("歌", "ge", "gē"), ("个", "ge", "gè"), ("各", "ge", "gè"), ("给", "gei", "gěi"),
            ("根", "gen", "gēn"), ("更", "geng", "gēng"), ("工", "gong", "gōng"), ("公", "gong", "gōng"),
            ("共", "gong", "gòng"), ("狗", "gou", "gǒu"), ("够", "gou", "gòu"), ("古", "gu", "gǔ"),
            ("股", "gu", "gǔ"), ("骨", "gu", "gǔ"), ("故", "gu", "gù"), ("关", "guan", "guān"),
            ("观", "guan", "guān"), ("馆", "guan", "guǎn"), ("光", "guang", "guāng"), ("广", "guang", "guǎng"),
            ("规", "gui", "guī"), ("国", "guo", "guó"), ("过", "guo", "guò"),
            
            // H
            ("海", "hai", "hǎi"), ("孩", "hai", "hái"), ("汉", "han", "hàn"), ("好", "hao", "hǎo"),
            ("号", "hao", "hào"), ("合", "he", "hé"), ("何", "he", "hé"), ("和", "he", "hé"),
            ("河", "he", "hé"), ("黑", "hei", "hēi"), ("很", "hen", "hěn"), ("红", "hong", "hóng"),
            ("后", "hou", "hòu"), ("候", "hou", "hòu"), ("湖", "hu", "hú"), ("互", "hu", "hù"),
            ("户", "hu", "hù"), ("花", "hua", "huā"), ("化", "hua", "huà"), ("话", "hua", "huà"),
            ("坏", "huai", "huài"), ("欢", "huan", "huān"), ("还", "huan", "huán"), ("换", "huan", "huàn"),
            ("黄", "huang", "huáng"), ("回", "hui", "huí"), ("会", "hui", "huì"), ("活", "huo", "huó"),
            ("火", "huo", "huǒ"), ("或", "huo", "huò"),
            
            // J
            ("机", "ji", "jī"), ("基", "ji", "jī"), ("及", "ji", "jí"), ("级", "ji", "jí"),
            ("极", "ji", "jí"), ("几", "ji", "jǐ"), ("己", "ji", "jǐ"), ("计", "ji", "jì"),
            ("记", "ji", "jì"), ("技", "ji", "jì"), ("际", "ji", "jì"), ("加", "jia", "jiā"),
            ("家", "jia", "jiā"), ("价", "jia", "jià"), ("假", "jia", "jiǎ"), ("间", "jian", "jiān"),
            ("建", "jian", "jiàn"), ("见", "jian", "jiàn"), ("件", "jian", "jiàn"), ("江", "jiang", "jiāng"),
            ("将", "jiang", "jiāng"), ("讲", "jiang", "jiǎng"), ("交", "jiao", "jiāo"), ("教", "jiao", "jiào"),
            ("叫", "jiao", "jiào"), ("接", "jie", "jiē"), ("结", "jie", "jié"), ("解", "jie", "jiě"),
            ("界", "jie", "jiè"), ("今", "jin", "jīn"), ("金", "jin", "jīn"), ("进", "jin", "jìn"),
            ("近", "jin", "jìn"), ("京", "jing", "jīng"), ("经", "jing", "jīng"), ("精", "jing", "jīng"),
            ("景", "jing", "jǐng"), ("净", "jing", "jìng"), ("静", "jing", "jìng"), ("九", "jiu", "jiǔ"),
            ("就", "jiu", "jiù"), ("局", "ju", "jú"), ("举", "ju", "jǔ"), ("据", "ju", "jù"),
            ("觉", "jue", "jué"), ("决", "jue", "jué"), ("军", "jun", "jūn"),
            
            // K
            ("开", "kai", "kāi"), ("看", "kan", "kàn"), ("康", "kang", "kāng"), ("考", "kao", "kǎo"),
            ("科", "ke", "kē"), ("可", "ke", "kě"), ("客", "ke", "kè"), ("课", "ke", "kè"),
            ("空", "kong", "kōng"), ("口", "kou", "kǒu"), ("苦", "ku", "kǔ"), ("快", "kuai", "kuài"),
            ("块", "kuai", "kuài"), ("况", "kuang", "kuàng"),
            
            // L
            ("拉", "la", "lā"), ("来", "lai", "lái"), ("老", "lao", "lǎo"), ("乐", "le", "lè"),
            ("了", "le", "le"), ("类", "lei", "lèi"), ("冷", "leng", "lěng"), ("离", "li", "lí"),
            ("里", "li", "lǐ"), ("理", "li", "lǐ"), ("力", "li", "lì"), ("历", "li", "lì"),
            ("立", "li", "lì"), ("利", "li", "lì"), ("连", "lian", "lián"), ("联", "lian", "lián"),
            ("脸", "lian", "liǎn"), ("练", "lian", "liàn"), ("两", "liang", "liǎng"), ("亮", "liang", "liàng"),
            ("量", "liang", "liàng"), ("林", "lin", "lín"), ("临", "lin", "lín"), ("领", "ling", "lǐng"),
            ("令", "ling", "lìng"), ("流", "liu", "liú"), ("六", "liu", "liù"), ("龙", "long", "lóng"),
            ("路", "lu", "lù"), ("录", "lu", "lù"), ("旅", "lv", "lǚ"), ("绿", "lv", "lǜ"),
            
            // M
            ("妈", "ma", "mā"), ("马", "ma", "mǎ"), ("吗", "ma", "ma"), ("买", "mai", "mǎi"),
            ("卖", "mai", "mài"), ("满", "man", "mǎn"), ("慢", "man", "màn"), ("忙", "mang", "máng"),
            ("毛", "mao", "máo"), ("么", "me", "me"), ("没", "mei", "méi"), ("每", "mei", "měi"),
            ("美", "mei", "měi"), ("妹", "mei", "mèi"), ("门", "men", "mén"), ("们", "men", "men"),
            ("米", "mi", "mǐ"), ("面", "mian", "miàn"), ("民", "min", "mín"), ("名", "ming", "míng"),
            ("明", "ming", "míng"), ("命", "ming", "mìng"), ("母", "mu", "mǔ"), ("木", "mu", "mù"),
            ("目", "mu", "mù"),
            
            // N
            ("那", "na", "nà"), ("南", "nan", "nán"), ("难", "nan", "nán"), ("内", "nei", "nèi"),
            ("能", "neng", "néng"), ("你", "ni", "nǐ"), ("年", "nian", "nián"), ("念", "nian", "niàn"),
            ("娘", "niang", "niáng"), ("鸟", "niao", "niǎo"), ("牛", "niu", "niú"), ("农", "nong", "nóng"),
            ("女", "nv", "nǚ"),
            
            // O
            ("欧", "ou", "ōu"),
            
            // P
            ("拍", "pai", "pāi"), ("排", "pai", "pái"), ("牌", "pai", "pái"), ("判", "pan", "pàn"),
            ("旁", "pang", "páng"), ("跑", "pao", "pǎo"), ("朋", "peng", "péng"), ("片", "pian", "piàn"),
            ("品", "pin", "pǐn"), ("平", "ping", "píng"), ("评", "ping", "píng"), ("破", "po", "pò"),
            ("普", "pu", "pǔ"),
            
            // Q
            ("七", "qi", "qī"), ("期", "qi", "qī"), ("其", "qi", "qí"), ("奇", "qi", "qí"),
            ("气", "qi", "qì"), ("器", "qi", "qì"), ("前", "qian", "qián"), ("钱", "qian", "qián"),
            ("强", "qiang", "qiáng"), ("桥", "qiao", "qiáo"), ("切", "qie", "qiē"), ("且", "qie", "qiě"),
            ("亲", "qin", "qīn"), ("青", "qing", "qīng"), ("清", "qing", "qīng"), ("情", "qing", "qíng"),
            ("请", "qing", "qǐng"), ("秋", "qiu", "qiū"), ("求", "qiu", "qiú"), ("区", "qu", "qū"),
            ("曲", "qu", "qū"), ("去", "qu", "qù"), ("全", "quan", "quán"), ("权", "quan", "quán"),
            ("确", "que", "què"),
            
            // R
            ("然", "ran", "rán"), ("让", "rang", "ràng"), ("热", "re", "rè"), ("人", "ren", "rén"),
            ("认", "ren", "rèn"), ("日", "ri", "rì"), ("容", "rong", "róng"), ("入", "ru", "rù"),
            
            // S
            ("三", "san", "sān"), ("色", "se", "sè"), ("森", "sen", "sēn"), ("山", "shan", "shān"),
            ("善", "shan", "shàn"), ("上", "shang", "shàng"), ("少", "shao", "shǎo"), ("舌", "she", "shé"),
            ("设", "she", "shè"), ("社", "she", "shè"), ("身", "shen", "shēn"), ("深", "shen", "shēn"),
            ("神", "shen", "shén"), ("生", "sheng", "shēng"), ("声", "sheng", "shēng"), ("省", "sheng", "shěng"),
            ("十", "shi", "shí"), ("时", "shi", "shí"), ("实", "shi", "shí"), ("识", "shi", "shí"),
            ("史", "shi", "shǐ"), ("使", "shi", "shǐ"), ("始", "shi", "shǐ"), ("世", "shi", "shì"),
            ("市", "shi", "shì"), ("示", "shi", "shì"), ("式", "shi", "shì"), ("事", "shi", "shì"),
            ("势", "shi", "shì"), ("视", "shi", "shì"), ("试", "shi", "shì"), ("室", "shi", "shì"),
            ("是", "shi", "shì"), ("书", "shu", "shū"), ("术", "shu", "shù"), ("树", "shu", "shù"),
            ("水", "shui", "shuǐ"), ("说", "shuo", "shuō"), ("司", "si", "sī"), ("思", "si", "sī"),
            ("死", "si", "sǐ"), ("四", "si", "sì"), ("送", "song", "sòng"), ("速", "su", "sù"),
            ("算", "suan", "suàn"), ("随", "sui", "suí"), ("岁", "sui", "suì"), ("孙", "sun", "sūn"),
            ("所", "suo", "suǒ"),
            
            // T
            ("他", "ta", "tā"), ("她", "ta", "tā"), ("它", "ta", "tā"), ("台", "tai", "tái"),
            ("太", "tai", "tài"), ("谈", "tan", "tán"), ("特", "te", "tè"), ("题", "ti", "tí"),
            ("体", "ti", "tǐ"), ("天", "tian", "tiān"), ("田", "tian", "tián"), ("条", "tiao", "tiáo"),
            ("听", "ting", "tīng"), ("通", "tong", "tōng"), ("同", "tong", "tóng"), ("统", "tong", "tǒng"),
            ("头", "tou", "tóu"), ("图", "tu", "tú"), ("土", "tu", "tǔ"), ("团", "tuan", "tuán"),
            ("推", "tui", "tuī"),
            
            // W
            ("外", "wai", "wài"), ("完", "wan", "wán"), ("万", "wan", "wàn"), ("王", "wang", "wáng"),
            ("网", "wang", "wǎng"), ("往", "wang", "wǎng"), ("忘", "wang", "wàng"), ("望", "wang", "wàng"),
            ("为", "wei", "wéi"), ("位", "wei", "wèi"), ("文", "wen", "wén"), ("问", "wen", "wèn"),
            ("我", "wo", "wǒ"), ("握", "wo", "wò"), ("无", "wu", "wú"), ("五", "wu", "wǔ"),
            ("武", "wu", "wǔ"), ("物", "wu", "wù"), ("务", "wu", "wù"),
            
            // X
            ("西", "xi", "xī"), ("希", "xi", "xī"), ("息", "xi", "xī"), ("习", "xi", "xí"),
            ("席", "xi", "xí"), ("洗", "xi", "xǐ"), ("系", "xi", "xì"), ("细", "xi", "xì"),
            ("戏", "xi", "xì"), ("下", "xia", "xià"), ("先", "xian", "xiān"), ("现", "xian", "xiàn"),
            ("线", "xian", "xiàn"), ("县", "xian", "xiàn"), ("限", "xian", "xiàn"), ("相", "xiang", "xiāng"),
            ("香", "xiang", "xiāng"), ("想", "xiang", "xiǎng"), ("向", "xiang", "xiàng"), ("象", "xiang", "xiàng"),
            ("像", "xiang", "xiàng"), ("小", "xiao", "xiǎo"), ("笑", "xiao", "xiào"), ("效", "xiao", "xiào"),
            ("些", "xie", "xiē"), ("写", "xie", "xiě"), ("血", "xie", "xuè"), ("心", "xin", "xīn"),
            ("新", "xin", "xīn"), ("信", "xin", "xìn"), ("星", "xing", "xīng"), ("行", "xing", "xíng"),
            ("形", "xing", "xíng"), ("性", "xing", "xìng"), ("姓", "xing", "xìng"), ("兄", "xiong", "xiōng"),
            ("学", "xue", "xué"), ("雪", "xue", "xuě"), ("血", "xue", "xuè"),
            
            // Y
            ("呀", "ya", "ya"), ("言", "yan", "yán"), ("研", "yan", "yán"), ("严", "yan", "yán"),
            ("颜", "yan", "yán"), ("眼", "yan", "yǎn"), ("演", "yan", "yǎn"), ("验", "yan", "yàn"),
            ("样", "yang", "yàng"), ("阳", "yang", "yáng"), ("洋", "yang", "yáng"), ("要", "yao", "yào"),
            ("业", "ye", "yè"), ("叶", "ye", "yè"), ("页", "ye", "yè"), ("夜", "ye", "yè"),
            ("一", "yi", "yī"), ("医", "yi", "yī"), ("依", "yi", "yī"), ("宜", "yi", "yí"),
            ("仪", "yi", "yí"), ("移", "yi", "yí"), ("已", "yi", "yǐ"), ("以", "yi", "yǐ"),
            ("艺", "yi", "yì"), ("议", "yi", "yì"), ("亦", "yi", "yì"), ("异", "yi", "yì"),
            ("易", "yi", "yì"), ("意", "yi", "yì"), ("义", "yi", "yì"), ("因", "yin", "yīn"),
            ("音", "yin", "yīn"), ("引", "yin", "yǐn"), ("印", "yin", "yìn"), ("英", "ying", "yīng"),
            ("应", "ying", "yīng"), ("营", "ying", "yíng"), ("影", "ying", "yǐng"), ("映", "ying", "yìng"),
            ("硬", "ying", "yìng"), ("用", "yong", "yòng"), ("优", "you", "yōu"), ("由", "you", "yóu"),
            ("油", "you", "yóu"), ("游", "you", "yóu"), ("友", "you", "yǒu"), ("有", "you", "yǒu"),
            ("又", "you", "yòu"), ("右", "you", "yòu"), ("幼", "you", "yòu"), ("于", "yu", "yú"),
            ("余", "yu", "yú"), ("鱼", "yu", "yú"), ("雨", "yu", "yǔ"), ("语", "yu", "yǔ"),
            ("元", "yuan", "yuán"), ("原", "yuan", "yuán"), ("源", "yuan", "yuán"), ("远", "yuan", "yuǎn"),
            ("院", "yuan", "yuàn"), ("月", "yue", "yuè"), ("乐", "yue", "yuè"), ("约", "yue", "yuē"),
            ("越", "yue", "yuè"), ("运", "yun", "yùn"),
            
            // Z
            ("杂", "za", "zá"), ("再", "zai", "zài"), ("在", "zai", "zài"), ("咱", "zan", "zán"),
            ("早", "zao", "zǎo"), ("作", "zuo", "zuò"), ("则", "ze", "zé"), ("怎", "zen", "zěn"),
            ("增", "zeng", "zēng"), ("展", "zhan", "zhǎn"), ("占", "zhan", "zhàn"), ("战", "zhan", "zhàn"),
            ("张", "zhang", "zhāng"), ("章", "zhang", "zhāng"), ("长", "zhang", "zhǎng"), ("掌", "zhang", "zhǎng"),
            ("招", "zhao", "zhāo"), ("找", "zhao", "zhǎo"), ("照", "zhao", "zhào"), ("真", "zhen", "zhēn"),
            ("正", "zheng", "zhèng"), ("证", "zheng", "zhèng"), ("支", "zhi", "zhī"), ("知", "zhi", "zhī"),
            ("之", "zhi", "zhī"), ("只", "zhi", "zhǐ"), ("指", "zhi", "zhǐ"), ("至", "zhi", "zhì"),
            ("制", "zhi", "zhì"), ("治", "zhi", "zhì"), ("质", "zhi", "zhì"), ("中", "zhong", "zhōng"),
            ("种", "zhong", "zhǒng"), ("重", "zhong", "zhòng"), ("周", "zhou", "zhōu"), ("主", "zhu", "zhǔ"),
            ("注", "zhu", "zhù"), ("住", "zhu", "zhù"), ("助", "zhu", "zhù"), ("专", "zhuan", "zhuān"),
            ("传", "zhuan", "zhuàn"), ("装", "zhuang", "zhuāng"), ("准", "zhun", "zhǔn"), ("着", "zhuo", "zhe"),
            ("子", "zi", "zǐ"), ("字", "zi", "zì"), ("自", "zi", "zì"), ("总", "zong", "zǒng"),
            ("走", "zou", "zǒu"), ("族", "zu", "zú"), ("组", "zu", "zǔ"), ("最", "zui", "zuì"),
            ("罪", "zui", "zuì"), ("左", "zuo", "zuǒ")
        ]
        
        var map: [UInt32: (String, String)] = [:]
        for (char, pinyin, pinyinWithTone) in mapping {
            if let scalar = char.unicodeScalars.first {
                map[scalar.value] = (pinyin, pinyinWithTone)
            }
        }
        return map
    }()
    
    // MARK: - 公开方法
    
    /// 将中文字符串转换为拼音
    /// - Parameters:
    ///   - text: 输入的中文字符串
    ///   - withTone: 是否包含声调，默认 false
    ///   - separator: 拼音之间的分隔符，默认空格
    /// - Returns: 拼音字符串
    public static func toPinyin(_ text: String, withTone: Bool = false, separator: String = " ") -> String {
        return text.map { char -> String in
            if let scalar = char.unicodeScalars.first {
                // 检查是否为中文字符范围 (CJK Unified Ideographs: 4E00-9FFF)
                if scalar.value >= 0x4E00 && scalar.value <= 0x9FFF {
                    if let (pinyin, pinyinWithTone) = pinyinMap[scalar.value] {
                        return withTone ? pinyinWithTone : pinyin
                    } else {
                        // 未知汉字，返回原字符
                        return String(char)
                    }
                }
            }
            // 非中文字符，返回原字符
            return String(char)
        }.joined(separator: separator)
    }
    
    /// 将中文字符串转换为拼音首字母
    /// - Parameter text: 输入的中文字符串
    /// - Returns: 拼音首字母字符串
    public static func toPinyinInitials(_ text: String) -> String {
        return text.compactMap { char -> String? in
            if let scalar = char.unicodeScalars.first {
                // 检查是否为中文字符
                if scalar.value >= 0x4E00 && scalar.value <= 0x9FFF {
                    if let (pinyin, _) = pinyinMap[scalar.value] {
                        return String(pinyin.prefix(1)).uppercased()
                    }
                    return nil
                }
                // 非中文字符，直接返回大写字母
                if char.isLetter {
                    return char.uppercased()
                }
            }
            return nil
        }.joined()
    }
    
    /// 获取单个汉字的拼音
    /// - Parameters:
    ///   - char: 单个汉字字符
    ///   - withTone: 是否包含声调
    /// - Returns: 拼音字符串，如果不是汉字则返回 nil
    public static func getPinyin(_ char: Character, withTone: Bool = false) -> String? {
        guard let scalar = char.unicodeScalars.first else { return nil }
        
        // 检查是否为中文字符
        guard scalar.value >= 0x4E00 && scalar.value <= 0x9FFF else {
            return nil
        }
        
        if let (pinyin, pinyinWithTone) = pinyinMap[scalar.value] {
            return withTone ? pinyinWithTone : pinyin
        }
        
        return nil
    }
    
    /// 检查字符是否为中文字符
    /// - Parameter char: 要检查的字符
    /// - Returns: 是否为中文字符
    public static func isChinese(_ char: Character) -> Bool {
        guard let scalar = char.unicodeScalars.first else { return false }
        return scalar.value >= 0x4E00 && scalar.value <= 0x9FFF
    }
    
    /// 检查字符串是否只包含中文字符
    /// - Parameter text: 要检查的字符串
    /// - Returns: 是否只包含中文字符
    public static func isAllChinese(_ text: String) -> String {
        guard !text.isEmpty else { return "false" }
        let allChinese = text.allSatisfy { isChinese($0) }
        return allChinese ? "true" : "false"
    }
    
    /// 统计字符串中的中文字符数量
    /// - Parameter text: 要统计的字符串
    /// - Returns: 中文字符数量
    public static func countChinese(_ text: String) -> Int {
        return text.filter { isChinese($0) }.count
    }
    
    /// 将拼音转换为带声调的拼音
    /// - Parameters:
    ///   - pinyin: 不带声调的拼音
    ///   - tone: 声调 (1-4)
    /// - Returns: 带声调的拼音
    public static func addTone(_ pinyin: String, tone: Int) -> String {
        guard (1...4).contains(tone) else { return pinyin }
        
        let vowelMap: [Character: [String]] = [
            "a": ["ā", "á", "ǎ", "à"],
            "e": ["ē", "é", "ě", "è"],
            "i": ["ī", "í", "ǐ", "ì"],
            "o": ["ō", "ó", "ǒ", "ò"],
            "u": ["ū", "ú", "ǔ", "ù"],
            "ü": ["ǖ", "ǘ", "ǚ", "ǜ"]
        ]
        
        var result = pinyin.lowercased()
        let toneIndex = tone - 1
        
        // 声调标记规则：a 存在时标记在 a 上，否则标记在最后一个元音上
        // 例外：当 i 和 u 同时存在时，标记在后者上
        
        if result.contains("a") {
            if let index = result.firstIndex(of: "a"),
               let tones = vowelMap["a"] {
                result.replaceSubrange(index...index, with: tones[toneIndex])
                return result
            }
        }
        
        if result.contains("e") {
            if let index = result.firstIndex(of: "e"),
               let tones = vowelMap["e"] {
                result.replaceSubrange(index...index, with: tones[toneIndex])
                return result
            }
        }
        
        // 处理 ou 的情况
        if result.contains("ou") {
            if let index = result.firstIndex(of: "o"),
               let tones = vowelMap["o"] {
                result.replaceSubrange(index...index, with: tones[toneIndex])
                return result
            }
        }
        
        // 找到最后一个元音
        let vowels = "aeiouvü"
        if let lastIndex = result.lastIndex(where: { vowels.contains($0) }) {
            let vowel = result[lastIndex]
            if let tones = vowelMap[vowel] {
                result.replaceSubrange(lastIndex...lastIndex, with: tones[toneIndex])
            }
        }
        
        return result
    }
    
    /// 比较两个中文字符串的拼音是否相同（忽略声调）
    /// - Parameters:
    ///   - lhs: 第一个字符串
    ///   - rhs: 第二个字符串
    /// - Returns: 拼音是否相同
    public static func pinyinEqual(_ lhs: String, _ rhs: String) -> Bool {
        return toPinyin(lhs) == toPinyin(rhs)
    }
    
    /// 按拼音对中文字符串数组进行排序
    /// - Parameters:
    ///   - texts: 要排序的中文字符串数组
    ///   - ascending: 是否升序，默认 true
    /// - Returns: 排序后的数组
    public static func sortByPinyin(_ texts: [String], ascending: Bool = true) -> [String] {
        return texts.sorted { lhs, rhs in
            let lhsPinyin = toPinyin(lhs)
            let rhsPinyin = toPinyin(rhs)
            return ascending ? lhsPinyin < rhsPinyin : lhsPinyin > rhsPinyin
        }
    }
    
    /// 根据拼音首字母分组
    /// - Parameter texts: 要分组的中文字符串数组
    /// - Returns: 按首字母分组的字典
    public static func groupByInitial(_ texts: [String]) -> [String: [String]] {
        var groups: [String: [String]] = [:]
        
        for text in texts {
            let initial = toPinyinInitials(text).first.map(String.init) ?? "#"
            if groups[initial] == nil {
                groups[initial] = []
            }
            groups[initial]?.append(text)
        }
        
        return groups
    }
    
    /// 在中文文本中搜索拼音匹配
    /// - Parameters:
    ///   - query: 拼音查询字符串
    ///   - texts: 要搜索的中文文本数组
    ///   - fuzzy: 是否启用模糊匹配（忽略分隔符）
    /// - Returns: 匹配的文本数组
    public static func searchByPinyin(_ query: String, in texts: [String], fuzzy: Bool = true) -> [String] {
        let normalizedQuery = query.lowercased().filter { $0.isLetter }
        
        return texts.filter { text in
            let pinyin = toPinyin(text).lowercased()
            let normalizedPinyin = fuzzy ? pinyin.filter { $0.isLetter || $0.isNumber } : pinyin
            
            if fuzzy {
                return normalizedPinyin.contains(normalizedQuery)
            } else {
                return normalizedPinyin.contains(normalizedQuery)
            }
        }
    }
}

// MARK: - String 扩展

public extension String {
    
    /// 将中文字符串转换为拼音
    /// - Parameters:
    ///   - withTone: 是否包含声调，默认 false
    ///   - separator: 拼音之间的分隔符，默认空格
    /// - Returns: 拼音字符串
    func toPinyin(withTone: Bool = false, separator: String = " ") -> String {
        return PinyinUtils.toPinyin(self, withTone: withTone, separator: separator)
    }
    
    /// 将中文字符串转换为拼音首字母
    /// - Returns: 拼音首字母字符串
    var pinyinInitials: String {
        return PinyinUtils.toPinyinInitials(self)
    }
    
    /// 检查是否只包含中文字符
    var isAllChinese: Bool {
        return PinyinUtils.isAllChinese(self) == "true"
    }
    
    /// 统计中文字符数量
    var chineseCount: Int {
        return PinyinUtils.countChinese(self)
    }
}