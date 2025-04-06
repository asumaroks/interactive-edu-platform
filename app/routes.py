from flask import Blueprint, jsonify, request, send_file
import random
from openpyxl import Workbook
import os

bp = Blueprint('main', __name__)

# Хранилище данных в памяти
rooms = {}

# Генерация пятизначного кода комнаты
@bp.route('/create-room', methods=['POST'])
def create_room():
    room_code = random.randint(10000, 99999)
    rooms[room_code] = {"questions": [], "results": [], "active": False}
    print("Текущие комнаты:", rooms)  # Отладочный вывод
    return jsonify({"room_code": room_code})

# Создание теста
@bp.route('/create-test', methods=['POST'])
def create_test():
    data = request.json
    room_code = data.get("room_code")
    questions = data.get("questions")

    if not room_code or not questions:
        return jsonify({"error": "room_code и questions обязательны"}), 400

    if room_code not in rooms:
        return jsonify({"error": "Комната не найдена"}), 404

    # Обновляем только вопросы в комнате
    rooms[room_code]["questions"] = questions
    print(f"Обновлённые данные комнаты {room_code}: {rooms[room_code]}")
    return jsonify({"message": "Тест создан", "room_code": room_code})

# Подключение ученика к комнате
@bp.route('/join-room', methods=['POST'])
def join_room():
    data = request.json
    room_code = data.get("room_code")
    student_name = data.get("student_name")

    if not room_code or not student_name:
        return jsonify({"error": "room_code и student_name обязательны"}), 400

    if room_code not in rooms:
        return jsonify({"error": "Комната не найдена"}), 404

    # Добавляем ученика в результаты комнаты
    rooms[room_code]["results"].append({"name": student_name, "answers": {}})
    return jsonify({"message": f"{student_name} подключён к комнате {room_code}"})

# Прохождение теста учеником
@bp.route('/submit-answers', methods=['POST'])
def submit_answers():
    data = request.json
    room_code = data.get("room_code")
    student_name = data.get("student_name")
    answers = data.get("answers")

    if not room_code or not student_name or not answers:
        return jsonify({"error": "room_code, student_name и answers обязательны"}), 400

    if room_code not in rooms:
        return jsonify({"error": "Комната не найдена"}), 404

    # Обновляем ответы ученика
    for student in rooms[room_code]["results"]:
        if student["name"] == student_name:
            student["answers"] = answers  # Сохраняем ответы
            break
    else:
        return jsonify({"error": "Ученик не найден"}), 404

    return jsonify({"message": "Ответы сохранены"})

# Начало теста
@bp.route('/start-test', methods=['POST'])
def start_test():
    data = request.json
    room_code = data.get("room_code")

    if not room_code:
        return jsonify({"error": "room_code обязателен"}), 400

    if room_code not in rooms:
        return jsonify({"error": "Комната не найдена"}), 404

    # Помечаем комнату как активную
    rooms[room_code]["active"] = True
    return jsonify({"message": f"Тест в комнате {room_code} начат"})

# Экспорт результатов в Excel
@bp.route('/export-results', methods=['GET'])
def export_results():
    room_code = request.args.get("room_code")

    if not room_code:
        return jsonify({"error": "room_code обязателен"}), 400

    try:
        room_code = int(room_code)  # Приведение room_code к числу
    except ValueError:
        return jsonify({"error": "room_code должен быть числом"}), 400

    if room_code not in rooms:
        return jsonify({"error": "Комната не найдена"}), 404

    # Проверяем, есть ли результаты
    if not rooms[room_code]["results"]:
        return jsonify({"error": "Нет результатов для экспорта"}), 400

    # Создаём Excel-файл
    wb = Workbook()
    ws = wb.active
    ws.title = "Результаты"

    # Заголовки
    ws.append(["Имя ученика", "Ответы"])

    # Добавляем данные
    for student in rooms[room_code]["results"]:
        ws.append([student["name"], str(student["answers"])])

    # Сохраняем файл
    file_path = os.path.join(os.getcwd(), f"results_{room_code}.xlsx")
    try:
        print(f"Сохраняем файл: {file_path}")
        wb.save(file_path)
        print(f"Файл сохранён: {os.path.exists(file_path)}")
    except Exception as e:
        return jsonify({"error": f"Ошибка при сохранении файла: {str(e)}"}), 500

    # Проверяем, что файл существует перед отправкой
    if not os.path.exists(file_path):
        return jsonify({"error": f"Файл {file_path} не найден"}), 500

    try:
        # Отправляем файл клиенту
        return send_file(file_path, as_attachment=True, download_name=os.path.basename(file_path), max_age=0)
    except Exception as e:
        return jsonify({"error": f"Ошибка при отправке файла: {str(e)}"}), 500
    finally:
        # Удаляем файл после отправки
        try:
            os.remove(file_path)
            print(f"Файл {file_path} успешно удалён")
        except PermissionError:
            print(f"Файл {file_path} занят другим процессом и не может быть удалён")