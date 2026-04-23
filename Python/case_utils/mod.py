"""
Case Utils - 命名风格转换工具

支持多种命名风格之间的相互转换：
- camelCase (小驼峰)
- PascalCase (大驼峰)
- snake_case (蛇形)
- SCREAMING_SNAKE_CASE (尖叫蛇形)
- kebab-case (短横线)
- Title Case (标题格式)
- sentence case (句子格式)
- dot.case (点分隔)

零外部依赖，纯Python实现。
"""

import re
from typing import List, Optional, Tuple


class CaseUtils:
    """命名风格转换工具类"""
    
    # 分词正则表达式
    _WORD_PATTERN = re.compile(
        r'[A-Z]?[a-z]+|'       # 大写开头的单词或小写单词
        r'[A-Z]+(?=[A-Z][a-z])|'  # 连续大写（非最后）
        r'[A-Z]+|'              # 连续大写
        r'\d+|'                 # 数字
        r'[a-z]+'               # 小写单词
    )
    
    @staticmethod
    def split_words(text: str) -> List[str]:
        """
        将任意格式的字符串拆分为单词列表
        
        Args:
            text: 输入字符串
            
        Returns:
            单词列表
            
        Examples:
            >>> CaseUtils.split_words("helloWorld")
            ['hello', 'World']
            >>> CaseUtils.split_words("hello_world")
            ['hello', 'world']
            >>> CaseUtils.split_words("HelloWorld")
            ['Hello', 'World']
            >>> CaseUtils.split_words("HELLO_WORLD")
            ['HELLO', 'WORLD']
        """
        # 处理分隔符
        text = re.sub(r'[-_.\s]+', ' ', text)
        
        # 在大写字母前插入空格（驼峰转换）
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
        text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', text)
        
        # 在数字边界插入空格（数字与字母之间）
        text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
        text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)
        
        # 分割并过滤空字符串
        words = text.split()
        return [w for w in words if w]
    
    @staticmethod
    def to_camel_case(text: str) -> str:
        """
        转换为 camelCase (小驼峰)
        
        Args:
            text: 任意格式的字符串
            
        Returns:
            camelCase 格式字符串
            
        Examples:
            >>> CaseUtils.to_camel_case("hello_world")
            'helloWorld'
            >>> CaseUtils.to_camel_case("Hello-World")
            'helloWorld'
            >>> CaseUtils.to_camel_case("HELLO_WORLD")
            'helloWorld'
        """
        words = CaseUtils.split_words(text)
        if not words:
            return ""
        
        result = words[0].lower()
        for word in words[1:]:
            result += word.capitalize()
        return result
    
    @staticmethod
    def to_pascal_case(text: str) -> str:
        """
        转换为 PascalCase (大驼峰/帕斯卡命名)
        
        Args:
            text: 任意格式的字符串
            
        Returns:
            PascalCase 格式字符串
            
        Examples:
            >>> CaseUtils.to_pascal_case("hello_world")
            'HelloWorld'
            >>> CaseUtils.to_pascal_case("hello-world")
            'HelloWorld'
            >>> CaseUtils.to_pascal_case("HELLO_WORLD")
            'HelloWorld'
        """
        words = CaseUtils.split_words(text)
        if not words:
            return ""
        
        return "".join(word.capitalize() for word in words)
    
    @staticmethod
    def to_snake_case(text: str) -> str:
        """
        转换为 snake_case (蛇形命名)
        
        Args:
            text: 任意格式的字符串
            
        Returns:
            snake_case 格式字符串
            
        Examples:
            >>> CaseUtils.to_snake_case("helloWorld")
            'hello_world'
            >>> CaseUtils.to_snake_case("HelloWorld")
            'hello_world'
            >>> CaseUtils.to_snake_case("hello-world")
            'hello_world'
        """
        words = CaseUtils.split_words(text)
        if not words:
            return ""
        
        return "_".join(word.lower() for word in words)
    
    @staticmethod
    def to_screaming_snake_case(text: str) -> str:
        """
        转换为 SCREAMING_SNAKE_CASE (尖叫蛇形命名)
        
        Args:
            text: 任意格式的字符串
            
        Returns:
            SCREAMING_SNAKE_CASE 格式字符串
            
        Examples:
            >>> CaseUtils.to_screaming_snake_case("helloWorld")
            'HELLO_WORLD'
            >>> CaseUtils.to_screaming_snake_case("hello-world")
            'HELLO_WORLD'
            >>> CaseUtils.to_screaming_snake_case("HelloWorld")
            'HELLO_WORLD'
        """
        words = CaseUtils.split_words(text)
        if not words:
            return ""
        
        return "_".join(word.upper() for word in words)
    
    @staticmethod
    def to_kebab_case(text: str) -> str:
        """
        转换为 kebab-case (短横线命名)
        
        Args:
            text: 任意格式的字符串
            
        Returns:
            kebab-case 格式字符串
            
        Examples:
            >>> CaseUtils.to_kebab_case("helloWorld")
            'hello-world'
            >>> CaseUtils.to_kebab_case("hello_world")
            'hello-world'
            >>> CaseUtils.to_kebab_case("HelloWorld")
            'hello-world'
        """
        words = CaseUtils.split_words(text)
        if not words:
            return ""
        
        return "-".join(word.lower() for word in words)
    
    @staticmethod
    def to_train_case(text: str) -> str:
        """
        转换为 Train-Case (列车命名，每个单词首字母大写，用短横线连接)
        
        Args:
            text: 任意格式的字符串
            
        Returns:
            Train-Case 格式字符串
            
        Examples:
            >>> CaseUtils.to_train_case("helloWorld")
            'Hello-World'
            >>> CaseUtils.to_train_case("hello_world")
            'Hello-World'
        """
        words = CaseUtils.split_words(text)
        if not words:
            return ""
        
        return "-".join(word.capitalize() for word in words)
    
    @staticmethod
    def to_dot_case(text: str) -> str:
        """
        转换为 dot.case (点分隔命名)
        
        Args:
            text: 任意格式的字符串
            
        Returns:
            dot.case 格式字符串
            
        Examples:
            >>> CaseUtils.to_dot_case("helloWorld")
            'hello.world'
            >>> CaseUtils.to_dot_case("hello_world")
            'hello.world'
        """
        words = CaseUtils.split_words(text)
        if not words:
            return ""
        
        return ".".join(word.lower() for word in words)
    
    @staticmethod
    def to_title_case(text: str) -> str:
        """
        转换为 Title Case (标题格式，每个单词首字母大写)
        
        Args:
            text: 任意格式的字符串
            
        Returns:
            Title Case 格式字符串
            
        Examples:
            >>> CaseUtils.to_title_case("helloWorld")
            'Hello World'
            >>> CaseUtils.to_title_case("hello_world")
            'Hello World'
        """
        words = CaseUtils.split_words(text)
        if not words:
            return ""
        
        return " ".join(word.capitalize() for word in words)
    
    @staticmethod
    def to_sentence_case(text: str) -> str:
        """
        转换为 Sentence case (句子格式，只有第一个单词首字母大写)
        
        Args:
            text: 任意格式的字符串
            
        Returns:
            Sentence case 格式字符串
            
        Examples:
            >>> CaseUtils.to_sentence_case("helloWorld")
            'Hello world'
            >>> CaseUtils.to_sentence_case("HELLO_WORLD")
            'Hello world'
        """
        words = CaseUtils.split_words(text)
        if not words:
            return ""
        
        result = [words[0].capitalize()]
        result.extend(word.lower() for word in words[1:])
        return " ".join(result)
    
    @staticmethod
    def to_path_case(text: str) -> str:
        """
        转换为 path/case (路径分隔命名)
        
        Args:
            text: 任意格式的字符串
            
        Returns:
            path/case 格式字符串
            
        Examples:
            >>> CaseUtils.to_path_case("helloWorld")
            'hello/world'
            >>> CaseUtils.to_path_case("hello_world")
            'hello/world'
        """
        words = CaseUtils.split_words(text)
        if not words:
            return ""
        
        return "/".join(word.lower() for word in words)
    
    @staticmethod
    def to_constant_case(text: str) -> str:
        """
        转换为 CONSTANT_CASE (常量命名，同 SCREAMING_SNAKE_CASE)
        
        Args:
            text: 任意格式的字符串
            
        Returns:
            CONSTANT_CASE 格式字符串
        """
        return CaseUtils.to_screaming_snake_case(text)
    
    @staticmethod
    def detect_case(text: str) -> Optional[str]:
        """
        检测字符串的命名风格
        
        Args:
            text: 输入字符串
            
        Returns:
            检测到的命名风格，可选值：
            - 'camel' (camelCase)
            - 'pascal' (PascalCase)
            - 'snake' (snake_case)
            - 'screaming_snake' (SCREAMING_SNAKE_CASE)
            - 'kebab' (kebab-case)
            - 'train' (Train-Case)
            - 'dot' (dot.case)
            - 'title' (Title Case)
            - 'unknown' (无法识别)
            
        Examples:
            >>> CaseUtils.detect_case("helloWorld")
            'camel'
            >>> CaseUtils.detect_case("HelloWorld")
            'pascal'
            >>> CaseUtils.detect_case("hello_world")
            'snake'
        """
        if not text:
            return None
        
        # 检测点分隔
        if '.' in text:
            parts = text.split('.')
            if all(p.islower() for p in parts):
                return 'dot'
        
        # 检测短横线
        if '-' in text:
            parts = text.split('-')
            if all(p.islower() for p in parts):
                return 'kebab'
            if all(p.istitle() for p in parts):
                return 'train'
        
        # 检测下划线
        if '_' in text:
            parts = text.split('_')
            if all(p.islower() for p in parts):
                return 'snake'
            if all(p.isupper() for p in parts):
                return 'screaming_snake'
        
        # 检测空格（标题格式）
        if ' ' in text:
            parts = text.split()
            if all(p.istitle() for p in parts):
                return 'title'
        
        # 检测驼峰
        if text[0].islower() and any(c.isupper() for c in text):
            return 'camel'
        
        if text[0].isupper() and any(c.islower() for c in text):
            # 检查是否是帕斯卡命名
            has_lower_after_upper = False
            for i, c in enumerate(text):
                if c.isupper() and i > 0:
                    if text[i-1].islower():
                        has_lower_after_upper = True
                        break
            if has_lower_after_upper or any(c.isupper() for c in text[1:]):
                return 'pascal'
        
        return 'unknown'
    
    @staticmethod
    def convert(text: str, target_case: str) -> str:
        """
        将字符串转换为指定的命名风格
        
        Args:
            text: 输入字符串
            target_case: 目标命名风格，可选值：
                - 'camel' / 'camelCase'
                - 'pascal' / 'PascalCase'
                - 'snake' / 'snake_case'
                - 'screaming_snake' / 'SCREAMING_SNAKE_CASE'
                - 'kebab' / 'kebab-case'
                - 'train' / 'Train-Case'
                - 'dot' / 'dot.case'
                - 'title' / 'Title Case'
                - 'sentence' / 'Sentence case'
                - 'path' / 'path/case'
                - 'constant' / 'CONSTANT_CASE'
                
        Returns:
            转换后的字符串
            
        Raises:
            ValueError: 不支持的命名风格
            
        Examples:
            >>> CaseUtils.convert("hello_world", "camel")
            'helloWorld'
            >>> CaseUtils.convert("helloWorld", "snake")
            'hello_world'
        """
        case_mapping = {
            'camel': CaseUtils.to_camel_case,
            'camelCase': CaseUtils.to_camel_case,
            'pascal': CaseUtils.to_pascal_case,
            'PascalCase': CaseUtils.to_pascal_case,
            'snake': CaseUtils.to_snake_case,
            'snake_case': CaseUtils.to_snake_case,
            'screaming_snake': CaseUtils.to_screaming_snake_case,
            'SCREAMING_SNAKE_CASE': CaseUtils.to_screaming_snake_case,
            'kebab': CaseUtils.to_kebab_case,
            'kebab-case': CaseUtils.to_kebab_case,
            'train': CaseUtils.to_train_case,
            'Train-Case': CaseUtils.to_train_case,
            'dot': CaseUtils.to_dot_case,
            'dot.case': CaseUtils.to_dot_case,
            'title': CaseUtils.to_title_case,
            'Title Case': CaseUtils.to_title_case,
            'sentence': CaseUtils.to_sentence_case,
            'Sentence case': CaseUtils.to_sentence_case,
            'path': CaseUtils.to_path_case,
            'path/case': CaseUtils.to_path_case,
            'constant': CaseUtils.to_constant_case,
            'CONSTANT_CASE': CaseUtils.to_constant_case,
        }
        
        target_case_lower = target_case.lower()
        
        # 先尝试完全匹配
        if target_case in case_mapping:
            return case_mapping[target_case](text)
        
        # 再尝试小写匹配
        for key, converter in case_mapping.items():
            if key.lower() == target_case_lower:
                return converter(text)
        
        raise ValueError(f"不支持的命名风格: {target_case}. 支持的风格: {', '.join(sorted(set(case_mapping.keys())))}")
    
    @staticmethod
    def convert_all(text: str) -> dict:
        """
        将字符串转换为所有支持的命名风格
        
        Args:
            text: 输入字符串
            
        Returns:
            包含所有转换结果的字典
            
        Examples:
            >>> result = CaseUtils.convert_all("helloWorld")
            >>> result['snake_case']
            'hello_world'
        """
        return {
            'camelCase': CaseUtils.to_camel_case(text),
            'PascalCase': CaseUtils.to_pascal_case(text),
            'snake_case': CaseUtils.to_snake_case(text),
            'SCREAMING_SNAKE_CASE': CaseUtils.to_screaming_snake_case(text),
            'kebab-case': CaseUtils.to_kebab_case(text),
            'Train-Case': CaseUtils.to_train_case(text),
            'dot.case': CaseUtils.to_dot_case(text),
            'Title Case': CaseUtils.to_title_case(text),
            'Sentence case': CaseUtils.to_sentence_case(text),
            'path/case': CaseUtils.to_path_case(text),
        }
    
    @staticmethod
    def is_valid_identifier(text: str, case_type: str) -> bool:
        """
        检查字符串是否符合指定的命名风格
        
        Args:
            text: 输入字符串
            case_type: 命名风格类型
            
        Returns:
            是否符合指定风格
            
        Examples:
            >>> CaseUtils.is_valid_identifier("helloWorld", "camel")
            True
            >>> CaseUtils.is_valid_identifier("hello_world", "camel")
            False
        """
        detected = CaseUtils.detect_case(text)
        if detected == 'unknown':
            return False
        
        # 映射别名
        case_aliases = {
            'camel': ['camel'],
            'pascal': ['pascal'],
            'snake': ['snake'],
            'screaming_snake': ['screaming_snake', 'constant'],
            'kebab': ['kebab'],
            'train': ['train'],
            'dot': ['dot'],
            'title': ['title'],
        }
        
        case_type_lower = case_type.lower()
        for key, aliases in case_aliases.items():
            if case_type_lower in aliases or case_type_lower == key:
                return detected == key
        
        return False
    
    @staticmethod
    def batch_convert(texts: List[str], target_case: str) -> List[str]:
        """
        批量转换字符串
        
        Args:
            texts: 字符串列表
            target_case: 目标命名风格
            
        Returns:
            转换后的字符串列表
            
        Examples:
            >>> CaseUtils.batch_convert(["hello_world", "fooBar"], "camel")
            ['helloWorld', 'fooBar']
        """
        return [CaseUtils.convert(text, target_case) for text in texts]
    
    @staticmethod
    def to_plural_snake(text: str) -> str:
        """
        转换为复数 snake_case（简单实现，适用于大多数情况）
        
        Args:
            text: 输入字符串
            
        Returns:
            复数 snake_case 格式字符串
            
        Examples:
            >>> CaseUtils.to_plural_snake("userAccount")
            'user_accounts'
        """
        snake = CaseUtils.to_snake_case(text)
        if not snake:
            return ""
        
        # 简单的复数规则
        if snake.endswith('y') and len(snake) > 1 and snake[-2] not in 'aeiou':
            return snake[:-1] + 'ies'
        elif snake.endswith(('s', 'x', 'z', 'ch', 'sh')):
            return snake + 'es'
        else:
            return snake + 's'


