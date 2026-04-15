//! # Slug Utils
//! 
//! 一个零外部依赖的 Rust URL Slug 生成工具库
//! 
//! ## 功能特性
//! - 字符串转 URL 友好 slug
//! - 支持中文转拼音（内置常用字库）
//! - 自定义分隔符
//! - 大小写转换选项
//! - 最大长度限制
//! - 去除停用词
//! - 批量处理

use std::collections::HashMap;

/// Slug 生成器配置
#[derive(Debug, Clone)]
pub struct SlugOptions {
    /// 分隔符，默认 "-"
    pub separator: String,
    /// 是否转换为小写，默认 true
    pub lowercase: bool,
    /// 最大长度，0 表示不限制
    pub max_length: usize,
    /// 是否去除停用词
    pub remove_stop_words: bool,
    /// 是否保留数字
    pub keep_numbers: bool,
}

impl Default for SlugOptions {
    fn default() -> Self {
        Self {
            separator: "-".to_string(),
            lowercase: true,
            max_length: 0,
            remove_stop_words: false,
            keep_numbers: true,
        }
    }
}

/// Slug 生成器
pub struct SlugGenerator {
    options: SlugOptions,
    stop_words: Vec<String>,
    pinyin_map: HashMap<char, &'static str>,
}

impl Default for SlugGenerator {
    fn default() -> Self {
        Self::new(SlugOptions::default())
    }
}

impl SlugGenerator {
    /// 创建新的 Slug 生成器
    pub fn new(options: SlugOptions) -> Self {
        Self {
            options,
            stop_words: get_default_stop_words(),
            pinyin_map: build_pinyin_map(),
        }
    }

    /// 设置停用词列表
    pub fn with_stop_words(mut self, stop_words: Vec<String>) -> Self {
        self.stop_words = stop_words;
        self
    }

    /// 将字符串转换为 slug
    pub fn slugify(&self, input: &str) -> String {
        let mut result = String::new();
        let chars: Vec<char> = input.chars().collect();
        let mut i = 0;

        while i < chars.len() {
            let c = chars[i];

            // 处理中文字符
            if is_chinese(c) {
                if let Some(pinyin) = self.pinyin_map.get(&c) {
                    if !result.is_empty() && !result.ends_with(&self.options.separator) {
                        result.push_str(&self.options.separator);
                    }
                    result.push_str(pinyin);
                }
                i += 1;
                continue;
            }

            // 处理字母
            if c.is_alphabetic() {
                let transformed = if self.options.lowercase {
                    c.to_lowercase().to_string()
                } else {
                    c.to_string()
                };
                result.push_str(&transformed);
                i += 1;
                continue;
            }

            // 处理数字
            if c.is_ascii_digit() {
                if self.options.keep_numbers {
                    result.push(c);
                } else {
                    // 数字被跳过时，检查是否需要插入分隔符
                    if !result.is_empty() && !result.ends_with(&self.options.separator) {
                        // 检查下一个字符是否是字母
                        if i + 1 < chars.len() && chars[i + 1].is_alphabetic() {
                            result.push_str(&self.options.separator);
                        }
                    }
                }
                i += 1;
                continue;
            }

            // 处理空格和分隔符
            if c.is_whitespace() || c == '-' || c == '_' {
                if !result.is_empty() && !result.ends_with(&self.options.separator) {
                    result.push_str(&self.options.separator);
                }
                i += 1;
                continue;
            }

            // 其他特殊字符跳过，但可能需要插入分隔符
            if !result.is_empty() && !result.ends_with(&self.options.separator) {
                // 检查下一个字符是否是字母或数字
                if i + 1 < chars.len() && (chars[i + 1].is_alphabetic() || chars[i + 1].is_ascii_digit()) {
                    result.push_str(&self.options.separator);
                }
            }
            i += 1;
        }

        // 后处理
        self.post_process(result)
    }

    /// 从文件名生成 slug
    pub fn from_filename(&self, filename: &str) -> String {
        // 移除扩展名
        let name = filename.rsplit_once('.').map(|(n, _)| n).unwrap_or(filename);
        self.slugify(name)
    }

    /// 批量生成 slug
    pub fn slugify_batch(&self, inputs: &[&str]) -> Vec<String> {
        inputs.iter().map(|s| self.slugify(s)).collect()
    }

