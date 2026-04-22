import os
import logging
from dotenv import load_dotenv

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_qdrant_connection():
    # 1. 加载环境变量
    load_dotenv()
    
    url = os.getenv("QDRANT_URL", "http://localhost:6333")
    api_key = os.getenv("QDRANT_API_KEY")
    collection_name = os.getenv("QDRANT_COLLECTION", "test_connection_collection")
    
    print(f"🔍 正在尝试连接到 Qdrant: {url}")
    
    try:
        from qdrant_client import QdrantClient
        from qdrant_client.http import models
    except ImportError:
        print("❌ 错误: 未安装 qdrant-client。请运行 'pip install qdrant-client'")
        return

    try:
        # 2. 初始化客户端
        client = QdrantClient(url=url, api_key=api_key, timeout=10)
        
        # 3. 检查基本连通性
        collections = client.get_collections()
        print(f"✅ 成功连接到 Qdrant 服务！")
        print(f"当前存在的集合数量: {len(collections.collections)}")
        
        # 4. 测试创建一个临时测试集合 (如果不存在)
        if collection_name not in [c.name for c in collections.collections]:
            print(f"🔨 正在创建测试集合: {collection_name}...")
            client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
            )
            print(f"✅ 测试集合创建成功")
        else:
            print(f"ℹ️ 测试集合 '{collection_name}' 已存在")
            
        print("\n🚀 Qdrant 环境检查完成，一切正常！")
        print(f"你可以访问 http://localhost:6333/dashboard 在浏览器中查看。")

    except Exception as e:
        print(f"❌ 连接失败: {str(e)}")
        print("\n请确保：")
        print("1. Docker Desktop 已启动且正在运行")
        print("2. 已在项目目录下运行过 'docker-compose up -d'")
        print("3. .env 文件中 QDRANT_URL 指向了正确的地址 (本地通常为 http://localhost:6333)")

if __name__ == "__main__":
    test_qdrant_connection()
