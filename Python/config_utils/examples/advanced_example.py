#!/usr/bin/env python3
"""
AllToolkit - Configuration Utilities Advanced Example

演示如何使用 config_utils 构建完整的应用配置系统。
"""

import sys
import os
import tempfile
from pathlib import Path

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    Config,
    ConfigParser,
    ConfigSchema,
    create_schema,
    load_config,
    ConfigFormat,
    ConfigValidationError,
    DATABASE_SCHEMA,
    SERVER_SCHEMA,
    LOGGING_SCHEMA,
)


def create_sample_config_files():
    """创建示例配置文件。"""
    temp_dir = tempfile.mkdtemp(prefix='config_utils_example_')
    
    # Key-Value 配置文件
    kv_path = Path(temp_dir) / 'app.conf'
    kv_path.write_text("""
# 应用程序配置文件

# 服务器配置
server.host=0.0.0.0
server.port=${SERVER_PORT:-8080}
server.debug=${DEBUG:-false}
server.workers=4

# 数据库配置
database.host=${DB_HOST:-localhost}
database.port=${DB_PORT:-5432}
database.name=${DB_NAME:-myapp}
database.user=${DB_USER:-admin}
database.password=${DB_PASSWORD:-secret}
database.ssl=false
database.pool_size=10

# 缓存配置
cache.enabled=true
cache.backend=redis
cache.host=${REDIS_HOST:-localhost}
cache.port=${REDIS_PORT:-6379}
cache.ttl=300

# 日志配置
logging.level=INFO
logging.file=/var/log/myapp/app.log
logging.max_size=10485760
logging.backup_count=5

# 功能开关
features.auth=true
features.api=true
features.admin=false
features.metrics=true
""")
    
    # JSON 配置文件
    json_path = Path(temp_dir) / 'settings.json'
    json_path.write_text("""
{
    "app": {
        "name": "MyApplication",
        "version": "1.0.0",
        "environment": "development"
    },
    "server": {
        "host": "0.0.0.0",
        "port": 8080,
        "debug": true,
        "cors_origins": ["http://localhost:3000", "http://localhost:8080"]
    },
    "database": {
        "driver": "postgresql",
        "host": "localhost",
        "port": 5432,
        "name": "myapp",
        "pool_size": 10,
        "timeout": 30
    },
    "cache": {
        "enabled": true,
        "backend": "redis",
        "ttl": 300
    },
    "logging": {
        "level": "DEBUG",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "handlers": ["console", "file"]
    }
}
""")
    
    # INI 配置文件
    ini_path = Path(temp_dir) / 'config.ini'
    ini_path.write_text("""
[application]
name = MyApplication
version = 1.0.0
environment = production

[server]
host = 0.0.0.0
port = 8080
workers = 4
timeout = 30

[database]
driver = postgresql
host = db.example.com
port = 5432
name = production_db
user = app_user
password = ${DB_PASSWORD}
pool_size = 20

[cache]
enabled = true
backend = redis
host = redis.example.com
port = 6379
ttl = 600

[logging]
level = WARNING
file = /var/log/myapp/production.log
max_size = 52428800
backup_count = 10

[security]
secret_key = ${SECRET_KEY}
token_expiry = 3600
rate_limit = 100
""")
    
    return temp_dir, kv_path, json_path, ini_path