    /// 生成唯一 slug（添加后缀）
    pub fn unique_slug(&self, base: &str, existing: &[String]) -> String {
        let base_slug = self.slugify(base);
        
        if !existing.contains(&base_slug) {
            return base_slug;
        }

        let mut counter = 1;
        loop {
            let candidate = format!("{}{}{}", base_slug, self.options.separator, counter);
            if !existing.contains(&candidate) {
                return candidate;
            }
            counter += 1;
        }
    }

    /// 后处理：清理和截断
    fn post_process(&self, mut slug: String) -> String {
        // 去除停用词
        if self.options.remove_stop_words {
            for word in &self.stop_words {
                let pattern1 = format!("{}{}{}", &self.options.separator, word, &self.options.separator);
                let pattern2 = format!("{}{}", &self.options.separator, word);
                let pattern3 = format!("{}{}", word, &self.options.separator);
                
                slug = slug.replace(&pattern1, &self.options.separator);
                slug = slug.replace(&pattern2, "");
                slug = slug.replace(&pattern3, "");
            }
        }

        // 清理多余的分隔符
        while slug.contains(&format!("{}{}", &self.options.separator, &self.options.separator)) {
            slug = slug.replace(
                &format!("{}{}", &self.options.separator, &self.options.separator),
                &self.options.separator
            );
        }

        // 去除首尾分隔符
        while slug.starts_with(&self.options.separator) {
            slug = slug[self.options.separator.len()..].to_string();
        }
        while slug.ends_with(&self.options.separator) {
            let len = slug.len();
            slug = slug[..len - self.options.separator.len()].to_string();
        }

        // 截断到最大长度
        if self.options.max_length > 0 && slug.len() > self.options.max_length {
            slug = slug[..self.options.max_length].to_string();
            // 确保不以分隔符结尾
            while slug.ends_with(&self.options.separator) {
                let len = slug.len();
                slug = slug[..len - self.options.separator.len()].to_string();
            }
        }

        slug
    }
}

/// 检查字符是否为中文字符
fn is_chinese(c: char) -> bool {
    matches!(c, '\u{4E00}'..='\u{9FFF}')
}

/// 获取默认停用词列表
fn get_default_stop_words() -> Vec<String> {
    vec![
        "a".to_string(), "an".to_string(), "the".to_string(),
        "and".to_string(), "or".to_string(), "but".to_string(),
        "in".to_string(), "on".to_string(), "at".to_string(),
        "to".to_string(), "for".to_string(), "of".to_string(),
        "is".to_string(), "are".to_string(), "was".to_string(),
        "were".to_string(), "be".to_string(), "been".to_string(),
    ]
}

