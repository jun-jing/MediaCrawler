from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import pandas as pd
import math
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# 数据库配置
DATABASE = os.environ.get('FLASK_DATABASE', 'xhs_data.db')

def get_db():
    db = sqlite3.connect(app.config.get('DATABASE', DATABASE))
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS posts
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       title TEXT NOT NULL,
                       content TEXT NOT NULL,
                       price REAL,
                       surroundings TEXT,
                       address TEXT,
                       purchase_date DATE,
                       image_url TEXT,
                       created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)''')
        db.commit()

@app.route('/')
def show_excel():
    # 读取Excel文件
    df = pd.read_excel(r'data/xhs/1_search_comments.xlsx')
    
    # 选择要显示的列及其样式
    selected_columns = {
        'ip_location': {
            'white-space': 'nowrap',
            'width': '50px'  # 设置列宽
        },
        'content': {
            'white-space': 'normal',
            'width': '100px'  # 设置列宽
        },
        'nickname': {
            'white-space': 'nowrap',
            'width': '150px'  # 设置列宽
        },
        'title': {
            'white-space': 'nowrap',
            'width': '150px'  # 设置列宽
        },
        'desc': {
            'white-space': 'normal',
            'width': '500px'  # 设置列宽
        },        
        'liked_count': {
            'white-space': 'nowrap',
            'width': '50px'  # 设置列宽
        },
        'note_url': {
            'white-space': 'nowrap',
            'width': '200px'  # 设置列宽
        }
    }

    # 只保留所选列的数据
    df_filtered = df[list(selected_columns.keys())]
    
    # 处理 content 和 desc 列
    df_filtered['content'] = df_filtered['content'].apply(lambda x: x[:100] + '....' if isinstance(x, str) and len(x) > 120 else x)
    df_filtered['desc'] = df_filtered['desc'].apply(lambda x: x[:100] + '....' if isinstance(x, str) and len(x) > 120 else x)
    
    # 分页设置
    page = request.args.get('page', 1, type=int)
    per_page = 50  # 每页显示的记录数
    total = len(df_filtered)
    pages = math.ceil(total / per_page)
    start = (page - 1) * per_page
    end = start + per_page

    # 获取当前页的数据
    data = df_filtered.iloc[start:end].to_dict(orient='records')
    
    # 将DataFrame数据、列及样式、分页信息传递给HTML模板
    return render_template(
        'excel_viewer.html',
        data=data,
        columns=selected_columns,
        page=page,
        pages=pages,
        total=total,
        per_page=per_page
    )

@app.route('/publish', methods=['GET', 'POST'])
def publish():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        price = request.form.get('price')
        surroundings = request.form.get('surroundings')
        address = request.form.get('address')
        purchase_date = request.form.get('purchase_date')
        image_url = request.form.get('image_url', '')  # Default to empty string if not provided
        
        # Validate required fields
        if not all([title, content, price, surroundings, address, purchase_date]):
            return render_template('publish.html')
        
        try:
            db = get_db()
            db.execute('INSERT INTO posts (title, content, price, surroundings, address, purchase_date, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (title, content, price, surroundings, address, purchase_date, image_url))
            db.commit()
            return redirect(url_for('show_posts'))
        except Exception as e:
            return render_template('publish.html')
    
    return render_template('publish.html')

@app.route('/posts')
def show_posts():
    db = get_db()
    search_term = request.args.get('search', '')
    
    if search_term:
        query = '''SELECT * FROM posts 
                   WHERE title LIKE ? OR content LIKE ? OR address LIKE ? OR surroundings LIKE ? 
                   ORDER BY created_at DESC'''
        search_pattern = f'%{search_term}%'
        posts = db.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern)).fetchall()
    else:
        posts = db.execute('SELECT * FROM posts ORDER BY created_at DESC').fetchall()
    
    return render_template('posts.html', posts=posts, search_term=search_term)

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        price = request.form.get('price')
        surroundings = request.form.get('surroundings')
        address = request.form.get('address')
        purchase_date = request.form.get('purchase_date')
        image_url = request.form.get('image_url', '')
        
        if not all([title, content, price, surroundings, address, purchase_date]):
            return render_template('edit_post.html', post=post)
        
        try:
            db.execute('''UPDATE posts SET title=?, content=?, price=?, surroundings=?, 
                          address=?, purchase_date=?, image_url=? WHERE id=?''',
                       (title, content, price, surroundings, address, purchase_date, image_url, post_id))
            db.commit()
            return redirect(url_for('show_posts'))
        except Exception as e:
            return render_template('edit_post.html', post=post)
    
    return render_template('edit_post.html', post=post)

@app.route('/notes')
def show_notes():
    # 读取Excel文件
    df = pd.read_excel(r'data/xhs/1_search_comments.xlsx')
    
    # 选择要显示的列及其样式
    selected_columns = {
        'title': {
            'white-space': 'nowrap',
            'width': '150px'  # 设置列宽
        },
        'desc': {
            'white-space': 'normal',
            'width': '500px'  # 设置列宽
        },        
        'liked_count': {
            'white-space': 'nowrap',
            'width': '50px'  # 设置列宽
        },
        'note_url': {
            'white-space': 'nowrap',
            'width': '200px'  # 设置列宽
        }
    }

    # 只保留所选列的数据
    df_filtered = df[list(selected_columns.keys())].drop_duplicates(subset=['note_url'])
    
    # 处理 desc 列
    df_filtered['desc'] = df_filtered['desc'].apply(lambda x: x[:100] + '....' if isinstance(x, str) and len(x) > 120 else x)
    
    # 分页设置
    page = request.args.get('page', 1, type=int)
    per_page = 20  # 每页显示的记录数
    total = len(df_filtered)
    pages = math.ceil(total / per_page)
    start = (page - 1) * per_page
    end = start + per_page

    # 获取当前页的数据
    data = df_filtered.iloc[start:end].to_dict(orient='records')
    
    # 将DataFrame数据、列及样式、分页信息传递给HTML模板
    return render_template(
        'notes.html',
        data=data,
        columns=selected_columns,
        page=page,
        pages=pages,
        total=total,
        per_page=per_page
    )

@app.route('/comments/<path:note_url>')
def show_comments(note_url):
    # 读取Excel文件
    df = pd.read_excel(r'data/xhs/1_search_comments.xlsx')
    
    # 选择要显示的列及其样式
    selected_columns = {
        'ip_location': {
            'white-space': 'nowrap',
            'width': '50px'  # 设置列宽
        },
        'content': {
            'white-space': 'normal',
            'width': '100px'  # 设置列宽
        },
        'nickname': {
            'white-space': 'nowrap',
            'width': '150px'  # 设置列宽
        }
    }

    # 只保留所选列的数据，并筛选出对应note_url的评论
    df_filtered = df[df['note_url'] == note_url][list(selected_columns.keys())]
    
    # 处理 content 列
    df_filtered['content'] = df_filtered['content'].apply(lambda x: x[:100] + '....' if isinstance(x, str) and len(x) > 120 else x)
    
    # 分页设置
    page = request.args.get('page', 1, type=int)
    per_page = 50  # 每页显示的记录数
    total = len(df_filtered)
    pages = math.ceil(total / per_page)
    start = (page - 1) * per_page
    end = start + per_page

    # 获取当前页的数据
    data = df_filtered.iloc[start:end].to_dict(orient='records')
    
    # 将DataFrame数据、列及样式、分页信息传递给HTML模板
    return render_template(
        'comments.html',
        data=data,
        columns=selected_columns,
        page=page,
        pages=pages,
        total=total,
        per_page=per_page,
        note_url=note_url
    )

@app.route('/show_comments/<path:note_url>')
def show_comments_ajax(note_url):
    page = request.args.get('page', 1, type=int)
    # 读取Excel文件
    df = pd.read_excel(r'data/xhs/1_search_comments.xlsx')
    
    # 只保留所需列的数据，并筛选出对应note_url的评论
    df_filtered = df[df['note_url'] == note_url][['ip_location', 'content', 'nickname']]
    
    # 分页设置
    per_page = 10  # 每页显示的记录数
    total = len(df_filtered)
    pages = math.ceil(total / per_page)
    start = (page - 1) * per_page
    end = start + per_page

    # 获取当前页的数据
    comments = df_filtered.iloc[start:end].to_dict(orient='records')
    
    # 创建分页对象
    class Pagination:
        def __init__(self, page, per_page, total_count):
            self.page = page
            self.per_page = per_page
            self.total_count = total_count

        @property
        def pages(self):
            return int(math.ceil(self.total_count / float(self.per_page)))

        def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
            last = 0
            for num in range(1, self.pages + 1):
                if num <= left_edge or \
                   (num > self.page - left_current - 1 and num < self.page + right_current) or \
                   num > self.pages - right_edge:
                    if last + 1 != num:
                        yield None
                    yield num
                    last = num

    pagination = Pagination(page, per_page, total)

    # 返回JSON格式的响应，包含评论内容和分页HTML
    return jsonify({
        'content': render_template('comments_content.html', comments=comments),
        'pagination': render_template('comments_pagination.html', pagination=pagination)
    })






# 监控发散内容，来自ReverseSpider的截屏发散子功能
from flask import render_template_string
import os
import time

# 文件路径
FILE_PATH = r"D:\Code\GitProject\typoraNotes\Python\venv_20240825_172602-ReverseSpider\screenshot_result.txt"

# 存储上次修改时间和内容
last_modified_time = 0
last_content = ""

@app.route('/brainstorm')
def brainstorm():
    global last_modified_time, last_content
    
    try:
        # 获取文件的当前修改时间
        current_modified_time = os.path.getmtime(FILE_PATH)
        
        # 如果文件被修改，则更新内容
        if current_modified_time > last_modified_time:
            with open(FILE_PATH, 'r', encoding='utf-8') as file:
                content = file.read()
            last_modified_time = current_modified_time
            last_content = content
        else:
            content = last_content  # 文件未修改，使用上次的内容
    except Exception as e:
        content = last_content if last_content else f"Error reading file: {str(e)}"
        last_modified_time = 0

    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Brainstorm</title>
        <style>
            body {
                font-size: 16px;
                margin: 0;
                padding: 20px;
                font-family: Arial, sans-serif;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: #f9f9f9;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 20px;
                font-size: 24px;
            }
            .highlight {
                color: #e74c3c;
                font-weight: bold;
            }
            pre {
                background-color: #fff;
                padding: 15px;
                border-radius: 5px;
                border: 1px solid #ddd;
                white-space: pre-wrap;
                word-wrap: break-word;
                transition: background-color 0.5s ease;
            }
            @keyframes softPulse {
                0% { background-color: #fff; }
                50% { background-color: #e6f3ff; }
                100% { background-color: #fff; }
            }
            .updated {
                animation: softPulse 1.5s ease;
            }
            @keyframes titleFlash {
                0% { color: #333; }
                25% { color: #e74c3c; }
                50% { color: #3498db; }
                75% { color: #2ecc71; }
                100% { color: #333; }
            }
            .flash-title {
                animation: titleFlash 2s ease;
            }
        </style>
        <script>
            function checkForUpdates() {
                fetch('/brainstorm')
                    .then(response => response.text())
                    .then(html => {
                        var parser = new DOMParser();
                        var newDoc = parser.parseFromString(html, 'text/html');
                        var newContent = newDoc.getElementById('content').innerHTML;
                        var currentContent = document.getElementById('content').innerHTML;
                        if (newContent !== currentContent && newContent !== 'No updates') {
                            document.getElementById('content').innerHTML = newContent;
                            document.getElementById('content').classList.add('updated');
                            document.getElementById('title').classList.add('flash-title');
                            setTimeout(() => {
                                document.getElementById('content').classList.remove('updated');
                                document.getElementById('title').classList.remove('flash-title');
                            }, 2000);
                        }
                    });
            }
            setInterval(checkForUpdates, 5000);  // 每5秒检查一次更新
        </script>
    </head>
    <body>
        <div class="container">
            <h1 id="title">Brainstorm Content</h1>
            <pre id="content">{{ content | safe }}</pre>
        </div>
        <script>
            var contentElement = document.getElementById('content');
            var keywords = ['Brainstorm', 'Content', 'Error'];
            keywords.forEach(function(keyword) {
                var regex = new RegExp(keyword, 'gi');
                contentElement.innerHTML = contentElement.innerHTML.replace(regex, '<span class="highlight">$&</span>');
            });
        </script>
    </body>
    </html>
    '''
    return render_template_string(html, content=content)

# 监控发散内容，来自ReverseSpider的截屏发散子功能




app.config['DATABASE'] = DATABASE

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)

# TODO: 更新 requirements.txt，确保包含所有必要的依赖，包括 Flask 和 sqlite3
# TODO: 确保 xhs_data.db 文件有适当的读写权限
# TODO: 考虑添加错误处理和用户反馈机制
# TODO: 可能需要添加分页功能到 show_posts 路由，以处理大量帖子
# TODO: 考虑添加删除帖子的功能
# TODO: 实现用户认证系统，以控制谁可以发布内容

# 这些修改允许我们在测试时使用不同的数据库，而不影响正常环境的使用。
# 在运行测试时，测试数据会被写入 test_xhs_data.db，而正常使用时仍然使用 xhs_data.db。

# 其他 py 文件不需要修改，只要它们通过 get_db() 函数获取数据库连接。