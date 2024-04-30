from flask import Flask, render_template, Blueprint


### 애플리케이션 팩토리 함수
def create_app():
    
    ### Flask Server 인스턴스 생성
    app = Flask(__name__)

    from .views import main_view
    from flask import Blueprint

    # Blueprint 등록
    app.register_blueprint(main_view.bp)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app


