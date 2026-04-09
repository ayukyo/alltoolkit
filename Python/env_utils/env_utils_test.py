# -*- coding: utf-8 -*-
"""
AllToolkit - Environment Utilities 测试套件

测试所有环境工具函数的功能。
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import *


# =============================================================================
# 测试工具函数
# =============================================================================

def print_section(title: str):
    """打印测试章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def print_test(name: str, passed: bool, details: str = ''):
    """打印测试结果"""
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"  {status}: {name}")
    if details:
        print(f"         {details}")
    return passed


def cleanup_env(names: List[str]):
    """清理测试环境变量"""
    for name in names:
        if name in os.environ:
            del os.environ[name]


# =============================================================================
# 测试用例
# =============================================================================

def test_basic_operations():
    """测试基本操作"""
    print_section("测试基本操作")
    
    all_passed = True
    test_vars = ['TEST_VAR', 'TEST_VAR2', 'TEST_REQUIRED']
    
    try:
        # 清理测试变量
        cleanup_env(test_vars)
        
        # 测试 has_env
        passed = not has_env('TEST_VAR')
        all_passed &= print_test("检查变量不存在", passed)
        
        # 测试 set_env
        passed = set_env('TEST_VAR', 'test_value')
        all_passed &= print_test("设置环境变量", passed)
        
        # 测试 get_env
        value = get_env('TEST_VAR')
        passed = value == 'test_value'
        all_passed &= print_test("获取环境变量", passed, f"值：{value}")
        
        # 测试 get_env with default
        value = get_env('NONEXISTENT', default='default_value')
        passed = value == 'default_value'
        all_passed &= print_test("获取环境变量（带默认值）", passed, f"值：{value}")
        
        # 测试 get_env required
        try:
            get_env('TEST_REQUIRED', required=True)
            passed = False
        except EnvironmentError:
            passed = True
        all_passed &= print_test("获取环境变量（必需）", passed)
        
        # 测试 delete_env
        passed = delete_env('TEST_VAR')
        all_passed &= print_test("删除环境变量", passed)
        
        passed = not has_env('TEST_VAR')
        all_passed &= print_test("验证已删除", passed)
        
        # 测试 get_all_env
        env = get_all_env()
        passed = 'PATH' in env or 'HOME' in env
        all_passed &= print_test("获取所有环境变量", passed, f"数量：{len(env)}")
        
    finally:
        cleanup_env(test_vars)
    
    return all_passed


def test_type_conversion():
    """测试类型转换"""
    print_section("测试类型转换")
    
    all_passed = True
    test_vars = ['TEST_INT', 'TEST_FLOAT', 'TEST_BOOL', 'TEST_LIST', 'TEST_JSON']
    
    try:
        # 测试整数转换
        os.environ['TEST_INT'] = '42'
        value = get_env_as('TEST_INT', VarType.INTEGER)
        passed = value == 42 and isinstance(value, int)
        all_passed &= print_test("整数转换", passed, f"值：{value}, 类型：{type(value).__name__}")
        
        # 测试浮点数转换
        os.environ['TEST_FLOAT'] = '3.14'
        value = get_env_as('TEST_FLOAT', VarType.FLOAT)
        passed = abs(value - 3.14) < 0.001
        all_passed &= print_test("浮点数转换", passed, f"值：{value}")
        
        # 测试布尔转换
        os.environ['TEST_BOOL'] = 'true'
        value = get_env_as('TEST_BOOL', VarType.BOOLEAN)
        passed = value == True
        all_passed &= print_test("布尔转换（true）", passed, f"值：{value}")
        
        os.environ['TEST_BOOL'] = 'false'
        value = get_env_as('TEST_BOOL', VarType.BOOLEAN)
        passed = value == False
        all_passed &= print_test("布尔转换（false）", passed, f"值：{value}")
        
        os.environ['TEST_BOOL'] = '1'
        value = get_env_as('TEST_BOOL', VarType.BOOLEAN)
        passed = value == True
        all_passed &= print_test("布尔转换（1）", passed, f"值：{value}")
        
        # 测试列表转换
        os.environ['TEST_LIST'] = 'a,b,c'
        value = get_env_as('TEST_LIST', VarType.LIST)
        passed = value == ['a', 'b', 'c']
        all_passed &= print_test("列表转换（逗号）", passed, f"值：{value}")
        
        os.environ['TEST_LIST'] = '[x;y;z]'
        value = get_env_as('TEST_LIST', VarType.LIST)
        passed = value == ['x', 'y', 'z']
        all_passed &= print_test("列表转换（分号）", passed, f"值：{value}")
        
        # 测试 JSON 转换
        os.environ['TEST_JSON'] = '{"key": "value", "num": 123}'
        value = get_env_as('TEST_JSON', VarType.JSON)
        passed = isinstance(value, dict) and value.get('key') == 'value'
        all_passed &= print_test("JSON 转换", passed, f"值：{value}")
        
    finally:
        cleanup_env(test_vars)
    
    return all_passed


