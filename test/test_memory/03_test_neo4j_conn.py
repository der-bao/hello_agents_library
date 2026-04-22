import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# 加载环境变量
load_dotenv()

def test_neo4j_connection():
    # 从环境变量获取配置
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password123")
    
    print(f"尝试连接到 Neo4j: {uri} (用户: {user})...")
    
    try:
        # 建立驱动
        driver = GraphDatabase.driver(uri, auth=(user, password))
        
        # 验证连接并获取服务器信息
        with driver.session() as session:
            result = session.run("RETURN 'Connection Successful!' as message, datetime() as time")
            record = result.single()
            print(f"成功! 服务端响应: {record['message']}")
            print(f"服务端时间: {record['time']}")
            
            # 创建并删除一个测试节点以验证写入权限
            print("正在验证写入权限...")
            session.run("CREATE (t:TestNode {name: 'connection_test'})")
            session.run("MATCH (t:TestNode {name: 'connection_test'}) DELETE t")
            print("写入和删除测试成功。")
            
        driver.close()
        print("\nNeo4j 连接测试全部通过！")
        
    except Exception as e:
        print(f"\n连接失败!")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误详情: {e}")
        print("\n请检查：")
        print("1. Docker 容器是否已启动 (docker ps)")
        print("2. .env 文件中的用户名和密码是否正确")
        print("3. neo4j 库是否已安装 (pip install neo4j)")

if __name__ == "__main__":
    test_neo4j_connection()
