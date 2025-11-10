# Redis 与 RedisJSON 集成文档 / Redis with RedisJSON Integration

## 概述 / Overview

本项目现已集成 Redis 数据库和 RedisJSON 模块，提供高性能的键值存储和原生 JSON 数据支持。

This project now integrates Redis database with RedisJSON module, providing high-performance key-value storage and native JSON data support.

## 功能特性 / Features

### ✅ Redis Stack
- **Redis 7.4.7**: 最新稳定版 Redis 服务器
- **RedisJSON 模块**: 原生 JSON 数据类型支持
- **RedisSearch 模块**: 全文搜索和查询功能
- **RedisTimeSeries**: 时间序列数据支持
- **RedisBloom**: 概率数据结构

### ✅ RedisJSON API 版本
项目支持所有 RedisJSON API 版本：
- RedisJSON_V1 API ✅
- RedisJSON_V2 API ✅
- RedisJSON_V3 API ✅
- RedisJSON_V4 API ✅
- RedisJSON_V5 API ✅

## 启动日志示例 / Startup Logs Example

当 Redis 成功启动时，您将看到类似以下的日志：

```
9:M 10 Nov 2025 10:19:11.056 * <ReJSON> Created new data type 'ReJSON-RL'
9:M 10 Nov 2025 10:19:11.056 * <ReJSON> version: 20809 git sha: unknown branch: unknown
9:M 10 Nov 2025 10:19:11.056 * <ReJSON> Exported RedisJSON_V1 API
9:M 10 Nov 2025 10:19:11.056 * <ReJSON> Exported RedisJSON_V2 API
9:M 10 Nov 2025 10:19:11.056 * <ReJSON> Exported RedisJSON_V3 API
9:M 10 Nov 2025 10:19:11.056 * <ReJSON> Exported RedisJSON_V4 API
9:M 10 Nov 2025 10:19:11.056 * <ReJSON> Exported RedisJSON_V5 API
9:M 10 Nov 2025 10:19:11.054 * <search> Initialized thread pools!
9:M 10 Nov 2025 10:19:11.059 * Ready to accept connections tcp
```

## 部署方式 / Deployment

### Docker Compose (推荐 / Recommended)

1. **启动 Redis 和机器人服务 / Start Redis and Bot Services:**
```bash
docker compose up -d
```

2. **查看 Redis 日志 / View Redis Logs:**
```bash
docker compose logs redis --tail 50
```

3. **查看机器人日志 / View Bot Logs:**
```bash
docker compose logs telegram-bot --tail 50
```

4. **停止服务 / Stop Services:**
```bash
docker compose down
```

### 本地开发 / Local Development

1. **启动 Redis Stack:**
```bash
docker compose up -d redis
```

2. **设置环境变量 / Set Environment Variables:**
```bash
export TG_TOKEN="your_telegram_bot_token"
export REDIS_HOST="localhost"
export REDIS_PORT="6379"
```

3. **安装依赖 / Install Dependencies:**
```bash
pip install -r requirements.txt
```

4. **运行机器人 / Run Bot:**
```bash
python main.py
```

## 环境变量 / Environment Variables

### Redis 配置 / Redis Configuration

在 `.env` 文件中添加以下配置：

```bash
# Redis Configuration
REDIS_HOST=localhost      # Redis 主机地址
REDIS_PORT=6379          # Redis 端口
REDIS_DB=0               # Redis 数据库编号
REDIS_PASSWORD=          # Redis 密码（如果需要）
```

### Docker Compose 环境

在 Docker Compose 中，服务会自动配置：
- `REDIS_HOST=redis` (容器名称)
- `REDIS_PORT=6379`

## Python API 使用 / Python API Usage

### 基本使用 / Basic Usage

```python
from redis_client import get_redis_client

# 获取 Redis 客户端实例
redis_client = get_redis_client()

# 字符串操作
redis_client.set('key', 'value')
value = redis_client.get('key')

# JSON 操作
import json
data = {'name': 'Bot', 'version': '1.0'}
redis_client.set_json('bot:config', '$', json.dumps(data))
result = redis_client.get_json('bot:config', '$')
```

### JSON 操作示例 / JSON Operations Examples