def test_env_file_operations():
    """测试 .env 文件操作"""
    print_section("测试 .env 文件操作")
    
    all_passed = True
    temp_files = []
    
    try:
        # 创建测试 .env 文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write("# 测试配置文件\n")
            f.write("DATABASE_URL=postgres://localhost/mydb\n")
            f.write("DEBUG=true\n")
            f.write("PORT=8080\n")
            f.write('SECRET_KEY="super-secret-key-123"\n')
            f.write("EMPTY_VAR=\n")
            temp_env_file = f.name
            temp_files.append(temp_env_file)
        
        # 测试 parse_env_file
        env_vars = parse_env_file(temp_env_file)
        passed = len(env_vars) == 5
        all_passed &= print_test("解析 .env 文件", passed, f"变量数：{len(env_vars)}")
        
        passed = env_vars.get('DATABASE_URL') == 'postgres://localhost/mydb'
        all_passed &= print_test("解析 URL 值", passed, f"值：{env_vars.get('DATABASE_URL')}")
        
        passed = env_vars.get('SECRET_KEY') == 'super-secret-key-123'
        all_passed &= print_test("解析带引号的值", passed, f"值：{env_vars.get('SECRET_KEY')}")
        
        # 测试 load_env_file
        cleanup_env(['DATABASE_URL', 'DEBUG', 'PORT', 'SECRET_KEY'])
        loaded = load_env_file(temp_env_file)
        passed = os.environ.get('DATABASE_URL') == 'postgres://localhost/mydb'
        all_passed &= print_test("加载 .env 文件", passed)
        
        # 测试 save_env_file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            temp_output = f.name
            temp_files.append(temp_output)
        
        count = save_env_file(temp_output, {'TEST_A': 'value_a', 'TEST_B': 'value_b'})
        passed = count == 2
        all_passed &= print_test("保存 .env 文件", passed, f"保存数：{count}")
        
        # 验证保存的内容
        saved = parse_env_file(temp_output)
        passed = saved.get('TEST_A') == 'value_a'
        all_passed &= print_test("验证保存内容", passed)
        
        # 测试 merge_env_files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f1:
            f1.write("VAR1=value1\nVAR2=value2\n")
            temp1 = f1.name
            temp_files.append(temp1)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f2:
            f2.write("VAR2=overridden\nVAR3=value3\n")
            temp2 = f2.name
            temp_files.append(temp2)
        
        merged = merge_env_files([temp1, temp2])
        passed = merged.get('VAR1') == 'value1' and merged.get('VAR2') == 'overridden'
        all_passed &= print_test("合并 .env 文件", passed, f"VAR2: {merged.get('VAR2')}")
        
    finally:
        # 清理临时文件
        for filepath in temp_files:
            try:
                os.unlink(filepath)
            except:
                pass
        cleanup_env(['DATABASE_URL', 'DEBUG', 'PORT', 'SECRET_KEY', 'TEST_A', 'TEST_B', 'VAR1', 'VAR2', 'VAR3'])
    
    return all_passed


