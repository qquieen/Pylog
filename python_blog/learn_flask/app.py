import sqlite3 
import os
import logging
from flask import Flask, render_template

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__) #创建一个Flask对象

# 获取数据库的绝对路径
DATABASE = os.path.join(app.root_path, 'database.db')
logger.info(f"数据库路径: {DATABASE}")

def get_db_connection():
    try:
        #使用绝对路径创建数据库链接
        conn = sqlite3.connect(DATABASE)
        #设置数据的解析方法，有了这个设置，就可以像字典一样访问每一列数据
        conn.row_factory = sqlite3.Row
        logger.info("成功连接到数据库")
        return conn
    except sqlite3.Error as e:
        logger.error(f"数据库连接错误: {e}")
        raise

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return post


@app.route('/') #如果请求根目录url，就访问下面的方法
def index():
    try:
        #调用上面的函数获取链接
        conn = get_db_connection()
        #查询所有数据，放到变量posts中
        posts = conn.execute('SELECT * FROM posts').fetchall()
        logger.info(f"成功查询到 {len(posts)} 篇文章")
        #关闭链接
        conn.close()
        
        #把查询出来的posts传给网页，网页中可以使用{{ posts }}来访问
        return render_template('index.html', posts=posts)
    except sqlite3.Error as e:
        logger.error(f"数据库查询错误: {e}")
        # 在实际应用中，应该显示一个友好的错误页面
        return f"数据库错误: {e}", 500
    except Exception as e:
        logger.error(f"未知错误: {e}")
        return f"服务器错误: {e}", 500
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post:
        return render_template('post.html', post=post)
    else:
        return f"文章 {post_id} 不存在", 404


if __name__ == '__main__':
    app.run(debug=True)