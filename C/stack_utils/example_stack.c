/**
 * @file example_stack.c
 * @brief Usage examples for Stack Data Structure
 * 
 * @author AllToolkit
 * @date 2026-04-22
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "stack.h"

/* Example 1: Basic integer stack operations */
void example_basic_int_stack(void) {
    printf("=== Example 1: Basic Integer Stack ===\n\n");
    
    /* Create a stack for integers */
    Stack *stack = stack_create_int();
    
    printf("Creating integer stack...\n");
    printf("Stack size: %zu\n", stack_size(stack));
    printf("Stack is empty: %s\n\n", stack_is_empty(stack) ? "yes" : "no");
    
    /* Push elements */
    printf("Pushing elements: 10, 20, 30, 40, 50\n");
    stack_push_int(stack, 10);
    stack_push_int(stack, 20);
    stack_push_int(stack, 30);
    stack_push_int(stack, 40);
    stack_push_int(stack, 50);
    
    printf("Stack size: %zu\n", stack_size(stack));
    printf("Stack is empty: %s\n\n", stack_is_empty(stack) ? "yes" : "no");
    
    /* Peek at top */
    int top;
    stack_peek_int(stack, &top);
    printf("Top element (peek): %d\n\n", top);
    
    /* Pop all elements (LIFO order) */
    printf("Popping all elements:\n");
    while (!stack_is_empty(stack)) {
        int val;
        stack_pop_int(stack, &val);
        printf("  Popped: %d\n", val);
    }
    
    printf("\nStack size after popping all: %zu\n\n", stack_size(stack));
    
    stack_free(&stack);
}

/* Example 2: String reversal using stack */
void example_string_reversal(void) {
    printf("=== Example 2: String Reversal ===\n\n");
    
    const char *original = "Hello, World!";
    printf("Original string: %s\n", original);
    
    Stack *stack = stack_create_char();
    
    /* Push each character */
    for (size_t i = 0; original[i] != '\0'; i++) {
        stack_push_char(stack, original[i]);
    }
    
    /* Pop into reversed string */
    char reversed[64];
    size_t idx = 0;
    while (!stack_is_empty(stack)) {
        stack_pop_char(stack, &reversed[idx++]);
    }
    reversed[idx] = '\0';
    
    printf("Reversed string: %s\n\n", reversed);
    
    stack_free(&stack);
}

/* Example 3: Expression evaluation (bracket matching) */
bool check_balanced_brackets(const char *expr) {
    Stack *stack = stack_create_char();
    
    for (size_t i = 0; expr[i] != '\0'; i++) {
        char c = expr[i];
        
        if (c == '(' || c == '[' || c == '{') {
            stack_push_char(stack, c);
        } else if (c == ')' || c == ']' || c == '}') {
            if (stack_is_empty(stack)) {
                stack_free(&stack);
                return false;
            }
            
            char top;
            stack_pop_char(stack, &top);
            
            if ((c == ')' && top != '(') ||
                (c == ']' && top != '[') ||
                (c == '}' && top != '{')) {
                stack_free(&stack);
                return false;
            }
        }
    }
    
    bool balanced = stack_is_empty(stack);
    stack_free(&stack);
    return balanced;
}

void example_bracket_matching(void) {
    printf("=== Example 3: Bracket Matching ===\n\n");
    
    const char *expressions[] = {
        "((a + b) * c)",
        "{[()]}",
        "([)]",
        "(((",
        "x + (y - z) * [w / {u + v}]",
        NULL
    };
    
    for (int i = 0; expressions[i] != NULL; i++) {
        bool balanced = check_balanced_brackets(expressions[i]);
        printf("  \"%s\" -> %s\n", expressions[i], 
               balanced ? "Balanced ✓" : "Not balanced ✗");
    }
    
    printf("\n");
}

/* Example 4: Custom struct stack */
typedef struct {
    int id;
    char name[32];
    double score;
} Student;

void example_struct_stack(void) {
    printf("=== Example 4: Custom Struct Stack ===\n\n");
    
    Stack *stack = stack_create(sizeof(Student), 0);
    
    Student students[] = {
        {1, "Alice", 95.5},
        {2, "Bob", 87.3},
        {3, "Charlie", 92.1},
        {4, "Diana", 88.9}
    };
    
    printf("Pushing students onto stack:\n");
    for (int i = 0; i < 4; i++) {
        stack_push(stack, &students[i]);
        printf("  Pushed: #%d %s (%.1f)\n", 
               students[i].id, students[i].name, students[i].score);
    }
    
    printf("\nPopping students (LIFO order):\n");
    while (!stack_is_empty(stack)) {
        Student s;
        stack_pop(stack, &s);
        printf("  Popped: #%d %s (%.1f)\n", s.id, s.name, s.score);
    }
    
    printf("\n");
    stack_free(&stack);
}