def test_validation():
    """测试验证功能"""
    print_section("测试验证功能")
    
    all_passed = True
    test_vars = ['TEST_REQUIRED', 'TEST_PORT', 'TEST_EMAIL', 'TEST_ENV']
    
    try:
        # 测试 required 验证
        cleanup_env(test_vars)
        result = validate_env('TEST_REQUIRED', [{'rule': 'required'}])
        passed = not result.valid and len(result.errors) == 1
        all_passed &= print_test("验证必需变量（缺失）", passed, f"错误：{result.errors}")
        
        os.environ['TEST_REQUIRED'] = 'value'
        result = validate_env('TEST_REQUIRED', [{'rule': 'required'}])
        passed = result.valid
        all_passed &= print_test("验证必需变量（存在）", passed)
        
        # 测试数值范围验证
        os.environ['TEST_PORT'] = '8080'
        result = validate_env('TEST_PORT', [
            {'rule': 'min_value', 'value': 1024},
            {'rule': 'max_value', 'value': 65535}
        ])
        passed = result.valid
        all_passed &= print_test("验证数值范围（有效）", passed)
        
        os.environ['TEST_PORT'] = '80'
        result = validate_env('TEST_PORT', [
            {'rule': 'min_value', 'value': 1024}
        ])
        passed = not result.valid
        all_passed &= print_test("验证数值范围（无效）", passed)
        
        # 测试模式验证
        os.environ['TEST_EMAIL'] = 'test@example.com'
        result = validate_env('TEST_EMAIL', [
            {'rule': 'pattern', 'value': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'}
        ])
        passed = result.valid
        all_passed &= print_test("验证邮箱格式", passed)
        
        # 测试 choices 验证
        os.environ['TEST_ENV'] = 'production'
        result = validate_env('TEST_ENV', [
            {'rule': 'choices', 'value': ['development', 'staging', 'production']}
        ])
        passed = result.valid
        all_passed &= print_test("验证选项（有效）", passed)
        
        os.environ['TEST_ENV'] = 'invalid'
        result = validate_env('TEST_ENV', [
            {'rule': 'choices', 'value': ['development', 'staging', 'production']}
        ])
        passed = not result.valid
        all_passed &= print_test("验证选项（无效）", passed)
        
        # 测试 schema 验证
        os.environ['TEST_REQUIRED'] = 'value'
        os.environ['TEST_PORT'] = '8080'
        schema = {
            'TEST_REQUIRED': {'rules': [{'rule': 'required'}]},
            'TEST_PORT': {'rules': [
                {'rule': 'min_value', 'value': 1024},
                {'rule': 'max_value', 'value': 65535}
            ]}
        }
        result = validate_env_schema(schema)
        passed = result.valid
        all_passed &= print_test("Schema 验证（全部通过）", passed)
        
    finally:
        cleanup_env(test_vars)
    
    return all_passed


def test_snapshots():
    """测试快照功能"""
    print_section("测试快照功能")
    
    all_passed = True
    temp_files = []
    
    try:
        # 捕获快照
        snapshot = capture_snapshot('Test snapshot')
        passed = snapshot.variable_count > 0
        all_passed &= print_test("捕获快照", passed, f"变量数：{snapshot.variable_count}")
        
        passed = snapshot.source == 'system'
        all_passed &= print_test("快照来源", passed, f"来源：{snapshot.source}")
        
        # 修改环境变量
        set_env('SNAPSHOT_TEST', 'original')
        before = capture_snapshot('Before change')
        
        set_env('SNAPSHOT_TEST', 'modified')
        set_env('SNAPSHOT_NEW', 'new_value')
        after = capture_snapshot('After change')
        
        # 测试差异比较
        diff = diff_snapshots(before, after)
        passed = 'SNAPSHOT_NEW' in diff['added']
        all_passed &= print_test("检测新增变量", passed, f"新增：{diff['added']}")
        
        passed = 'SNAPSHOT_TEST' in diff['changed']
        all_passed &= print_test("检测修改变量", passed, f"修改：{list(diff['changed'].keys())}")
        
        # 测试保存快照
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_json = f.name
            temp_files.append(temp_json)
        
        saved = save_snapshot(snapshot, temp_json)
        passed = saved
        all_passed &= print_test("保存快照到文件", passed)
        
        # 测试加载快照
        loaded = load_snapshot(temp_json)
        passed = loaded is not None and loaded.variable_count == snapshot.variable_count
        all_passed &= print_test("从文件加载快照", passed, f"变量数：{loaded.variable_count if loaded else 0}")
        
        # 测试恢复快照
        set_env('RESTORE_TEST', 'test_value')
        passed = os.environ.get('RESTORE_TEST') == 'test_value'
        all_passed &= print_test("设置测试变量", passed)
        
        # 创建只包含少量变量的快照用于恢复测试
        test_snapshot = EnvSnapshot(
            timestamp=datetime.now().isoformat(),
            variables={'RESTORE_TEST': 'restored_value', 'PATH': os.environ.get('PATH', '')},
            source='test',
            description='Restore test'
        )
        count = restore_snapshot(test_snapshot, clear_first=False)
        passed = os.environ.get('RESTORE_TEST') == 'restored_value'
        all_passed &= print_test("恢复快照", passed, f"恢复数：{count}")
        
    finally:
        # 清理临时文件
        for filepath in temp_files:
            try:
                os.unlink(filepath)
            except:
                pass
        cleanup_env(['SNAPSHOT_TEST', 'SNAPSHOT_NEW', 'RESTORE_TEST'])
    
    return all_passed


def test_sensitive_data():
    """测试敏感数据处理"""
    print_section("测试敏感数据处理")
    
    all_passed = True
    
    try:
        # 测试脱敏
        test_vars = {
            'DATABASE_PASSWORD': 'supersecret123',
            'API_KEY': 'key-abc-123',
            'APP_NAME': 'MyApplication',
            'SHORT_PWD': 'abc'
        }
        
        masked = mask_sensitive_vars(test_vars)
        
        passed = masked['DATABASE_PASSWORD'] == 'su**********23'
        all_passed &= print_test("脱敏长密码", passed, f"原：{test_vars['DATABASE_PASSWORD']}, 脱敏：{masked['DATABASE_PASSWORD']}")
        
        passed = masked['API_KEY'] == 'ke*******23'
        all_passed &= print_test("脱敏 API 密钥", passed, f"脱敏：{masked['API_KEY']}")
        
        passed = masked['APP_NAME'] == 'MyApplication'
        all_passed &= print_test("非敏感变量不变", passed)
        
        passed = masked['SHORT_PWD'] == '***'
        all_passed &= print_test("脱敏短密码", passed, f"脱敏：{masked['SHORT_PWD']}")
        
        # 测试安全转储
        os.environ['TEST_SAFE_PASSWORD'] = 'secret'
        os.environ['TEST_SAFE_NORMAL'] = 'visible'
        
        dump = get_safe_env_dump()
        passed = 'secret' not in dump
        all_passed &= print_test("安全转储不包含明文密码", passed)
        
        passed = 'visible' in dump
        all_passed &= print_test("安全转储包含正常变量", passed)
        
    finally:
        cleanup_env(['TEST_SAFE_PASSWORD', 'TEST_SAFE_NORMAL'])
    
    return all_passed


def test_utility_functions():
    """测试工具函数"""
    print_section("测试工具函数")
    
    all_passed = True
    test_vars = ['TEST_HOME', 'TEST_DB_HOST', 'TEST_DB_PORT', 'ENV', 'APP_NAME']
    
    try:
        # 测试环境变量展开
        os.environ['TEST_HOME'] = '/home/user'
        text = expand_env_vars('Path: $TEST_HOME/documents')
        passed = text == 'Path: /home/user/documents'
        all_passed &= print_test("展开 $VAR 语法", passed, f"结果：{text}")
        
        text = expand_env_vars('Path: ${TEST_HOME}/documents')
        passed = text == 'Path: /home/user/documents'
        all_passed &= print_test("展开 ${VAR} 语法", passed, f"结果：{text}")
        
        text = expand_env_vars('Value: ${NONEXISTENT:-default}')
        passed = text == 'Value: default'
        all_passed &= print_test("展开带默认值语法", passed, f"结果：{text}")
        
        # 测试配置插值
        os.environ['TEST_DB_HOST'] = 'localhost'
        os.environ['TEST_DB_PORT'] = '5432'
        config = {
            'database': {
                'host': '${TEST_DB_HOST}',
                'port': '${TEST_DB_PORT}',
                'name': 'mydb'
            },
            'servers': ['${TEST_DB_HOST}', 'backup_host']
        }
        result = interpolate_env_vars(config)
        passed = result['database']['host'] == 'localhost'
        all_passed &= print_test("递归配置插值", passed, f"结果：{result['database']}")
        
        # 测试环境变量树
        tree = get_env_tree('TEST_DB')
        passed = 'HOST' in tree and 'PORT' in tree
        all_passed &= print_test("环境变量树", passed, f"树：{tree}")
        
        # 测试环境检查函数
        os.environ['ENV'] = 'production'
        passed = is_production() == True
        all_passed &= print_test("检查生产环境", passed)
        
        os.environ['ENV'] = 'development'
        passed = is_development() == True
        all_passed &= print_test("检查开发环境", passed)
        
        os.environ['ENV'] = 'test'
        passed = is_testing() == True
        all_passed &= print_test("检查测试环境", passed)
        
        # 测试应用信息
        os.environ['ENV'] = 'production'
        os.environ['APP_NAME'] = 'TestApp'
        os.environ['APP_VERSION'] = '1.0.0'
        os.environ['PORT'] = '3000'
        os.environ['DEBUG'] = 'false'
        
        info = get_app_info()
        passed = info['environment'] == 'production' and info['app_name'] == 'TestApp'
        all_passed &= print_test("获取应用信息", passed, f"信息：{info}")
        
        # 测试 require_envs
        os.environ['REQ_VAR1'] = 'value1'
        os.environ['REQ_VAR2'] = 'value2'
        result = require_envs('REQ_VAR1', 'REQ_VAR2')
        passed = result['REQ_VAR1'] == 'value1' and result['REQ_VAR2'] == 'value2'
        all_passed &= print_test("要求多个环境变量", passed)
        
        try:
            require_envs('NONEXISTENT_VAR')
            passed = False
        except EnvironmentError:
            passed = True
        all_passed &= print_test("要求不存在变量抛出异常", passed)
        
    finally:
        cleanup_env(test_vars + ['REQ_VAR1', 'REQ_VAR2'])
    
    return all_passed


def test_env_dataclass():
    """测试 EnvVar 数据类"""
    print_section("测试 EnvVar 数据类")
    
    all_passed = True
    
    try:
        # 创建 EnvVar
        var = EnvVar(
            name='DATABASE_PASSWORD',
            value='secret123',
            var_type=VarType.STRING,
            required=True,
            description='数据库密码',
            sensitive=True
        )
        
        passed = var.name == 'DATABASE_PASSWORD'
        all_passed &= print_test("创建 EnvVar", passed)
        
        # 测试脱敏值
        masked = var.mask_value()
        passed = masked == 'se*****23'
        all_passed &= print_test("脱敏值", passed, f"脱敏后：{masked}")
        
        # 测试非敏感变量
        normal_var = EnvVar(name='APP_NAME', value='MyApp', sensitive=False)
        passed = normal_var.mask_value() == 'MyApp'
        all_passed &= print_test("非敏感变量不脱敏", passed)
        
        # 测试类型化值
        int_var = EnvVar(name='PORT', value='8080', var_type=VarType.INTEGER)
        passed = int_var.get_typed_value() == 8080
        all_passed &= print_test("获取类型化值", passed, f"值：{int_var.get_typed_value()}")
        
    finally:
        pass
    
    return all_passed


# =============================================================================
# 主测试函数
# =============================================================================

def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("  AllToolkit - Environment Utilities 测试套件")
    print("="*60)
    
    results = []
    
    results.append(("基本操作", test_basic_operations()))
    results.append(("类型转换", test_type_conversion()))
    results.append((".env 文件操作", test_env_file_operations()))
    results.append(("验证功能", test_validation()))
    results.append(("快照功能", test_snapshots()))
    results.append(("敏感数据处理", test_sensitive_data()))
    results.append(("工具函数", test_utility_functions()))
    results.append(("EnvVar 数据类", test_env_dataclass()))
    
    # 打印总结
    print("\n" + "="*60)
    print("  测试总结")
    print("="*60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {name}")
    
    print(f"\n  总计：{passed_count}/{total_count} 通过")
    
    if passed_count == total_count:
        print("\n  🎉 所有测试通过！")
        return True
    else:
        print(f"\n  ⚠️  {total_count - passed_count} 个测试失败")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
