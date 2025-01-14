import os

import cv2
from flask import Flask, request, jsonify, send_file, Response
from werkzeug.utils import secure_filename
import shutil
import config
from exts import cors
from flask.views import MethodView
from geoalchemy2.shape import to_shape
from flask_cors import CORS
from shapely.geometry import Point
from shapely.wkt import dumps
from flask_sqlalchemy import SQLAlchemy
from shapely.wkt import loads
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from datetime import datetime
import matplotlib.pyplot as plt
import io
import pandas as pd
from ultralytics import YOLO
import os
app = Flask(__name__)

os.environ["KMP_DUPLICATE_LIB_OK"]='True'
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://0.0.0.0:5173/"}})
# 设置上传文件的保存路径
UPLOAD_FOLDER = r'C:\Users\gaojack\PycharmProjects\flaskProject2\upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
# 加载模型（确保只加载一次）
model = YOLO(r'E:\Download\best3.pt')  # 加载你的YOLOv8模型


class Covers(db.Model):
    __tablename__ = "Covers"
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Location = db.Column(db.String(255), nullable=False)
    Coordinates = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    IssueDescription = db.Column(Text)
    Status = db.Column(Enum('good', 'circle', 'broke', 'lose', 'uncovered', '维修中'), nullable=False)
    ImageURL = db.Column(String(255))

    resolutions = db.relationship('Resolutions', back_populates='cover')


class Resolutions(db.Model):
    __tablename__ = 'Resolutions'
    ID = db.Column(Integer, primary_key=True)
    CoverID = db.Column(Integer, ForeignKey('Covers.ID'))
    ResolvedBy = db.Column(Integer, ForeignKey('Users.ID'))
    ResolvedAt = db.Column(DateTime, nullable=False, default=datetime.now)

    cover = db.relationship('Covers', back_populates='resolutions')
    user = db.relationship('User')


class User(db.Model):
    __tablename__ = 'Users'
    ID = db.Column(Integer, primary_key=True)
    Username = db.Column(String(255), nullable=False)
    Password = db.Column(String(255), nullable=False)
    Role = db.Column(Enum('管理员', '维修人员', '用户'), nullable=False)
    resolutions = db.relationship('Resolutions', back_populates='user')


@app.route('/')
def hello_world():
    return '耶耶耶！！！'


class CoversApi(MethodView):
    def get(self, cover_id):
        if not cover_id:
            covers = Covers.query.all()
            results = [{
                'ID': cover.ID,
                'Location': cover.Location,
                'Coordinates': to_shape(cover.Coordinates).wkt,  # Convert to WKT string
                'IssueDescription': cover.IssueDescription,
                'Status': cover.Status,
                'ImageURL': cover.ImageURL,
            } for cover in covers]
            return jsonify({
                'status': 'success',
                'message': '数据查询成功',
                'results': results
            })
        cover = Covers.query.get(cover_id)

        return jsonify({
            'status': 'success',
            'message': '数据查询成功!!!',
            'results': {
                'ID': cover.ID,
                'Location': cover.Location,
                'Coordinates': to_shape(cover.Coordinates).wkt,  # Convert to WKT string
                'IssueDescription': cover.IssueDescription,
                'Status': cover.Status,
                'ImageURL': cover.ImageURL,
            }
        })

    def post(self):
        form = request.json
        cover = Covers()
        cover.Location = form.get('Location')
        # 解析坐标数据并转换成合适的格式
        longitude, latitude = map(float, form.get('Coordinates').split(','))
        coordinates = Point(longitude, latitude)
        cover.Coordinates = dumps(coordinates)  # 将坐标数据转换成 WKT 格式
        cover.IssueDescription = form.get('IssueDescription')
        cover.Status = form.get('Status')
        cover.ImageURL = form.get('ImageURL')
        db.session.add(cover)
        db.session.commit()

        return {
            'status': 'success',
            'message': '数据添加成功'
        }

    def delete(self, cover_id):
        cover = Covers.query.get(cover_id)
        db.session.delete(cover)
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据删除成功'
        }

    def put(self, cover_id):
        cover = Covers.query.get(cover_id)
        cover.Location = request.json.get('Location')

        # 解析坐标数据并转换为合适的格式
        longitude, latitude = map(float, request.json.get('Coordinates').split(','))
        coordinates = Point(longitude, latitude)
        cover.Coordinates = dumps(coordinates)  # 将坐标数据转换为 WKT 格式

        cover.IssueDescription = request.json.get('IssueDescription')
        cover.Status = request.json.get('Status')
        cover.ImageURL = request.json.get('ImageURL')

        db.session.commit()

        return {
            'status': 'success',
            'message': '数据修改成功'
        }


cover_view = CoversApi.as_view('cover_api')
app.add_url_rule('/covers/', defaults={'cover_id': None},
                 view_func=cover_view, methods=['GET', ])
