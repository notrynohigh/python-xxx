#coding=utf-8
import os
# 渲染HTML模板，从flask使用请求对象，访问通过POST发送的数据。
# 重定向和url_for 用于一旦上传成功，重定向用户，
# send_from_directory有助于我们在浏览器send/show用户上传的文件。
from flask import Flask, render_template, request, send_from_directory
from werkzeug import secure_filename
from ctypes import *


# 初始化Flask应用程序
app = Flask(__name__)
# 上传文件存放的路径
app.config['UPLOAD_FOLDER'] = 'uploads/'
# 设置允许上传文件的扩展名(可以自行添加)
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


dll = cdll.LoadLibrary('aiyandll.dll')

# 判断文件名带点并且扩展名是允许的名称
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


# 该路由显示一个表单，jQuery执行一个AJAX request
# 装载jQuery，执行请求，执行上传操作
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
         # 保存文件名到列表，后面我们需要使用它
        # 重定向用户到uploaded_file路由，它
        # 在浏览器上显示基本的文件上传信息
    dll.AiYanPR.argtypes = [c_char_p]
    dll.AiYanPR.restype = c_char_p
    sBuf = app.config['UPLOAD_FOLDER'] + filename
    print(sBuf)
    res = dll.AiYanPR(sBuf)
    return res


# 该路由需要一个包含文件名的参数。
# 然后定位上传目录的文件，在浏览器上显示出来，
# 因此用户上传一个图像，那么这个图像在上传后可以显示
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(
        host="192.168.1.111",
        port=int("80"),
        debug=True
    )