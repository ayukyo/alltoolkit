/**
 * @file example.c
 * @brief string_utils 使用示例
 */

#include <stdio.h>
#include <stdlib.h>
#include "string_utils.h"

int main() {
    printf("=== C String Utils Example ===\n\n");
    
    /* Trim Example */
    printf("1. Trim:\n");
    char s1[] = "  hello world  ";
    printf("   Original: \"%s\"\n", s1);
    str_trim(s1);
    printf("   Trimmed:  \"%s\"\n\n", s1);
    
    /* Split Example */
    printf("2. Split:\n");
    StringSplitResult result = str_split("apple,banana,cherry", ",", 0);
    printf("   Splitting 'apple,banana,cherry' by ',':\n");
    for (size_t i = 0; i < result.count; i++) {
        printf("   [%zu]: %s\n", i, result.tokens[i]);
    }
    str_split_free(&result);
    printf("\n");
    
    /* Replace Example */
    printf("3. Replace:\n");
    char* replaced = str_replace("hello world", "world", "C");
    printf("   'hello world' -> replace 'world' with 'C':\n");
    printf("   Result: %s\n\n", replaced);
    free(replaced);
    
    /* Case Conversion */
    printf("4. Case Conversion:\n");
    char* upper = str_to_upper_copy("hello");
    char* lower = str_to_lower_copy("WORLD");
    printf("   to_upper('hello') = %s\n", upper);
    printf("   to_lower('WORLD') = %s\n\n", lower);
    free(upper);
    free(lower);
    
    /* Validation */
    printf("5. Validation:\n");
    printf("   is_numeric('12345') = %s\n", str_is_numeric("12345") ? "true" : "false");
    printf("   is_integer('-42') = %s\n", str_is_integer("-42") ? "true" : "false");
    printf("   is_float('3.14') = %s\n", str_is_float("3.14") ? "true" : "false");
    printf("   is_alpha('hello') = %s\n", str_is_alpha("hello") ? "true" : "false");
    printf("   is_blank('   ') = %s\n\n", str_is_blank("   ") ? "true" : "false");
    
    /* Substring */
    printf("6. Substring:\n");
    char* sub = str_substring("hello world", 6, 5);
    printf("   substring('hello world', 6, 5) = %s\n\n", sub);
    free(sub);
    
    /* Join */
    printf("7. Join:\n");
    const char* parts[] = {"2024", "04", "04"};
    char* joined = str_join_array(parts, 3, "-");
    printf("   join(['2024', '04', '04'], '-') = %s\n\n", joined);
    free(joined);
    
    /* Repeat */
    printf("8. Repeat:\n");
    char* repeated = str_repeat("ha", 3);
    printf("   repeat('ha', 3) = %s\n\n", repeated);
    free(repeated);
    
    printf("=== End of Example ===\n");
    return 0;
}