app.add_url_rule('/covers', view_func=cover_view, methods=['POST', ])
app.add_url_rule('/covers/<int:cover_id>', view_func=cover_view, methods=['GET', 'PUT', 'DELETE'])


@app.route('/covers/total')
def get_total_covers():
    total_covers = Covers.query.count()  # 假设使用 Covers 模型来代表井盖
    good_total = Covers.query.filter_by(Status='good').count()
    return jsonify({'total': total_covers, 'good_total': good_total})


@app.route('/covers/good')
def get_good_covers():
    good_covers = Covers.query.filter_by(Status='good').all()

    results = [{
        'ID': cover.ID,
        'Location': cover.Location,
        'Coordinates': to_shape(cover.Coordinates).wkt,  # Convert to WKT string
        'IssueDescription': cover.IssueDescription,
        'Status': cover.Status,
        'ImageURL': cover.ImageURL,
    } for cover in good_covers]
    return jsonify({
        'status': 'success',
        'message': '数据查询成功',
        'results': results
    })


@app.route('/covers/not_good')
def get_not_good_covers():
    not_good_covers = Covers.query.filter(Covers.Status != 'good').all()

    results = [{
        'ID': cover.ID,
        'Location': cover.Location,
        'Coordinates': to_shape(cover.Coordinates).wkt,  # Convert to WKT string
        'IssueDescription': cover.IssueDescription,
        'Status': cover.Status,
        'ImageURL': cover.ImageURL,
    } for cover in not_good_covers]
    return jsonify({
        'status': 'success',
        'message': '数据查询成功',
        'results': results
    })


@app.route('/plot')
def plot():
    # 假设你有三个模型的CSV文件，分别命名为 'model1.csv', 'model2.csv', 'model3.csv'
    models = ['yolov8x_olddataset', 'yolov8n_olddataset', 'yolov5x6_olddataset', 'yolov8n_newdataset','yolov8n-ours']

    # 创建一个新的图像
    fig, ax = plt.subplots()

    for model in models:
        # 读取每个模型的CSV文件
        df = pd.read_csv(f'E:\Download\{model}.csv')
        print(df.columns)
        # 绘制折线图，每个模型使用一种颜色，label参数用于图例
        if model == 'yolov5x6_olddataset':
            epoches = df['               epoch']
            map50e = df['     metrics/mAP_0.5']
            ax.plot(epoches, map50e, label=model)
        else:
            epochs = df['                  epoch']
            map50 = df['       metrics/mAP50(B)']
            ax.plot(epochs, map50, label=model)

    # 显示图例
    ax.legend()

    # 将生成的 matplotlib 图片转化为 IO 流
    output = io.BytesIO()
    fig.savefig(output, format='png')

    # 重新定位到流的开始位置
    output.seek(0)

    return send_file(output, mimetype='image/png')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    filename = secure_filename(file.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(image_path)

    # 使用YOLOv8进行预测
    results = model.predict(image_path, save=True)
    # 解析预测结果
    predictions = results[0].boxes
    classes = model.names[int(predictions.cls)]
    # 构建响应数据
    response_data = {
        "classes": classes,
        "image_url": f"http://localhost:5000/download/{filename}"  # 返回处理后图片的URL
    }
    return jsonify(response_data), 200




@app.route('/download/<string:filename>', methods=['GET'])
def download_file(filename):
    """提供一个下载处理后图片的路由"""
    # 构建处理后图片的完整路径
    predict_folder = os.path.join('runs', 'detect', 'predict')
    processed_image_path = os.path.join(predict_folder, filename)
    print(predict_folder)
    print(processed_image_path)
    # 发送文件之前，确保文件存在
    if not os.path.exists(processed_image_path):
        return "File not found.", 404

    # 使用send_file直接发送文件
    response = send_file(processed_image_path, as_attachment=True)

    # # 发送完毕后清理：删除predict文件夹
    # try:
    #     shutil.rmtree(predict_folder)
    # except OSError as e:
    #     print(f"Error: {predict_folder} : {e.strerror}")

    return response


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('Username')
    password = request.json.get('Password')

    user = User.query.filter_by(Username=username, Password=password).first()
    if user:
        return jsonify({'success': True,
                        'message': '登录成功',
                        'results': {
                            'USERID': user.ID,
                        }
                        })
    else:

        return jsonify({'success': False, 'message': '用户名或密码错误'})
def generate_frames(video_path):
    while True:  # 无限循环播放视频
        video_capture = cv2.VideoCapture(video_path)
        while True:
            success, frame = video_capture.read()
            if not success:
                break  # 视频播放完毕，跳出内层循环
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        video_capture.release()  # 释放视频文件

@app.route('/video_feed')
def video_feed():
    # 替换为您的视频文件路径
    return Response(generate_frames(r"C:\Users\gaojack\PycharmProjects\pythonProject10\runs\detect\predict17\1.avi"),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
