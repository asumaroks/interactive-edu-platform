import os
from flask import Flask, render_template
from app.routes import bp  # Импортируем Blueprint

print("Текущая рабочая директория:", os.getcwd())
print("Файл index.html существует:", os.path.exists('templates/index.html'))

app = Flask(__name__, template_folder='templates')  # Указываем путь к папке templates
app.register_blueprint(bp)  # Регистрируем Blueprint

print(app.url_map)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)