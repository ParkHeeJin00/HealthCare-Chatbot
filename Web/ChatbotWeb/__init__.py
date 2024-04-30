# 모듈 로딩
from flask import Flask, request, jsonify   


def create_app():
    # Flask 인스턴스 생성
    app = Flask(__name__)

    # 설정 내용 로딩
    app.config.from_pyfile('config.py') 

    # 라우팅 처리
    @app.route('/keyboard')
    def keyboard():
        return jsonify({
            'type': 'text'
        })
    
    @app.route('/message', methods=['POST'])    
    def message():
        data = request.json
        content = data['content']
        return jsonify({
            'message': {
                'text': content
            }
        })  
    
    return app
