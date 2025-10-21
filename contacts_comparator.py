#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сравнитель баз контактов
Находит дубликаты и пересечения между двумя файлами с контактами
"""

import pandas as pd
import numpy as np
from pathlib import Path
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ContactsComparator:
    def __init__(self):
        self.file1_data = None
        self.file2_data = None
        self.file1_name = None
        self.file2_name = None
        self.duplicates = None
        self.unique_file1 = None
        self.unique_file2 = None
    
    def load_file(self, file_path, file_number=1):
        """
        Загружает файл с контактами (Excel или CSV)
        file_number: 1 для первого файла, 2 для второго
        """
        file_path = Path(file_path)
        
        try:
            # Определяем тип файла
            if file_path.suffix.lower() in ['.xlsx', '.xls']:
                data = pd.read_excel(file_path)
                print(f"✅ Excel файл загружен: {file_path.name}")
            elif file_path.suffix.lower() == '.csv':
                # Пробуем разные кодировки
                encodings = ['utf-8', 'cp1251', 'windows-1251', 'iso-8859-1']
                for encoding in encodings:
                    try:
                        data = pd.read_csv(file_path, encoding=encoding)
                        print(f"✅ CSV файл загружен: {file_path.name} (кодировка: {encoding})")
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    raise ValueError("Не удалось определить кодировку CSV файла")
            else:
                raise ValueError(f"Неподдерживаемый формат файла: {file_path.suffix}")
            
            # Сохраняем данные
            if file_number == 1:
                self.file1_data = data
                self.file1_name = file_path.name
                print(f"📊 Файл 1: {len(data)} записей, колонки: {list(data.columns)}")
            else:
                self.file2_data = data
                self.file2_name = file_path.name
                print(f"📊 Файл 2: {len(data)} записей, колонки: {list(data.columns)}")
            
            return data
            
        except Exception as e:
            print(f"❌ Ошибка при загрузке файла: {e}")
            return None
    
    def normalize_phone(self, phone):
        """
        Нормализует номер телефона для сравнения
        Убирает все символы кроме цифр
        """
        if pd.isna(phone):
            return None
        
        phone_str = str(phone)
        # Убираем все символы кроме цифр
        digits = re.sub(r'\D', '', phone_str)
        
        # Если номер начинается с 8, заменяем на 7
        if digits.startswith('8') and len(digits) == 11:
            digits = '7' + digits[1:]
        
        # Если номер 10 цифр, добавляем 7 в начало
        if len(digits) == 10:
            digits = '7' + digits
        
        return digits if digits else None
    
    def normalize_email(self, email):
        """
        Нормализует email для сравнения
        Приводит к нижнему регистру и убирает пробелы
        """
        if pd.isna(email):
            return None
        
        email_str = str(email).strip().lower()
        return email_str if '@' in email_str else None
    
    def normalize_name(self, name):
        """
        Нормализует имя для сравнения
        Приводит к нижнему регистру и убирает лишние пробелы
        """
        if pd.isna(name):
            return None
        
        name_str = str(name).strip().lower()
        # Убираем множественные пробелы
        name_str = re.sub(r'\s+', ' ', name_str)
        return name_str if name_str else None
    
    def detect_columns(self, data):
        """
        Автоматически определяет колонки с именем, email и телефоном
        """
        columns = {
            'name': None,
            'email': None,
            'phone': None
        }
        
        # Поиск колонки с именем
        name_patterns = ['имя', 'name', 'фио', 'fullname', 'full_name', 'full name', 'ф.и.о']
        for col in data.columns:
            if any(pattern in col.lower() for pattern in name_patterns):
                columns['name'] = col
                break
        
        # Поиск колонки с email
        email_patterns = ['email', 'e-mail', 'mail', 'почта', 'емейл', 'имейл']
        for col in data.columns:
            if any(pattern in col.lower() for pattern in email_patterns):
                columns['email'] = col
                break
        
        # Поиск колонки с телефоном
        phone_patterns = ['телефон', 'phone', 'тел', 'tel', 'mobile', 'мобильный']
        for col in data.columns:
            if any(pattern in col.lower() for pattern in phone_patterns):
                columns['phone'] = col
                break
        
        return columns
    
    def prepare_data(self, data, columns=None):
        """
        Подготавливает данные для сравнения
        Нормализует имена, email и телефоны
        """
        if columns is None:
            columns = self.detect_columns(data)
        
        print(f"\n🔍 Обнаруженные колонки:")
        print(f"   Имя: {columns['name']}")
        print(f"   Email: {columns['email']}")
        print(f"   Телефон: {columns['phone']}")
        
        # Создаем копию данных
        prepared = data.copy()
        
        # Нормализуем данные
        if columns['name']:
            prepared['normalized_name'] = prepared[columns['name']].apply(self.normalize_name)
        
        if columns['email']:
            prepared['normalized_email'] = prepared[columns['email']].apply(self.normalize_email)
        
        if columns['phone']:
            prepared['normalized_phone'] = prepared[columns['phone']].apply(self.normalize_phone)
        
        return prepared, columns
    
    def find_duplicates(self, match_by='all'):
        """
        Находит дубликаты между двумя файлами
        match_by: 'email', 'phone', 'name', 'all' (любое совпадение)
        """
        if self.file1_data is None or self.file2_data is None:
            print("❌ Загрузите оба файла перед сравнением")
            return None
        
        print("\n🔍 Поиск дубликатов...")
        
        # Подготавливаем данные
        data1, cols1 = self.prepare_data(self.file1_data)
        data2, cols2 = self.prepare_data(self.file2_data)
        
        # Добавляем источник данных
        data1['source'] = self.file1_name
        data2['source'] = self.file2_name
        
        duplicates = []
        
        # Поиск дубликатов по разным критериям
        if match_by in ['email', 'all']:
            if 'normalized_email' in data1.columns and 'normalized_email' in data2.columns:
                email_matches = pd.merge(
                    data1, data2,
                    on='normalized_email',
                    how='inner',
                    suffixes=('_file1', '_file2')
                )
                email_matches = email_matches[email_matches['normalized_email'].notna()]
                if len(email_matches) > 0:
                    email_matches['match_type'] = 'Email'
                    duplicates.append(email_matches)
        
        if match_by in ['phone', 'all']:
            if 'normalized_phone' in data1.columns and 'normalized_phone' in data2.columns:
                phone_matches = pd.merge(
                    data1, data2,
                    on='normalized_phone',
                    how='inner',
                    suffixes=('_file1', '_file2')
                )
                phone_matches = phone_matches[phone_matches['normalized_phone'].notna()]
                if len(phone_matches) > 0:
                    phone_matches['match_type'] = 'Телефон'
                    duplicates.append(phone_matches)
        
        if match_by in ['name', 'all']:
            if 'normalized_name' in data1.columns and 'normalized_name' in data2.columns:
                name_matches = pd.merge(
                    data1, data2,
                    on='normalized_name',
                    how='inner',
                    suffixes=('_file1', '_file2')
                )
                name_matches = name_matches[name_matches['normalized_name'].notna()]
                if len(name_matches) > 0:
                    name_matches['match_type'] = 'Имя'
                    duplicates.append(name_matches)
        
        # Объединяем все найденные дубликаты
        if duplicates:
            self.duplicates = pd.concat(duplicates, ignore_index=True)
            # Убираем полные дубликаты
            self.duplicates = self.duplicates.drop_duplicates()
        else:
            self.duplicates = pd.DataFrame()
        
        # Находим уникальные записи
        if 'normalized_email' in data1.columns and 'normalized_email' in data2.columns:
            duplicate_emails = set(self.duplicates['normalized_email'].dropna().unique()) if not self.duplicates.empty else set()
            self.unique_file1 = data1[~data1['normalized_email'].isin(duplicate_emails)]
            self.unique_file2 = data2[~data2['normalized_email'].isin(duplicate_emails)]
        else:
            self.unique_file1 = data1
            self.unique_file2 = data2
        
        return self.duplicates
    
    def generate_report(self):
        """
        Генерирует детальный отчет о сравнении
        """
        if self.duplicates is None:
            print("❌ Сначала выполните поиск дубликатов")
            return
        
        print("\n" + "="*60)
        print("📊 ОТЧЕТ О СРАВНЕНИИ КОНТАКТОВ")
        print("="*60)
        
        print(f"\n📁 Файл 1: {self.file1_name}")
        print(f"   Всего контактов: {len(self.file1_data)}")
        
        print(f"\n📁 Файл 2: {self.file2_name}")
        print(f"   Всего контактов: {len(self.file2_data)}")
        
        print(f"\n🔄 РЕЗУЛЬТАТЫ СРАВНЕНИЯ:")
        print(f"   Найдено дубликатов: {len(self.duplicates)}")
        print(f"   Уникальных в файле 1: {len(self.unique_file1)}")
        print(f"   Уникальных в файле 2: {len(self.unique_file2)}")
        
        if len(self.duplicates) > 0:
            print(f"\n📌 ТИПЫ СОВПАДЕНИЙ:")
            match_types = self.duplicates['match_type'].value_counts()
            for match_type, count in match_types.items():
                print(f"   {match_type}: {count}")
            
            print(f"\n👥 ПРИМЕРЫ ДУБЛИКАТОВ (первые 10):")
            print("-" * 60)
            
            # Определяем какие колонки показывать
            display_cols = []
            for col in self.duplicates.columns:
                if 'normalized' not in col and col not in ['source_file1', 'source_file2', 'match_type']:
                    display_cols.append(col)
            
            # Показываем первые 10 дубликатов
            for idx, row in self.duplicates.head(10).iterrows():
                print(f"\nДубликат #{idx + 1} (совпадение: {row['match_type']})")
                # Ищем колонки из первого и второго файла
                for col in display_cols[:5]:  # Показываем первые 5 колонок
                    if not pd.isna(row.get(col)):
                        print(f"   {col}: {row.get(col)}")
        else:
            print("\n✅ Дубликаты не найдены!")
        
        # Статистика
        total_contacts = len(self.file1_data) + len(self.file2_data)
        unique_contacts = len(self.unique_file1) + len(self.unique_file2) + len(self.duplicates)
        
        print(f"\n📈 СТАТИСТИКА:")
        print(f"   Всего контактов в обоих файлах: {total_contacts}")
        print(f"   Уникальных контактов: {unique_contacts}")
        print(f"   Процент дубликатов: {(len(self.duplicates) / total_contacts * 100):.1f}%")
    
    def create_visualization(self):
        """
        Создает визуализацию результатов сравнения
        """
        if self.duplicates is None:
            print("❌ Сначала выполните поиск дубликатов")
            return
        
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            # Настройка для русского текста
            plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial Unicode MS', 'Lucida Grande']
            plt.rcParams['axes.unicode_minus'] = False
            
            print("📊 Создание визуализации...")
            
            # Создаем фигуру с графиками
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle('Анализ сравнения баз контактов', fontsize=16, fontweight='bold')
            
            # 1. Круговая диаграмма общего распределения
            labels = ['Дубликаты', f'Уникальные\n({self.file1_name})', f'Уникальные\n({self.file2_name})']
            sizes = [len(self.duplicates), len(self.unique_file1), len(self.unique_file2)]
            colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
            
            axes[0, 0].pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
            axes[0, 0].set_title('Распределение контактов')
            
            # 2. Столбчатая диаграмма по файлам
            files_data = pd.DataFrame({
                'Файл': [self.file1_name, self.file2_name],
                'Всего': [len(self.file1_data), len(self.file2_data)],
                'Уникальных': [len(self.unique_file1), len(self.unique_file2)]
            })
            
            x = np.arange(len(files_data))
            width = 0.35
            
            axes[0, 1].bar(x - width/2, files_data['Всего'], width, label='Всего', color='#95e1d3')
            axes[0, 1].bar(x + width/2, files_data['Уникальных'], width, label='Уникальных', color='#38ada9')
            axes[0, 1].set_xlabel('Файлы')
            axes[0, 1].set_ylabel('Количество контактов')
            axes[0, 1].set_title('Сравнение файлов')
            axes[0, 1].set_xticks(x)
            axes[0, 1].set_xticklabels(['Файл 1', 'Файл 2'])
            axes[0, 1].legend()
            
            # 3. Распределение дубликатов по типам совпадений
            if len(self.duplicates) > 0 and 'match_type' in self.duplicates.columns:
                match_counts = self.duplicates['match_type'].value_counts()
                axes[1, 0].bar(match_counts.index, match_counts.values, color='#e056fd')
                axes[1, 0].set_xlabel('Тип совпадения')
                axes[1, 0].set_ylabel('Количество')
                axes[1, 0].set_title('Дубликаты по типам совпадений')
                axes[1, 0].tick_params(axis='x', rotation=45)
            else:
                axes[1, 0].text(0.5, 0.5, 'Дубликаты не найдены', 
                               ha='center', va='center', fontsize=12)
                axes[1, 0].set_title('Дубликаты по типам совпадений')
            
            # 4. Статистика в виде текста
            total = len(self.file1_data) + len(self.file2_data)
            unique_total = len(self.unique_file1) + len(self.unique_file2) + len(self.duplicates)
            duplicate_pct = (len(self.duplicates) / total * 100) if total > 0 else 0
            
            stats_text = f"""
