import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import pyperclip
import os
import sys
from PIL import Image, ImageDraw
import threading

# Попытка импортировать pystray
try:
    import pystray
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False
    print("pystray не установлен. Установите: pip install pystray pillow")

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер паролей")
        self.root.geometry("950x650")
        
        # Иконка для трея
        self.icon_image = self.create_icon()
        
        # Настройка системного трея
        self.setup_system_tray()
        
        # Путь к файлу по умолчанию
        self.default_file = "Password.xlsx"
        self.work_file = "Работа.xlsx"
        self.data = []
        
        self.create_widgets()
        self.load_default_file()
        
        # Флаг для отслеживания состояния трея
        self.tray_icon_running = False
        self.tray_icon_instance = None
    
    def create_icon(self):
        """Создание иконки для системного трея"""
        # Создаем простую иконку 64x64
        image = Image.new('RGB', (64, 64), color='#2196F3')
        draw = ImageDraw.Draw(image)
        
        # Рисуем замок
        draw.rectangle([20, 25, 44, 45], fill='white', outline='black')
        draw.rectangle([28, 15, 36, 25], fill='white', outline='black')
        
        return image
    
    def setup_system_tray(self):
        """Настройка системного трея"""
        if TRAY_AVAILABLE:
            # Создаем меню для иконки в трее
            menu = pystray.Menu(
                pystray.MenuItem("Открыть", self.restore_from_tray),
                pystray.MenuItem("Выход", self.quit_application)
            )
            
            self.tray_icon = pystray.Icon("PasswordManager", self.icon_image, "Менеджер паролей", menu)
        else:
            # Резервный вариант - контекстное меню
            self.tray_menu = tk.Menu(self.root, tearoff=0)
            self.tray_menu.add_command(label="Открыть", command=self.restore_from_tray)
            self.tray_menu.add_separator()
            self.tray_menu.add_command(label="Выход", command=self.quit_application)
            self.root.bind("<Button-3>", self.show_context_menu)
        
        # Обработка закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
    
    def minimize_to_tray(self):
        """Сворачивание в трей"""
        if TRAY_AVAILABLE:
            # Скрываем главное окно
            self.root.withdraw()
            
            # Запускаем иконку в трее в отдельном потоке
            if not self.tray_icon_running:
                self.tray_thread = threading.Thread(target=self.run_tray_icon, daemon=True)
                self.tray_thread.start()
                self.tray_icon_running = True
        else:
            # Резервный вариант - просто скрываем окно
            self.root.withdraw()
    
    def minimize_to_tray_button(self):
        """Сворачивание в трей через кнопку"""
        self.minimize_to_tray()
    
    def run_tray_icon(self):
        """Запуск иконки в трее"""
        try:
            # Создаем меню для иконки в трее
            menu = pystray.Menu(
                pystray.MenuItem("Открыть", self.restore_from_tray),
                pystray.MenuItem("Выход", self.quit_application)
            )
            
            # Создаем новую иконку
            self.tray_icon_instance = pystray.Icon("PasswordManager", self.icon_image, "Менеджер паролей", menu)
            
            # Запускаем иконку
            self.tray_icon_instance.run()
            
        except Exception as e:
            print(f"Ошибка запуска иконки в трее: {e}")
    
    def restore_from_tray(self, icon=None, item=None):
        """Восстановление из трея"""
        # Показываем главное окно
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        
        # Останавливаем иконку в трее если она есть
        if hasattr(self, 'tray_icon_instance') and self.tray_icon_instance:
            try:
                self.tray_icon_instance.stop()
            except:
                pass
            self.tray_icon_running = False
            self.tray_icon_instance = None
    
    def quit_application(self, icon=None, item=None):
        """Выход из приложения"""
        # Останавливаем иконку в трее если она есть
        if hasattr(self, 'tray_icon_instance') and self.tray_icon_instance:
            try:
                self.tray_icon_instance.stop()
            except:
                pass
        
        self.root.destroy()
        sys.exit()
    
    def show_context_menu(self, event):
        """Показ контекстного меню (резервный вариант)"""
        if not TRAY_AVAILABLE:
            try:
                self.tray_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.tray_menu.grab_release()
    
    def open_password_file(self):
        """Открыть файл Password.xlsx"""
        if os.path.exists(self.default_file):
            self.load_data_from_file(self.default_file)
            self.file_label.config(text=f"Файл: {self.default_file}")
        else:
            messagebox.showwarning("Файл не найден", f"Файл {self.default_file} не найден в папке программы.")
    
    def open_work_file(self):
        """Открыть файл Работа.xlsx"""
        if os.path.exists(self.work_file):
            self.load_data_from_file(self.work_file)
            self.file_label.config(text=f"Файл: {self.work_file}")
        else:
            messagebox.showwarning("Файл не найден", f"Файл {self.work_file} не найден в папке программы.")
    
    def create_widgets(self):
        # Кнопка загрузки файла
        load_frame = tk.Frame(self.root, bg="#f0f0f0")
        load_frame.pack(pady=15, fill=tk.X, padx=10)
        
        # Кнопки быстрого доступа
        password_button = tk.Button(load_frame, text="Password.xlsx", command=self.open_password_file,
                                  bg="#4CAF50", fg="white", font=("Arial", 9, "bold"),
                                  relief="flat", padx=10, pady=3)
        password_button.pack(side=tk.LEFT, padx=2)
        
        work_button = tk.Button(load_frame, text="Работа.xlsx", command=self.open_work_file,
                              bg="#FF9800", fg="white", font=("Arial", 9, "bold"),
                              relief="flat", padx=10, pady=3)
        work_button.pack(side=tk.LEFT, padx=2)
        
        # Разделитель
        tk.Frame(load_frame, width=20, bg="#f0f0f0").pack(side=tk.LEFT)
        
        self.load_button = tk.Button(load_frame, text="Загрузить файл", command=self.load_file, 
                                   bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                                   relief="flat", padx=15, pady=5)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        self.file_label = tk.Label(load_frame, text=f"Файл: {self.default_file}", 
                                 font=("Arial", 9), bg="#f0f0f0")
        self.file_label.pack(side=tk.LEFT, padx=15)
        
        # Кнопка сворачивания в трей
        minimize_button = tk.Button(load_frame, text="Свернуть в трей", command=self.minimize_to_tray_button,
                                  bg="#9C27B0", fg="white", font=("Arial", 10, "bold"),
                                  relief="flat", padx=10, pady=5)
        minimize_button.pack(side=tk.RIGHT, padx=5)
        
        # Таблица с паролями
        table_frame = tk.Frame(self.root, relief="solid", bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Создаем Treeview с улучшенным оформлением
        style = ttk.Style()
        style.theme_use("default")
        
        # Стиль для таблицы с границами
        style.configure("Bordered.Treeview",
                       background="white",
                       foreground="black",
                       rowheight=30,
                       fieldbackground="white",
                       font=("Arial", 9))
        
        # Стиль для заголовков
        style.configure("Bordered.Treeview.Heading",
                       font=("Arial", 10, "bold"),
                       background="#e0e0e0",
                       foreground="black",
                       relief="raised",
                       padding=5)
        
        # Стиль для выделенной строки
        style.map("Bordered.Treeview",
                 background=[('selected', '#4A90E2')],
                 foreground=[('selected', 'white')])
        
        self.tree = ttk.Treeview(table_frame, 
                                columns=("Название", "Логин", "Пароль", "Информация"), 
                                show="headings",
                                style="Bordered.Treeview")
        
        # Определяем заголовки
        self.tree.heading("Название", text="Название")
        self.tree.heading("Логин", text="Логин")
        self.tree.heading("Пароль", text="Пароль")
        self.tree.heading("Информация", text="Дополнительная информация")
        
        # Устанавливаем ширину колонок
        self.tree.column("Название", width=200, minwidth=150)
        self.tree.column("Логин", width=180, minwidth=150)
        self.tree.column("Пароль", width=150, minwidth=120)
        self.tree.column("Информация", width=300, minwidth=250)
        
        # Настройка тегов для чередования цветов строк (контрастные цвета)
        self.tree.tag_configure('oddrow', background='white')
        self.tree.tag_configure('evenrow', background='#dbdbdb')  # Контрастный серый цвет
        
        # Добавляем скроллбары
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Размещаем элементы
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Привязываем событие клика
        self.tree.bind("<Button-1>", self.on_cell_click)
        self.tree.bind("<Double-1>", self.on_cell_click)
    
    def load_default_file(self):
        """Загрузка файла по умолчанию при запуске"""
        if os.path.exists(self.default_file):
            self.load_data_from_file(self.default_file)
        else:
            # Создаем пустой файл если его нет
            df = pd.DataFrame(columns=["Название", "Логин", "Пароль", "Информация"])
            df.to_excel(self.default_file, index=False)
    
    def load_file(self):
        """Загрузка файла через диалог"""
        file_path = filedialog.askopenfilename(
            title="Выберите файл с паролями",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            self.load_data_from_file(file_path)
            self.file_label.config(text=f"Файл: {os.path.basename(file_path)}")
    
    def load_data_from_file(self, file_path):
        """Загрузка данных из Excel файла"""
        try:
            # Читаем только первые 4 столбца
            df = pd.read_excel(file_path, usecols=[0, 1, 2, 3])
            
            # Если столбцов меньше 4, добавляем недостающие
            while len(df.columns) < 4:
                df[f"Столбец_{len(df.columns)+1}"] = ""
            
            # Очищаем таблицу
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Заполняем таблицу данными с чередованием цветов строк
            for index, row in df.iterrows():
                values = (
                    str(row.iloc[0]) if not pd.isna(row.iloc[0]) else "",
                    str(row.iloc[1]) if not pd.isna(row.iloc[1]) else "",
                    str(row.iloc[2]) if not pd.isna(row.iloc[2]) else "",
                    str(row.iloc[3]) if not pd.isna(row.iloc[3]) else ""
                )
                
                # Чередование цветов строк (контрастные цвета)
                tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                self.tree.insert("", tk.END, values=values, tags=(tag,))
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{str(e)}")
    
    def on_cell_click(self, event):
        """Обработка клика по ячейке таблицы"""
        try:
            # Определяем, по какой ячейке кликнули
            item = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)
            
            if item and column:
                # Получаем значения строки
                values = self.tree.item(item, 'values')
                
                # Определяем индекс колонки (начинается с 1)
                col_index = int(column[1:]) - 1
                
                # Копируем содержимое ячейки в буфер обмена
                if col_index < len(values):
                    cell_value = values[col_index]
                    pyperclip.copy(cell_value)
                    
                    # Показываем уведомление с содержимым, которое было скопировано
                    self.show_copy_notification(cell_value)
                    
                    # Подсвечиваем выбранную строку
                    self.tree.selection_set(item)
                    
        except Exception as e:
            pass  # Игнорируем ошибки копирования
    
    def show_copy_notification(self, copied_text):
        """Показ уведомления о копировании с отображением скопированного текста"""
        # Создаем временное окно уведомления
        notification = tk.Toplevel(self.root)
        notification.title("")
        notification.overrideredirect(True)  # Без рамки
        notification.configure(bg="#4CAF50", relief="solid", bd=1)
        
        # Ограничиваем длину отображаемого текста
        display_text = copied_text[:30] + "..." if len(copied_text) > 30 else copied_text
        if not display_text:
            display_text = "[пусто]"
        
        # Позиционируем уведомление в центре экрана
        x = self.root.winfo_x() + self.root.winfo_width() // 2 - 150
        y = self.root.winfo_y() + 80
        notification.geometry(f"300x50+{x}+{y}")
        
        tk.Label(notification, text=f"✓ Скопировано: {display_text}", 
                bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), 
                wraplength=280).pack(expand=True, pady=5)
        
        # Автоматически закрываем уведомление через 1.5 секунды
        notification.after(1500, notification.destroy)

def main():
    root = tk.Tk()
    root.configure(bg="#f5f5f5")  # Фон основного окна
    
    # Устанавливаем иконку окна (если есть)
    try:
        # Можно добавить свою иконку здесь
        # root.iconbitmap('icon.ico')
        pass
    except:
        pass
    
    app = PasswordManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()