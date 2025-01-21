# 使用 Python 3.7 slim 版
FROM python:3.7-slim

# 安裝 gcc 及 MySQL/MariaDB client dev headers
RUN apt-get update && \
    apt-get install -y gcc default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt
COPY requirements.txt /app/

# 安裝套件
RUN pip install --no-cache-dir -r requirements.txt

# 複製整個 src/ 目錄 (或自行調整只複製需要的檔案)
COPY src /app/src

# 對外開放 8000
EXPOSE 8000

# 預設執行指令(可於 docker-compose 覆寫)
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