СТАТИСТИКА СРАВНЕНИЯ

Файл 1: {self.file1_name}
  • Всего контактов: {len(self.file1_data):,}
  • Уникальных: {len(self.unique_file1):,}

Файл 2: {self.file2_name}
  • Всего контактов: {len(self.file2_data):,}
  • Уникальных: {len(self.unique_file2):,}

ИТОГО:
  • Найдено дубликатов: {len(self.duplicates):,}
  • Процент дубликатов: {duplicate_pct:.1f}%
  • Всего уникальных: {unique_total:,}
            """
            
            axes[1, 1].text(0.1, 0.9, stats_text, fontsize=10, verticalalignment='top',
                           fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            axes[1, 1].axis('off')
            
            plt.tight_layout()
            
            # Сохраняем график
            output_path = Path('contacts_comparison_chart.png')
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"✅ Визуализация сохранена: {output_path}")
            
            plt.show()
            
        except ImportError:
            print("⚠️ Для визуализации установите matplotlib и seaborn:")
            print("   pip install matplotlib seaborn")
        except Exception as e:
            print(f"❌ Ошибка при создании визуализации: {e}")
    
    def export_results(self, output_dir='.'):
        """
        Экспортирует результаты в Excel файлы
        """
        if self.duplicates is None:
            print("❌ Сначала выполните поиск дубликатов")
            return
        
        output_dir = Path(output_dir)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        try:
            # Экспортируем дубликаты
            if len(self.duplicates) > 0:
                duplicates_file = output_dir / f'duplicates_{timestamp}.xlsx'
                self.duplicates.to_excel(duplicates_file, index=False)
                print(f"✅ Дубликаты сохранены: {duplicates_file}")
            
            # Экспортируем уникальные контакты из файла 1
            if len(self.unique_file1) > 0:
                unique1_file = output_dir / f'unique_file1_{timestamp}.xlsx'
                self.unique_file1.to_excel(unique1_file, index=False)
                print(f"✅ Уникальные из файла 1: {unique1_file}")
            
            # Экспортируем уникальные контакты из файла 2
            if len(self.unique_file2) > 0:
                unique2_file = output_dir / f'unique_file2_{timestamp}.xlsx'
                self.unique_file2.to_excel(unique2_file, index=False)
                print(f"✅ Уникальные из файла 2: {unique2_file}")
            
            # Создаем сводный отчет
            summary_file = output_dir / f'comparison_summary_{timestamp}.xlsx'
            with pd.ExcelWriter(summary_file) as writer:
                if len(self.duplicates) > 0:
                    self.duplicates.to_excel(writer, sheet_name='Дубликаты', index=False)
                self.unique_file1.to_excel(writer, sheet_name='Уникальные_файл1', index=False)
                self.unique_file2.to_excel(writer, sheet_name='Уникальные_файл2', index=False)
                
                # Добавляем статистику
                stats = pd.DataFrame({
                    'Метрика': [
                        'Всего в файле 1',
                        'Всего в файле 2',
                        'Найдено дубликатов',
                        'Уникальных в файле 1',
                        'Уникальных в файле 2'
                    ],
                    'Значение': [
                        len(self.file1_data),
                        len(self.file2_data),
                        len(self.duplicates),
                        len(self.unique_file1),
                        len(self.unique_file2)
                    ]
                })
                stats.to_excel(writer, sheet_name='Статистика', index=False)
            
            print(f"✅ Сводный отчет сохранен: {summary_file}")
            
        except Exception as e:
            print(f"❌ Ошибка при экспорте: {e}")

def main():
    """
    Пример использования
    """
    print("🔍 Сравнитель баз контактов")
    print("="*40)
    print("\n📝 Инструкция:")
    print("1. Загрузите два файла с контактами (Excel или CSV)")
    print("2. Программа автоматически найдет дубликаты")
    print("3. Получите детальный отчет и экспортируйте результаты")
    print("\n💡 Пример использования:")
    print("-"*40)
    print("comparator = ContactsComparator()")
    print("comparator.load_file('contacts1.xlsx', file_number=1)")
    print("comparator.load_file('contacts2.xlsx', file_number=2)")
    print("comparator.find_duplicates(match_by='all')")
    print("comparator.generate_report()")
    print("comparator.create_visualization()")
    print("comparator.export_results()")
    print("-"*40)
    
    return ContactsComparator()

if __name__ == "__main__":
    comparator = main()
