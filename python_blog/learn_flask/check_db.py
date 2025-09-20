import sqlite3

# 连接数据库
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# 检查数据库中的所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("数据库中的表：")
for table in tables:
    print(table[0])

# 如果posts表存在，检查其结构
if any('posts' == table[0] for table in tables):
    print("\nposts表结构：")
    cursor.execute("PRAGMA table_info(posts);")
    columns = cursor.fetchall()
    for column in columns:
        print(f"列名: {column[1]}, 类型: {column[2]}")
    
    # 查询posts表中的数据
    print("\nposts表中的数据：")
    cursor.execute("SELECT * FROM posts;")
    posts = cursor.fetchall()
    for post in posts:
        print(post)
else:
    print("\nposts表不存在！")

# 关闭连接
conn.close()