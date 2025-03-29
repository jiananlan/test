from pymongo import MongoClient

# 连接 MongoDB
client = MongoClient("mongodb://localhost:27017/")

# 获取数据库
db = client.test_database

# 插入数据
db.test_collection.insert_one({"message": "Hello, MongoDB from GitHub Actions!"})

# 读取数据
doc = db.test_collection.find_one()
print("Retrieved from MongoDB:", doc)

# 关闭连接
client.close()