# 便捷函数（模块级别）
def to_camel_case(text: str) -> str:
    """转换为 camelCase"""
    return CaseUtils.to_camel_case(text)


def to_pascal_case(text: str) -> str:
    """转换为 PascalCase"""
    return CaseUtils.to_pascal_case(text)


def to_snake_case(text: str) -> str:
    """转换为 snake_case"""
    return CaseUtils.to_snake_case(text)


def to_kebab_case(text: str) -> str:
    """转换为 kebab-case"""
    return CaseUtils.to_kebab_case(text)


def detect_case(text: str) -> Optional[str]:
    """检测命名风格"""
    return CaseUtils.detect_case(text)


def convert_case(text: str, target_case: str) -> str:
    """转换为指定命名风格"""
    return CaseUtils.convert(text, target_case)


if __name__ == "__main__":
    # 演示用法
    test_strings = [
        "helloWorld",
        "HelloWorld",
        "hello_world",
        "HELLO_WORLD",
        "hello-world",
        "hello.world",
        "Hello World",
    ]
    
    print("=" * 60)
    print("Case Utils - 命名风格转换工具演示")
    print("=" * 60)
    
    for s in test_strings:
        print(f"\n输入: {s!r}")
        print(f"  检测风格: {CaseUtils.detect_case(s)}")
        print(f"  camelCase: {CaseUtils.to_camel_case(s)}")
        print(f"  PascalCase: {CaseUtils.to_pascal_case(s)}")
        print(f"  snake_case: {CaseUtils.to_snake_case(s)}")
        print(f"  SCREAMING_SNAKE: {CaseUtils.to_screaming_snake_case(s)}")
        print(f"  kebab-case: {CaseUtils.to_kebab_case(s)}")
        print(f"  Train-Case: {CaseUtils.to_train_case(s)}")
        print(f"  dot.case: {CaseUtils.to_dot_case(s)}")
        print(f"  Title Case: {CaseUtils.to_title_case(s)}")
    
    print("\n" + "=" * 60)
    print("convert_all() 示例:")
    result = CaseUtils.convert_all("helloWorld")
    for case_type, value in result.items():
        print(f"  {case_type}: {value}")