/* Example 5: Stack operations - copy, reverse, at */
void example_stack_operations(void) {
    printf("=== Example 5: Stack Operations ===\n\n");
    
    Stack *stack = stack_create_int();
    
    /* Push elements */
    for (int i = 1; i <= 5; i++) {
        stack_push_int(stack, i * 10);
    }
    
    printf("Original stack: 10, 20, 30, 40, 50 (50 on top)\n");
    printf("Stack size: %zu\n\n", stack_size(stack));
    
    /* Access by index from top */
    printf("Access by index (from top):\n");
    for (size_t i = 0; i < stack_size(stack); i++) {
        int val;
        stack_at(stack, i, &val);
        printf("  Index %zu: %d\n", i, val);
    }
    printf("\n");
    
    /* Copy stack */
    Stack *copy = stack_copy(stack);
    printf("Created a copy of the stack\n");
    printf("Copy size: %zu\n\n", stack_size(copy));
    
    /* Reverse stack */
    stack_reverse(stack);
    printf("Reversed the original stack\n");
    printf("Reversed stack (top to bottom):\n");
    while (!stack_is_empty(stack)) {
        int val;
        stack_pop_int(stack, &val);
        printf("  %d\n", val);
    }
    printf("\n");
    
    printf("Copy still intact (top to bottom):\n");
    while (!stack_is_empty(copy)) {
        int val;
        stack_pop_int(copy, &val);
        printf("  %d\n", val);
    }
    printf("\n");
    
    stack_free(&stack);
    stack_free(&copy);
}

/* Example 6: Memory management - reserve and shrink */
void example_memory_management(void) {
    printf("=== Example 6: Memory Management ===\n\n");
    
    Stack *stack = stack_create_int();
    
    printf("Initial capacity: %zu\n", stack_capacity(stack));
    
    /* Reserve capacity */
    stack_reserve(stack, 1000);
    printf("After reserve(1000): %zu\n", stack_capacity(stack));
    
    /* Push some elements */
    for (int i = 0; i < 100; i++) {
        stack_push_int(stack, i);
    }
    printf("After pushing 100 elements:\n");
    printf("  Size: %zu\n", stack_size(stack));
    printf("  Capacity: %zu\n\n", stack_capacity(stack));
    
    /* Shrink to fit */
    stack_shrink_to_fit(stack);
    printf("After shrink_to_fit:\n");
    printf("  Size: %zu\n", stack_size(stack));
    printf("  Capacity: %zu\n\n", stack_capacity(stack));
    
    stack_free(&stack);
}

/* Example 7: Undo system simulation */
typedef enum {
    ACTION_INSERT,
    ACTION_DELETE,
    ACTION_REPLACE
} ActionType;

typedef struct {
    ActionType type;
    char data[64];
    int position;
} Action;

void example_undo_system(void) {
    printf("=== Example 7: Undo System Simulation ===\n\n");
    
    Stack *undo_stack = stack_create(sizeof(Action), 0);
    
    /* Simulate some actions */
    Action actions[] = {
        {ACTION_INSERT, "Hello", 0},
        {ACTION_DELETE, "World", 5},
        {ACTION_REPLACE, "OpenClaw", 0},
    };
    
    printf("Performing actions:\n");
    for (int i = 0; i < 3; i++) {
        stack_push(undo_stack, &actions[i]);
        const char *type_str[] = {"INSERT", "DELETE", "REPLACE"};
        printf("  Action %d: %s \"%s\" at position %d\n", 
               i + 1, type_str[actions[i].type], actions[i].data, actions[i].position);
    }
    
    printf("\nUndoing actions:\n");
    while (!stack_is_empty(undo_stack)) {
        Action action;
        stack_pop(undo_stack, &action);
        const char *type_str[] = {"INSERT", "DELETE", "REPLACE"};
        printf("  Undo: %s \"%s\" at position %d\n", 
               type_str[action.type], action.data, action.position);
    }
    
    printf("\n");
    stack_free(&undo_stack);
}

int main(void) {
    printf("\n");
    printf("╔════════════════════════════════════════════════════════╗\n");
    printf("║           Stack Utils - Usage Examples                 ║\n");
    printf("║                   AllToolkit v1.0                      ║\n");
    printf("╚════════════════════════════════════════════════════════╝\n\n");
    
    example_basic_int_stack();
    example_string_reversal();
    example_bracket_matching();
    example_struct_stack();
    example_stack_operations();
    example_memory_management();
    example_undo_system();
    
    printf("All examples completed successfully!\n\n");
    
    return 0;
}