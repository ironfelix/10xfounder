#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Веб-сервис для сравнения баз контактов
Flask приложение с загрузкой файлов и визуализацией результатов
"""

from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
import os
import pandas as pd
import json
from pathlib import Path
import uuid
from datetime import datetime
import sys

from contacts_comparator import ContactsComparator

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'  # Измените в продакшене!

# Поддержка работы в подпапке (например, /comparator)
app.config['APPLICATION_ROOT'] = '/comparator'

# Настройки
UPLOAD_FOLDER = Path('uploads')
RESULTS_FOLDER = Path('results')
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Создаем необходимые директории
UPLOAD_FOLDER.mkdir(exist_ok=True)
RESULTS_FOLDER.mkdir(exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    """Проверяет допустимость расширения файла"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_old_files(folder, max_age_hours=24):
    """Удаляет старые файлы"""
    try:
        current_time = datetime.now().timestamp()
        for file_path in folder.iterdir():
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > max_age_hours * 3600:
                    file_path.unlink()
    except Exception as e:
        print(f"Ошибка очистки: {e}")

@app.route('/comparator/')
@app.route('/comparator')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/comparator/upload', methods=['POST'])
def upload_files():
    """Обрабатывает загрузку и сравнение файлов"""
    try:
        # Проверяем наличие файлов
        if 'file1' not in request.files or 'file2' not in request.files:
            return jsonify({'error': 'Необходимо загрузить оба файла'}), 400
        
        file1 = request.files['file1']
        file2 = request.files['file2']
        
        # Проверяем что файлы выбраны
        if file1.filename == '' or file2.filename == '':
            return jsonify({'error': 'Выберите оба файла'}), 400
        
        # Проверяем расширения
        if not (allowed_file(file1.filename) and allowed_file(file2.filename)):
            return jsonify({'error': 'Поддерживаются только CSV и Excel файлы'}), 400
        
        # Получаем критерий поиска
        match_by = request.form.get('match_by', 'all')
        
        # Создаем уникальную сессию
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        
        session_folder = UPLOAD_FOLDER / session_id
        session_folder.mkdir(exist_ok=True)
        
        # Сохраняем файлы
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        
        filepath1 = session_folder / filename1
        filepath2 = session_folder / filename2
        
        file1.save(str(filepath1))
        file2.save(str(filepath2))
        
        # Выполняем сравнение
        comparator = ContactsComparator()
        
        # Загружаем файлы
        if not comparator.load_file(str(filepath1), file_number=1):
            return jsonify({'error': 'Ошибка загрузки первого файла'}), 400
        
        if not comparator.load_file(str(filepath2), file_number=2):
            return jsonify({'error': 'Ошибка загрузки второго файла'}), 400
        
        # Ищем дубликаты
        comparator.find_duplicates(match_by=match_by)
        
        # Готовим результаты
        results = {
            'session_id': session_id,
            'file1_name': filename1,
            'file2_name': filename2,
            'file1_count': len(comparator.file1_data),
            'file2_count': len(comparator.file2_data),
            'duplicates_count': len(comparator.duplicates),
            'unique_file1_count': len(comparator.unique_file1),
            'unique_file2_count': len(comparator.unique_file2),
            'match_by': match_by
        }
        
        # Добавляем статистику по типам совпадений
        if len(comparator.duplicates) > 0 and 'match_type' in comparator.duplicates.columns:
            match_types = comparator.duplicates['match_type'].value_counts().to_dict()
            results['match_types'] = match_types
        else:
            results['match_types'] = {}
        
        # Сохраняем примеры дубликатов
        if len(comparator.duplicates) > 0:
            duplicates_sample = comparator.duplicates.head(10).to_dict('records')
            # Очищаем от NaN
            for record in duplicates_sample:
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = None
            results['duplicates_sample'] = duplicates_sample
        else:
            results['duplicates_sample'] = []
        
        # Экспортируем результаты
        results_folder = RESULTS_FOLDER / session_id
        results_folder.mkdir(exist_ok=True)
        
        # Сохраняем Excel файлы
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if len(comparator.duplicates) > 0:
            duplicates_file = results_folder / f'duplicates_{timestamp}.xlsx'
            comparator.duplicates.to_excel(str(duplicates_file), index=False)
            results['duplicates_file'] = f'duplicates_{timestamp}.xlsx'
        
        if len(comparator.unique_file1) > 0:
            unique1_file = results_folder / f'unique_file1_{timestamp}.xlsx'
            comparator.unique_file1.to_excel(str(unique1_file), index=False)
            results['unique1_file'] = f'unique_file1_{timestamp}.xlsx'
        
        if len(comparator.unique_file2) > 0:
            unique2_file = results_folder / f'unique_file2_{timestamp}.xlsx'
            comparator.unique_file2.to_excel(str(unique2_file), index=False)
            results['unique2_file'] = f'unique_file2_{timestamp}.xlsx'
        
        # Сводный отчет
        summary_file = results_folder / f'comparison_summary_{timestamp}.xlsx'
        with pd.ExcelWriter(str(summary_file)) as writer:
            if len(comparator.duplicates) > 0:
                comparator.duplicates.to_excel(writer, sheet_name='Дубликаты', index=False)
            comparator.unique_file1.to_excel(writer, sheet_name='Уникальные_файл1', index=False)
            comparator.unique_file2.to_excel(writer, sheet_name='Уникальные_файл2', index=False)
            
            stats = pd.DataFrame({
                'Метрика': [
                    'Всего в файле 1',
                    'Всего в файле 2',
                    'Найдено дубликатов',
                    'Уникальных в файле 1',
                    'Уникальных в файле 2'
                ],
                'Значение': [
                    len(comparator.file1_data),
                    len(comparator.file2_data),
                    len(comparator.duplicates),
                    len(comparator.unique_file1),
                    len(comparator.unique_file2)
                ]
            })
            stats.to_excel(writer, sheet_name='Статистика', index=False)
        
        results['summary_file'] = f'comparison_summary_{timestamp}.xlsx'
        
        # Очищаем старые файлы
        cleanup_old_files(UPLOAD_FOLDER)
        cleanup_old_files(RESULTS_FOLDER)
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': f'Ошибка обработки: {str(e)}'}), 500

@app.route('/comparator/download/<session_id>/<filename>')
def download_file(session_id, filename):
    """Скачивает результирующий файл"""
    try:
        file_path = RESULTS_FOLDER / session_id / filename
        if file_path.exists():
            return send_file(str(file_path), as_attachment=True)
        else:
            return jsonify({'error': 'Файл не найден'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/comparator/health')
def health():
    """Проверка работоспособности сервиса"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

@app.errorhandler(413)
def request_entity_too_large(error):
    """Обработка слишком больших файлов"""
    return jsonify({'error': 'Файл слишком большой. Максимальный размер: 16MB'}), 413

if __name__ == '__main__':
    # Режим разработки
    app.run(debug=True, host='0.0.0.0', port=5000)
