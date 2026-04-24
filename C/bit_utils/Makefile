# Makefile for bit_utils
# C 位操作工具库构建文件

CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -O2
SRCDIR = .
OUTDIR = .

# 目标文件
LIB_OBJ = bit_utils.o
TEST_BIN = test_bit_utils
EXAMPLES_BIN = examples_app

# 默认目标: 编译所有
all: $(LIB_OBJ) $(TEST_BIN) $(EXAMPLES_BIN)

# 编译库文件
$(LIB_OBJ): $(SRCDIR)/bit_utils.c $(SRCDIR)/bit_utils.h
	$(CC) $(CFLAGS) -c $(SRCDIR)/bit_utils.c -o $(OUTDIR)/bit_utils.o

# 编译并运行测试
test: $(TEST_BIN)
	./$(TEST_BIN)

$(TEST_BIN): $(SRCDIR)/test_bit_utils.c $(LIB_OBJ)
	$(CC) $(CFLAGS) $(SRCDIR)/test_bit_utils.c $(LIB_OBJ) -o $(OUTDIR)/$(TEST_BIN)

# 编译并运行示例
run-examples: $(EXAMPLES_BIN)
	./$(EXAMPLES_BIN)

# 仅编译示例
examples: $(EXAMPLES_BIN)

$(EXAMPLES_BIN): $(SRCDIR)/examples.c $(LIB_OBJ)
	$(CC) $(CFLAGS) $(SRCDIR)/examples.c $(LIB_OBJ) -o $(OUTDIR)/$(EXAMPLES_BIN)

# 仅编译测试
build-test: $(TEST_BIN)

# 清理
clean:
	rm -f $(LIB_OBJ) $(TEST_BIN) $(EXAMPLES_BIN)

# 重新构建
rebuild: clean all

.PHONY: all test run-examples examples build-test clean rebuild