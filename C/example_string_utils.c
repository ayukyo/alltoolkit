/**
 * @file example_string_utils.c
 * @brief string_utils.h 使用示例
 * @author AllToolkit
 * @version 1.0.0
 * @date 2026-04-02
 *
 * 编译命令: gcc -o example_string_utils example_string_utils.c string_utils.c
 * 运行命令: ./example_string_utils
 */

#include <stdio.h>
#include <string.h>
#include "string_utils.h"

int main(void) {
    printf("=== AllToolkit C String Utils Demo ===\n\n");
    
    // 1. str_trim 示例
    printf("1. str_trim - 去除首尾空白\n");
    char trim_test[] = "   Hello World   ";
    printf("   原始: \"%s\"\n", trim_test);
    str_trim(trim_test);
    printf("   结果: \"%s\"\n\n", trim_test);
    
    // 2. str_to_lower / str_to_upper 示例
    printf("2. str_to_lower / str_to_upper - 大小写转换\n");
    char case_test[] = "Hello World";
    printf("   原始: \"%s\"\n", case_test);
    str_to_lower(case_test);
    printf("   小写: \"%s\"\n", case_test);
    strcpy(case_test, "Hello World");
    str_to_upper(case_test);
    printf("   大写: \"%s\"\n\n", case_test);
    
    // 3. str_reverse 示例
    printf("3. str_reverse - 字符串反转\n");
    char reverse_test[] = "Hello";
    printf("   原始: \"%s\"\n", reverse_test);
    str_reverse(reverse_test);
    printf("   反转: \"%s\"\n\n", reverse_test);
    
    // 4. str_starts_with / str_ends_with 示例
    printf("4. str_starts_with / str_ends_with - 前缀后缀检查\n");
    const char* check_str = "HelloWorld.txt";
    printf("   字符串: \"%s\"\n", check_str);
    printf("   以 \"Hello\" 开头: %s\n", str_starts_with(check_str, "Hello") ? "true" : "false");
    printf("   以 \"World\" 开头: %s\n", str_starts_with(check_str, "World") ? "true" : "false");
    printf("   以 \".txt\" 结尾: %s\n", str_ends_with(check_str, ".txt") ? "true" : "false");
    printf("   以 \".pdf\" 结尾: %s\n\n", str_ends_with(check_str, ".pdf") ? "true" : "false");
    
    // 5. str_count 示例
    printf("5. str_count - 子串计数\n");
    const char* count_str = "abababababa";
    printf("   字符串: \"%s\"\n", count_str);
    printf("   \"aba\" 出现次数: %zu\n", str_count(count_str, "aba"));
    printf("   \"ab\" 出现次数: %zu\n\n", str_count(count_str, "ab"));
    
    // 6. str_copy_safe 示例
    printf("6. str_copy_safe - 安全字符串复制\n");
    char dest[20];
    const char* long_src = "This is a very long string";
    size_t copied = str_copy_safe(dest, long_src, sizeof(dest));
    printf("   源字符串: \"%s\"\n", long_src);
    printf("   目标大小: %zu\n", sizeof(dest));
    printf("   复制结果: \"%s\"\n", dest);
    printf("   实际复制: %zu 字符\n\n", copied);
    
    // 7. 组合使用示例
    printf("7. 组合使用示例\n");
    char combo[] = "  USER@EXAMPLE.COM  ";
    printf("   原始: \"%s\"\n", combo);
    str_trim(combo);
    str_to_lower(combo);
    printf("   处理后: \"%s\"\n", combo);
    printf("   是邮箱格式: %s\n", str_ends_with(combo, ".com") ? "可能" : "否");
    
    printf("\n=== Demo Complete ===\n");
    return 0;
}
