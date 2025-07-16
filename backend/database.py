import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# 数据库配置
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://root:1234qwer!@127.0.0.1:3306/mingjun"
)

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建SessionLocal类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建Base类
Base = declarative_base()

def create_database():
    """创建数据库（如果不存在）"""
    try:
        # 连接MySQL服务器（不指定数据库）
        connection = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='1234qwer!',
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # 创建数据库
            cursor.execute("CREATE DATABASE IF NOT EXISTS mingjun CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("数据库创建成功或已存在")
        
        connection.close()
        
    except Exception as e:
        print(f"创建数据库时出错: {e}")

if __name__ == "__main__":
    create_database()