```python
import json
from redis_client import get_redis_client

redis_client = get_redis_client()

# 设置 JSON 数据
user_data = {
    'user_id': 123456,
    'username': 'john_doe',
    'settings': {
        'language': 'zh-CN',
        'notifications': True
    },
    'balance': 1000.50
}

redis_client.set_json('user:123456', '$', json.dumps(user_data))

# 获取整个 JSON
data = redis_client.get_json('user:123456', '$')
print(f"User data: {data}")

# 删除 JSON
redis_client.delete_json('user:123456')
```

## 测试 / Testing

运行测试脚本验证 Redis 和 RedisJSON 集成：

```bash
python test_redis.py
```

成功的测试输出：
```
============================================================
Testing Redis with RedisJSON Integration
============================================================

✅ Successfully connected to Redis

Testing basic string operations...
✅ String operations working

Testing RedisJSON operations...
✅ RedisJSON operations working

============================================================
✅ All tests passed!
============================================================
```

## 架构 / Architecture

```
┌─────────────────────┐
│   Telegram Bot      │
│    (Python)         │
└──────────┬──────────┘
           │
           │ redis_client.py
           │
┌──────────▼──────────┐
│   Redis Stack       │
│                     │
│  ┌───────────────┐  │
│  │  RedisJSON    │  │
│  │  RedisSearch  │  │
│  │  RedisTS      │  │
│  └───────────────┘  │
│                     │
│  Port: 6379         │
└─────────────────────┘
```

## 数据持久化 / Data Persistence

Redis 数据存储在 Docker volume 中，确保数据持久化：

```yaml
volumes:
  redis-data:  # 数据卷名称
```

### 备份数据 / Backup Data

```bash
# 备份 Redis 数据
docker compose exec redis redis-cli SAVE
docker cp my-robot-redis:/data/dump.rdb ./backup/

# 恢复数据
docker cp ./backup/dump.rdb my-robot-redis:/data/dump.rdb
docker compose restart redis
```

## 性能优化 / Performance Optimization

### Redis 配置建议

1. **内存优化**: 根据需要调整 maxmemory
2. **持久化策略**: 选择 RDB 或 AOF
3. **连接池**: Python 客户端自动管理连接池

### 最佳实践 / Best Practices

1. ✅ 使用 JSON 路径查询优化查询性能
2. ✅ 合理设置 key 过期时间
3. ✅ 使用连接池减少连接开销
4. ✅ 监控 Redis 内存使用
5. ✅ 定期备份重要数据

## 故障排除 / Troubleshooting

### Redis 连接失败

```bash
# 检查 Redis 是否运行
docker compose ps redis

# 查看 Redis 日志
docker compose logs redis

# 测试 Redis 连接
docker compose exec redis redis-cli ping
# 应返回: PONG
```

### RedisJSON 模块未加载

检查 Redis Stack 镜像是否正确：
```bash
docker compose exec redis redis-cli MODULE LIST
```

应该看到 ReJSON 模块在列表中。

## 监控 / Monitoring

### 查看 Redis 信息

```bash
# Redis 服务器信息
docker compose exec redis redis-cli INFO

# 内存使用
docker compose exec redis redis-cli INFO memory

# 已加载模块
docker compose exec redis redis-cli MODULE LIST
```

### Python 客户端日志

Redis 客户端会自动记录连接状态和操作日志：

```
INFO:redis_client:✅ Connected to Redis at localhost:6379
INFO:redis_client:📊 Redis version: 7.4.7
INFO:redis_client:✅ RedisJSON module loaded
INFO:redis_client:📦 RedisJSON APIs available:
INFO:redis_client:   - RedisJSON_V1 API
INFO:redis_client:   - RedisJSON_V2 API
INFO:redis_client:   - RedisJSON_V3 API
INFO:redis_client:   - RedisJSON_V4 API
```

## 扩展功能 / Advanced Features

### 使用 RedisSearch 进行全文搜索

```python
# 创建索引
redis_client.client.execute_command(
    'FT.CREATE', 'user_idx',
    'ON', 'JSON',
    'PREFIX', '1', 'user:',
    'SCHEMA', '$.username', 'AS', 'username', 'TEXT'
)

# 搜索
results = redis_client.client.execute_command(
    'FT.SEARCH', 'user_idx', '@username:john'
)
```

## 参考资源 / References

- [Redis Stack Documentation](https://redis.io/docs/stack/)
- [RedisJSON Commands](https://redis.io/docs/stack/json/)
- [Redis Python Client](https://redis-py.readthedocs.io/)

## 许可证 / License

MIT License - 详见 LICENSE 文件