/// 构建中文到拼音的映射（常用字）
fn build_pinyin_map() -> HashMap<char, &'static str> {
    let pairs: Vec<(char, &'static str)> = vec![
        // 常用字拼音映射（使用正确的英文单引号）
        ('中', "zhong"), ('文', "wen"), ('标', "biao"), ('题', "ti"),
        ('测', "ce"), ('试', "shi"), ('开', "kai"), ('发', "fa"),
        ('学', "xue"), ('习', "xi"), ('编', "bian"), ('程', "cheng"),
        ('语', "yu"), ('言', "yan"), ('数', "shu"), ('据', "ju"),
        ('网', "wang"), ('络', "luo"), ('系', "xi"), ('统', "tong"),
        ('欢', "huan"), ('迎', "ying"), ('使', "shi"), ('用', "yong"),
        ('简', "jian"), ('单', "dan"), ('复', "fu"), ('杂', "za"),
        ('快', "kuai"), ('慢', "man"), ('好', "hao"), ('坏', "huai"),
        ('大', "da"), ('小', "xiao"), ('多', "duo"), ('少', "shao"),
        ('高', "gao"), ('低', "di"), ('长', "chang"), ('短', "duan"),
        ('新', "xin"), ('旧', "jiu"), ('老', "lao"),
        ('人', "ren"), ('事', "shi"), ('物', "wu"), ('地', "di"),
        ('时', "shi"), ('年', "nian"), ('月', "yue"), ('日', "ri"),
        ('今', "jin"), ('明', "ming"), ('昨', "zuo"), ('后', "hou"),
        ('前', "qian"), ('上', "shang"), ('下', "xia"), ('左', "zuo"),
        ('右', "you"), ('里', "li"), ('外', "wai"), ('内', "nei"),
        ('这', "zhe"), ('那', "na"), ('什', "shi"), ('么', "me"),
        ('怎', "zen"), ('样', "yang"), ('为', "wei"), ('何', "he"),
        ('谁', "shui"), ('哪', "na"), ('儿', "er"),
        ('我', "wo"), ('你', "ni"), ('他', "ta"), ('她', "ta"),
        ('它', "ta"), ('们', "men"), ('的', "de"), ('是', "shi"),
        ('在', "zai"), ('有', "you"), ('和', "he"), ('与', "yu"),
        ('或', "huo"), ('但', "dan"), ('如', "ru"), ('果', "guo"),
        ('因', "yin"), ('所', "suo"), ('以', "yi"), ('可', "ke"),
        ('能', "neng"), ('会', "hui"), ('要', "yao"), ('想', "xiang"),
        ('做', "zuo"), ('作', "zuo"), ('工', "gong"),
        ('读', "du"), ('写', "xie"), ('说', "shuo"), ('听', "ting"),
        ('看', "kan"), ('走', "zou"), ('跑', "pao"), ('跳', "tiao"),
        ('吃', "chi"), ('喝', "he"), ('睡', "shui"), ('玩', "wan"),
        ('电', "dian"), ('脑', "nao"), ('手', "shou"), ('机', "ji"),
        ('平', "ping"), ('台', "tai"), ('应', "ying"), ('用', "yong"),
        ('软', "ruan"), ('件', "jian"), ('硬', "ying"), ('序', "xu"),
        ('码', "ma"), ('代', "dai"), ('算', "suan"), ('法', "fa"),
        ('结', "jie"), ('果', "guo"), ('错', "cuo"), ('误', "wu"),
        ('正', "zheng"), ('确', "que"), ('成', "cheng"), ('功', "gong"),
        ('失', "shi"), ('败', "bai"), ('启', "qi"), ('动', "dong"),
        ('停', "ting"), ('止', "zhi"), ('运', "yun"), ('行', "xing"),
        ('配', "pei"), ('置', "zhi"), ('设', "she"), ('计', "ji"),
        ('模', "mo"), ('块', "kuai"), ('功', "gong"), ('能', "neng"),
        ('特', "te"), ('性', "xing"), ('属', "shu"),
        ('方', "fang"), ('法', "fa"), ('类', "lei"), ('型', "xing"),
        ('对', "dui"), ('象', "xiang"), ('接', "jie"), ('口', "kou"),
        ('参', "can"), ('数', "shu"), ('变', "bian"), ('量', "liang"),
        ('常', "chang"), ('量', "liang"), ('函', "han"),
        ('过', "guo"), ('程', "cheng"), ('事', "shi"), ('件', "jian"),
        ('消', "xiao"), ('息', "xi"), ('通', "tong"), ('知', "zhi"),
        ('警', "jing"), ('告', "gao"), ('错', "cuo"), ('误', "wu"),
        ('异', "yi"), ('常', "chang"), ('崩', "beng"), ('溃', "kui"),
        ('恢', "hui"), ('复', "fu"), ('重', "chong"),
        ('超', "chao"), ('时', "shi"), ('连', "lian"), ('接', "jie"),
        ('断', "duan"), ('开', "kai"), ('关', "guan"), ('闭', "bi"),
        ('打', "da"), ('开', "kai"), ('创', "chuang"), ('建', "jian"),
        ('删', "shan"), ('除', "chu"), ('更', "geng"), ('新', "xin"),
        ('查', "cha"), ('询', "xun"), ('搜', "sou"), ('索', "suo"),
        ('过', "guo"), ('滤', "lv"), ('排', "pai"), ('序', "xu"),
        ('分', "fen"), ('组', "zu"), ('合', "he"), ('并', "bing"),
        ('分', "fen"), ('割', "ge"), ('连', "lian"), ('接', "jie"),
        ('格', "ge"), ('式', "shi"), ('转', "zhuan"), ('换', "huan"),
        ('解', "jie"), ('析', "xi"), ('验', "yan"), ('证', "zheng"),
        ('校', "jiao"), ('验', "yan"), ('测', "ce"), ('试', "shi"),
        ('调', "tiao"), ('试', "shi"), ('日', "ri"), ('志', "zhi"),
        ('记', "ji"), ('录', "lu"), ('监', "jian"), ('控', "kong"),
        ('性', "xing"), ('能', "neng"), ('优', "you"), ('化', "hua"),
        ('安', "an"), ('全', "quan"), ('权', "quan"), ('限', "xian"),
        ('用', "yong"), ('户', "hu"), ('登', "deng"), ('录', "lu"),
        ('注', "zhu"), ('册', "ce"), ('密', "mi"), ('码', "ma"),
        ('认', "ren"), ('证', "zheng"), ('授', "shou"), ('权', "quan"),
        // 数字相关
        ('一', "yi"), ('二', "er"), ('三', "san"), ('四', "si"),
        ('五', "wu"), ('六', "liu"), ('七', "qi"), ('八', "ba"),
        ('九', "jiu"), ('十', "shi"), ('百', "bai"), ('千', "qian"),
        ('万', "wan"), ('亿', "yi"), ('元', "yuan"), ('角', "jiao"),
        ('分', "fen"), ('块', "kuai"), ('毛', "mao"), ('美', "mei"),
        ('金', "jin"), ('英', "ying"), ('镑', "bang"), ('欧', "ou"),
        ('洲', "zhou"), ('亚', "ya"), ('国', "guo"),
        ('家', "jia"), ('城', "cheng"), ('市', "shi"), ('镇', "zhen"),
        ('村', "cun"), ('路', "lu"), ('街', "jie"), ('区', "qu"),
        ('号', "hao"), ('室', "shi"), ('楼', "lou"), ('层', "ceng"),
        ('公', "gong"), ('司', "si"), ('部', "bu"), ('门', "men"),
        ('组', "zu"), ('团', "tuan"), ('队', "dui"), ('员', "yuan"),
        ('经', "jing"), ('理', "li"), ('总', "zong"), ('裁', "cai"),
        ('董', "dong"), ('事', "shi"), ('长', "zhang"), ('主', "zhu"),
        ('任', "ren"), ('领', "ling"), ('导', "dao"), ('技', "ji"),
        ('术', "shu"), ('产', "chan"), ('品', "pin"), ('服', "fu"),
        ('务', "wu"), ('项', "xiang"), ('目', "mu"), ('计', "ji"),
        ('划', "hua"), ('任', "ren"), ('务', "wu"), ('进', "jin"),
        ('度', "du"), ('状', "zhuang"), ('态', "tai"), ('等', "deng"),
        ('级', "ji"), ('类', "lei"), ('别', "bie"), ('标', "biao"),
        ('签', "qian"), ('附', "fu"), ('件', "jian"), ('图', "tu"),
        ('片', "pian"), ('视', "shi"), ('频', "pin"), ('音', "yin"),
        ('乐', "yue"), ('游', "you"), ('戏', "xi"), ('电', "dian"),
        ('影', "ying"), ('书', "shu"), ('籍', "ji"), ('文', "wen"),
        ('章', "zhang"), ('新', "xin"), ('闻', "wen"), ('广', "guang"),
        ('告', "gao"), ('推', "tui"), ('荐', "jian"), ('热', "re"),
        ('门', "men"), ('最', "zui"), ('新', "xin"), ('精', "jing"),
        ('选', "xuan"), ('优', "you"), ('秀', "xiu"), ('排', "pai"),
        ('行', "hang"), ('榜', "bang"), ('评', "ping"), ('论', "lun"),
        ('点', "dian"), ('赞', "zan"), ('收', "shou"), ('藏', "cang"),
        ('分', "fen"), ('享', "xiang"), ('转', "zhuan"), ('发', "fa"),
    ];
    
    pairs.into_iter().collect()
}

