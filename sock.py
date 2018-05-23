#coding=utf-8
import os

from flask import Flask, render_template, request, send_from_directory
from werkzeug import secure_filename
from ctypes import *


# 初始化Flask应用程序
app = Flask(__name__)
# 上传文件存放的路径
app.config['UPLOAD_FOLDER'] = 'uploads/'
# 设置允许上传文件的扩展名(可以自行添加)
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


dll = CDLL('aiyandll.dll')

# 判断文件名带点并且扩展名是允许的名称
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']



@app.route('/')
def index():
    return render_template('index.html')


# 这个路由处理文件上传
@app.route('/upload', methods=['POST'])
def upload():
    # 获得上传文件的名称
    uploaded_files = request.files.get('car')

    if uploaded_files and allowed_file(uploaded_files.filename):
        # 产生安全的文件名，移除不支持的字符
        filename = secure_filename(uploaded_files.filename)
         # 移动文件，从临时目录到我们创建的上传目录
        uploaded_files.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    dll.AiYanPR.argtypes = [c_char_p, c_char_p]
    print filename
    sBuf = b"E:\\Bean_workshop\\doc\\aiyan\\python-xxx\\uploads\\" + filename
    res = b"abcdefgaa"
    dll.AiYanPR(sBuf, res)
    return res.decode('gbk')



if __name__ == '__main__':
    app.run(
        host="192.168.1.111",
        port=int("80"),
        debug=True
    )