class ApplicationConfig:
    """
    应用程序配置管理类。
    
    演示如何构建一个完整的配置系统。
    """
    
    def __init__(self, config_path: str = None):
        """
        初始化应用配置。
        
        Args:
            config_path: 配置文件路径（可选）
        """
        self._config: Config = None
        self._load_config(config_path)
    
    def _create_schema(self) -> ConfigSchema:
        """创建应用 Schema。"""
        return create_schema(
            # 应用信息
            app_name=dict(type=str, default='MyApp'),
            app_version=dict(type=str, default='1.0.0'),
            environment=dict(type=str, choices=['development', 'staging', 'production']),
            
            # 服务器
            server_host=dict(type=str, default='0.0.0.0'),
            server_port=dict(type=int, required=True, min=1, max=65535),
            server_debug=dict(type=bool, default=False),
            server_workers=dict(type=int, default=4, min=1, max=64),
            
            # 数据库
            database_host=dict(type=str, required=True),
            database_port=dict(type=int, default=5432),
            database_name=dict(type=str, required=True),
            database_user=dict(type=str, required=True),
            database_password=dict(type=str, required=True),
            database_pool_size=dict(type=int, default=10, min=1),
            
            # 缓存
            cache_enabled=dict(type=bool, default=True),
            cache_backend=dict(type=str, choices=['memory', 'redis', 'memcached']),
            cache_host=dict(type=str),
            cache_port=dict(type=int),
            cache_ttl=dict(type=int, default=300),
            
            # 日志
            logging_level=dict(type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR']),
            logging_file=dict(type=str),
            logging_max_size=dict(type=int, default=10485760),
        )
    
    def _load_config(self, config_path: str = None):
        """加载配置。"""
        schema = self._create_schema()
        
        if config_path:
            # 从文件加载
            self._config = load_config(
                config_path,
                schema=schema,
                env_substitute=True,
                env_prefix=''
            )
        else:
            # 使用默认配置
            self._config = Config({
                'app_name': 'MyApp',
                'app_version': '1.0.0',
                'environment': 'development',
                'server_host': '0.0.0.0',
                'server_port': 8080,
                'server_debug': True,
                'server_workers': 2,
                'database_host': 'localhost',
                'database_port': 5432,
                'database_name': 'dev_db',
                'database_user': 'dev_user',
                'database_password': 'dev_password',
                'database_pool_size': 5,
                'cache_enabled': True,
                'cache_backend': 'memory',
                'cache_ttl': 60,
                'logging_level': 'DEBUG',
            }, schema)
        
        # 验证配置
        try:
            self._config.validate_strict()
        except ConfigValidationError as e:
            print(f"配置验证失败：{e}")
            raise
    
    @property
    def config(self) -> Config:
        """获取配置对象。"""
        return self._config
    
    def get_database_url(self) -> str:
        """构建数据库连接 URL。"""
        return (
            f"postgresql://{self._config.get('database_user')}:"
            f"{self._config.get('database_password')}@"
            f"{self._config.get('database_host')}:"
            f"{self._config.get_int('database_port')}/"
            f"{self._config.get('database_name')}"
        )
    
    def get_cache_config(self) -> dict:
        """获取缓存配置。"""
        return {
            'enabled': self._config.get_bool('cache_enabled'),
            'backend': self._config.get('cache_backend'),
            'host': self._config.get('cache_host'),
            'port': self._config.get_int('cache_port'),
            'ttl': self._config.get_int('cache_ttl'),
        }
    
    def get_server_config(self) -> dict:
        """获取服务器配置。"""
        return {
            'host': self._config.get('server_host'),
            'port': self._config.get_int('server_port'),
            'debug': self._config.get_bool('server_debug'),
            'workers': self._config.get_int('server_workers'),
        }
    
    def get_logging_config(self) -> dict:
        """获取日志配置。"""
        return {
            'level': self._config.get('logging_level', 'INFO'),
            'file': self._config.get('logging_file'),
            'max_size': self._config.get_int('logging_max_size'),
        }
    
    def is_production(self) -> bool:
        """检查是否为生产环境。"""
        return self._config.get('environment') == 'production'
    
    def print_config_summary(self):
        """打印配置摘要。"""
        print("\n" + "=" * 60)
        print("应用程序配置摘要")
        print("=" * 60)
        
        print(f"\n📦 应用信息:")
        print(f"   名称：{self._config.get('app_name')}")
        print(f"   版本：{self._config.get('app_version')}")
        print(f"   环境：{self._config.get('environment')}")
        
        print(f"\n🌐 服务器配置:")
        server = self.get_server_config()
        print(f"   地址：{server['host']}:{server['port']}")
        print(f"   调试：{'开启' if server['debug'] else '关闭'}")
        print(f"   工作进程：{server['workers']}")
        
        print(f"\n💾 数据库配置:")
        print(f"   主机：{self._config.get('database_host')}:{self._config.get_int('database_port')}")
        print(f"   数据库：{self._config.get('database_name')}")
        print(f"   用户：{self._config.get('database_user')}")
        print(f"   连接池：{self._config.get_int('database_pool_size')}")
        
        print(f"\n🚀 缓存配置:")
        cache = self.get_cache_config()
        if cache['enabled']:
            print(f"   状态：启用")
            print(f"   后端：{cache['backend']}")
            if cache['host']:
                print(f"   地址：{cache['host']}:{cache['port']}")
            print(f"   TTL: {cache['ttl']}秒")
        else:
            print(f"   状态：禁用")
        
        print(f"\n📝 日志配置:")
        logging = self.get_logging_config()
        print(f"   级别：{logging['level']}")
        if logging['file']:
            print(f"   文件：{logging['file']}")
        print(f"   最大大小：{logging['max_size'] / 1024 / 1024:.1f}MB")
        
        print("\n" + "=" * 60)


def example_load_kv_config(temp_dir: str, kv_path: Path):
    """加载 Key-Value 配置文件示例。"""
    print("\n" + "=" * 60)
    print("示例 1: 加载 Key-Value 配置文件")
    print("=" * 60)
    
    # 设置环境变量
    os.environ['SERVER_PORT'] = '9000'
    os.environ['DEBUG'] = 'true'
    os.environ['DB_HOST'] = 'db.production.com'
    os.environ['DB_PASSWORD'] = 'production_secret'
    os.environ['REDIS_HOST'] = 'redis.production.com'
    
    try:
        config = load_config(kv_path, env_substitute=True)
        
        print(f"\n服务器端口：{config.get('server.port')}")
        print(f"调试模式：{config.get('server.debug')}")
        print(f"数据库主机：{config.get('database.host')}")
        print(f"Redis 主机：{config.get('cache.host')}")
        
    finally:
        # 清理环境变量
        for key in ['SERVER_PORT', 'DEBUG', 'DB_HOST', 'DB_PASSWORD', 'REDIS_HOST']:
            os.environ.pop(key, None)


def example_load_json_config(json_path: Path):
    """加载 JSON 配置文件示例。"""
    print("\n" + "=" * 60)
    print("示例 2: 加载 JSON 配置文件")
    print("=" * 60)
    
    config = load_config(json_path, format=ConfigFormat.JSON)
    
    print(f"\n应用名称：{config.get('app.name')}")
    print(f"应用版本：{config.get('app.version')}")
    print(f"环境：{config.get('app.environment')}")
    print(f"CORS 来源：{config.get('server.cors_origins')}")
    print(f"日志处理器：{config.get('logging.handlers')}")


def example_load_ini_config(ini_path: Path):
    """加载 INI 配置文件示例。"""
    print("\n" + "=" * 60)
    print("示例 3: 加载 INI 配置文件")
    print("=" * 60)
    
    config = load_config(ini_path, format=ConfigFormat.INI)
    
    print(f"\n配置文件结构:")
    for section in config.keys():
        print(f"  [{section}]")
        section_data = config.get_dict(section)
        for key in section_data.keys():
            value = config.get(f'{section}.{key}')
            print(f"    {key} = {value}")


def example_application_config_class(temp_dir: str):
    """使用 ApplicationConfig 类示例。"""
    print("\n" + "=" * 60)
    print("示例 4: 使用 ApplicationConfig 类")
    print("=" * 60)
    
    # 设置环境变量
    os.environ['DB_PASSWORD'] = 'secret123'
    os.environ['SECRET_KEY'] = 'my-super-secret-key'
    
    try:
        # 使用默认配置
        print("\n使用默认配置:")
        app_config = ApplicationConfig()
        app_config.print_config_summary()
        
        print(f"\n数据库 URL: {app_config.get_database_url()}")
        print(f"是否生产环境：{app_config.is_production()}")
        
    finally:
        os.environ.pop('DB_PASSWORD', None)
        os.environ.pop('SECRET_KEY', None)


def example_custom_schema():
    """自定义 Schema 示例。"""
    print("\n" + "=" * 60)
    print("示例 5: 自定义 Schema")
    print("=" * 60)
    
    # 创建复杂 Schema
    schema = create_schema(
        # 必需字段
        api_key=dict(type=str, required=True, description="API 密钥"),
        api_secret=dict(type=str, required=True, description="API 密钥"),
        
        # 带范围的数字
        rate_limit=dict(type=int, min=1, max=10000, default=100),
        timeout=dict(type=int, min=1, max=300, default=30),
        
        # 选择项
        region=dict(type=str, choices=['us-east', 'us-west', 'eu-west', 'ap-east'], default='us-east'),
        
        # 正则验证
        webhook_url=dict(
            type=str,
            pattern=r'^https?://[\w.-]+(?:/[\w.-]*)*$',
            description="Webhook URL"
        ),
        
        # 列表
        allowed_ips=dict(type=list, default=[]),
    )
    
    # 有效配置
    valid_config = Config({
        'api_key': 'pk_test_123',
        'api_secret': 'sk_test_456',
        'rate_limit': 500,
        'timeout': 60,
        'region': 'ap-east',
        'webhook_url': 'https://example.com/webhook',
        'allowed_ips': ['192.168.1.1', '10.0.0.1'],
    }, schema)
    
    is_valid, errors = valid_config.validate()
    print(f"\n有效配置验证：{'通过 ✓' if is_valid else '失败 ✗'}")
    
    # 无效配置
    invalid_config = Config({
        'api_key': 'pk_test_123',
        # 缺少 api_secret
        'rate_limit': 50000,  # 超出范围
        'region': 'invalid-region',  # 不在选项中
        'webhook_url': 'not-a-url',  # 不匹配正则
    }, schema)
    
    is_valid, errors = invalid_config.validate()
    print(f"\n无效配置验证：{'通过 ✓' if is_valid else '失败 ✗'}")
    if errors:
        print("\n错误列表:")
        for error in errors:
            print(f"  - {error}")


def example_config_merge():
    """配置合并示例。"""
    print("\n" + "=" * 60)
    print("示例 6: 配置合并")
    print("=" * 60)
    
    # 基础配置
    base_config = Config({
        'app_name': 'MyApp',
        'debug': False,
        'log_level': 'INFO',
        'database': {
            'host': 'localhost',
            'port': 5432,
        }
    })
    
    # 开发环境覆盖
    dev_override = Config({
        'debug': True,
        'log_level': 'DEBUG',
        'database': {
            'host': 'dev-db.local',
        }
    })
    
    # 合并配置
    for key in dev_override.keys():
        base_config.set(key, dev_override.get(key))
    
    print(f"\n合并后的配置:")
    print(f"  app_name: {base_config.get('app_name')}")
    print(f"  debug: {base_config.get('debug')}")
    print(f"  log_level: {base_config.get('log_level')}")
    print(f"  database.host: {base_config.get('database.host')}")
    print(f"  database.port: {base_config.get('database.port')}")


def main():
    """运行所有高级示例。"""
    print("\n" + "=" * 60)
    print("AllToolkit Configuration Utilities - 高级示例")
    print("=" * 60)
    
    # 创建示例配置文件
    temp_dir, kv_path, json_path, ini_path = create_sample_config_files()
    
    try:
        example_load_kv_config(temp_dir, kv_path)
        example_load_json_config(json_path)
        example_load_ini_config(ini_path)
        example_application_config_class(temp_dir)
        example_custom_schema()
        example_config_merge()
        
        print("\n" + "=" * 60)
        print("所有高级示例运行完成！")
        print("=" * 60)
        
    finally:
        # 清理临时文件
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == '__main__':
    main()