/// 便捷函数：使用默认配置生成 slug
pub fn slugify(input: &str) -> String {
    SlugGenerator::default().slugify(input)
}

/// 便捷函数：使用自定义分隔符生成 slug
pub fn slugify_with_separator(input: &str, separator: &str) -> String {
    let options = SlugOptions {
        separator: separator.to_string(),
        ..Default::default()
    };
    SlugGenerator::new(options).slugify(input)
}

/// 便捷函数：生成指定最大长度的 slug
pub fn slugify_with_max_length(input: &str, max_length: usize) -> String {
    let options = SlugOptions {
        max_length,
        ..Default::default()
    };
    SlugGenerator::new(options).slugify(input)
}

/// 便捷函数：从文件名生成 slug
pub fn slugify_filename(filename: &str) -> String {
    SlugGenerator::default().from_filename(filename)
}

/// 便捷函数：批量生成 slug
pub fn slugify_batch(inputs: &[&str]) -> Vec<String> {
    SlugGenerator::default().slugify_batch(inputs)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_slugify() {
        let gen = SlugGenerator::default();
        
        assert_eq!(gen.slugify("Hello World"), "hello-world");
        assert_eq!(gen.slugify("This is a Test"), "this-is-a-test");
        assert_eq!(gen.slugify("  Multiple   Spaces  "), "multiple-spaces");
    }

    #[test]
    fn test_special_characters() {
        let gen = SlugGenerator::default();
        
        assert_eq!(gen.slugify("Hello@World!"), "hello-world");
        assert_eq!(gen.slugify("Test#123$%^"), "test-123");  // 数字前会插入分隔符
        assert_eq!(gen.slugify("Under_Score-Text"), "under-score-text");
    }

    #[test]
    fn test_chinese_characters() {
        let gen = SlugGenerator::default();
        
        let result = gen.slugify("中文标题");
        assert!(!result.is_empty());
        assert!(result.contains("-") || result.len() > 0);
        
        let result2 = gen.slugify("测试开发");
        assert!(!result2.is_empty());
    }

    #[test]
    fn test_custom_separator() {
        let options = SlugOptions {
            separator: "_".to_string(),
            ..Default::default()
        };
        let gen = SlugGenerator::new(options);
        
        assert_eq!(gen.slugify("Hello World"), "hello_world");
        assert_eq!(gen.slugify("Test Case"), "test_case");
    }

    #[test]
    fn test_preserve_case() {
        let options = SlugOptions {
            lowercase: false,
            ..Default::default()
        };
        let gen = SlugGenerator::new(options);
        
        assert_eq!(gen.slugify("Hello World"), "Hello-World");
    }

    #[test]
    fn test_max_length() {
        let options = SlugOptions {
            max_length: 10,
            ..Default::default()
        };
        let gen = SlugGenerator::new(options);
        
        assert_eq!(gen.slugify("This is a very long string"), "this-is-a");
    }

    #[test]
    fn test_remove_stop_words() {
        let options = SlugOptions {
            remove_stop_words: true,
            ..Default::default()
        };
        let gen = SlugGenerator::new(options);
        
        let result = gen.slugify("The Quick Brown Fox");
        assert!(!result.contains("the"));
    }

    #[test]
    fn test_no_numbers() {
        let options = SlugOptions {
            keep_numbers: false,
            ..Default::default()
        };
        let gen = SlugGenerator::new(options);
        
        assert_eq!(gen.slugify("Test123Case456"), "test-case");
    }

    #[test]
    fn test_from_filename() {
        let gen = SlugGenerator::default();
        
        assert_eq!(gen.from_filename("My Document.pdf"), "my-document");
        assert_eq!(gen.from_filename("report_2024.xlsx"), "report-2024");
        assert_eq!(gen.from_filename("no_extension"), "no-extension");
    }

    #[test]
    fn test_batch_slugify() {
        let gen = SlugGenerator::default();
        let inputs = vec!["Hello World", "Test Case", "Example"];
        let results = gen.slugify_batch(&inputs);
        
        assert_eq!(results, vec!["hello-world", "test-case", "example"]);
    }

    #[test]
    fn test_unique_slug() {
        let gen = SlugGenerator::default();
        let existing = vec!["hello-world".to_string()];
        
        let result = gen.unique_slug("Hello World", &existing);
        assert_eq!(result, "hello-world-1");
        
        let existing2 = vec!["hello-world".to_string(), "hello-world-1".to_string()];
        let result2 = gen.unique_slug("Hello World", &existing2);
        assert_eq!(result2, "hello-world-2");
    }

    #[test]
    fn test_convenience_functions() {
        assert_eq!(slugify("Hello World"), "hello-world");
        assert_eq!(slugify_with_separator("Hello World", "_"), "hello_world");
        assert_eq!(slugify_filename("test file.txt"), "test-file");
        
        let batch = slugify_batch(&["A", "B C", "D E F"]);
        assert_eq!(batch, vec!["a", "b-c", "d-e-f"]);
    }

    #[test]
    fn test_edge_cases() {
        let gen = SlugGenerator::default();
        
        // 空字符串
        assert_eq!(gen.slugify(""), "");
        
        // 只有特殊字符
        assert_eq!(gen.slugify("@#$%^&*()"), "");
        
        // 只有分隔符
        assert_eq!(gen.slugify("---"), "");
        assert_eq!(gen.slugify("___"), "");
        
        // 连续分隔符
        assert_eq!(gen.slugify("a---b"), "a-b");
        
        // 首尾分隔符
        assert_eq!(gen.slugify("---hello---"), "hello");
    }

    #[test]
    fn test_mixed_content() {
        let gen = SlugGenerator::default();
        
        let result = gen.slugify("Hello 世界! This is 测试 2024");
        assert!(!result.is_empty());
        assert!(result.contains("hello"));
        assert!(result.contains("2024"));
    }
}