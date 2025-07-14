from flask import Flask, render_template, render_template_string, request, jsonify
import pandas as pd
import math
import mysql.connector
from datetime import datetime
import os

# Flask 应用初始化
app = Flask(__name__)

# MySQL 数据库配置
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '123456')
MYSQL_DB = os.environ.get('MYSQL_DB', 'media_crawler')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))

# 配置数据库连接
def get_db():
    db = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        port=MYSQL_PORT
    )
    return db

# 根目录：显示主要功能导航
@app.route('/')
def home():
    return render_template('home.html')

# 显示数据库表列表
@app.route('/tables')
def list_tables():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()
        return render_template('tables.html', tables=tables)
    except Exception as e:
        return f"Error: {str(e)}"

# 显示指定表的内容
@app.route('/table/<table_name>', methods=['GET', 'POST'])
def show_table(table_name):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        # 定义预设维度
        preset_dimensions = {
            'desc_liked_count': ['title', 'nickname', 'desc', 'liked_count', 'note_url', 'last_update_time']
        }

        # 获取列选择和排序参数
        selected_preset = request.args.get('preset', None)  # 获取预设维度
        selected_columns = request.form.getlist('columns')  # 从表单获取选中的列
        sort_column = request.args.get('sort', None)  # 获取排序列
        sort_order = request.args.get('order', 'asc')  # 获取排序顺序

        # 获取表的所有列
        cursor.execute(f"DESCRIBE {table_name}")
        all_columns = [column['Field'] for column in cursor.fetchall()]

        # 如果选择了预设维度，使用预设列
        if selected_preset in preset_dimensions:
            selected_columns = preset_dimensions[selected_preset]

        # 如果没有选择列，默认显示所有列
        if not selected_columns:
            selected_columns = all_columns

        # 构建查询语句
        columns_str = ', '.join([f"`{col}`" for col in selected_columns])
        query = f"SELECT {columns_str} FROM `{table_name}`"
        if selected_preset == 'desc_liked_count':
            query += " ORDER BY `last_update_time` DESC, `liked_count` DESC"
        elif sort_column and sort_column in selected_columns:
            query += f" ORDER BY `{sort_column}` {sort_order.upper()}"
        query += " LIMIT 100"

        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

        # Multiply the 'desc' content by 5 for testing
        for row in rows:
            if 'desc' in row:
                row['desc'] = row['desc'] * 5

        return render_template(
            'table_view.html',
            table_name=table_name,
            rows=rows,
            all_columns=all_columns,
            selected_columns=selected_columns,
            sort_column=sort_column,
            sort_order=sort_order,
            preset_dimensions=preset_dimensions
        )
    except Exception as e:
        return f"Error: {str(e)}"

# 监控文件内容更新
FILE_PATH = r"D:\Code\GitProject\typoraNotes\Python\venv_20240825_172602-ReverseSpider\screenshot_result.txt"
last_modified_time = 0
last_content = ""

@app.route('/brainstorm')
def brainstorm():
    global last_modified_time, last_content
    try:
        current_modified_time = os.path.getmtime(FILE_PATH)
        if current_modified_time > last_modified_time:
            with open(FILE_PATH, 'r', encoding='utf-8') as file:
                content = file.read()
            last_modified_time = current_modified_time
            last_content = content
        else:
            content = last_content
    except Exception as e:
        content = last_content if last_content else f"Error reading file: {str(e)}"
        last_modified_time = 0
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head><title>Brainstorm</title></head>
    <body>
        <h1>Brainstorm Content</h1>
        <pre>{{ content | safe }}</pre>
    </body>
    </html>
    ''', content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)