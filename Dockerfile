# 使用官方 Python 运行时作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用程序代码
COPY main.py .

# 设置环境变量（运行时需要提供）
ENV TG_TOKEN=""

# 运行机器人
CMD ["python", "-u", "main.py"]
