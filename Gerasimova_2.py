import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("600x500")

        # Переменные
        self.password_length = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)
        self.history = []

        self.setup_ui()
        self.load_history()

    def setup_ui(self):
        # Ползунок длины пароля
        ttk.Label(self.root, text="Длина пароля:").pack(pady=5)
        slider = ttk.Scale(self.root, from_=4, to=64,
                           variable=self.password_length, orient=tk.HORIZONTAL)
        slider.pack(fill=tk.X, padx=20)

        length_label = ttk.Label(self.root,
                              textvariable=self.password_length)
        length_label.pack()

        # Чекбоксы для выбора символов
        ttk.Checkbutton(self.root, text="Цифры (0-9)",
                       variable=self.use_digits).pack(anchor=tk.W, padx=20)
        ttk.Checkbutton(self.root, text="Буквы (A-Z, a-z)",
                       variable=self.use_letters).pack(anchor=tk.W, padx=20)
        ttk.Checkbutton(self.root, text="Спецсимволы (!@#$%)",
                       variable=self.use_special).pack(anchor=tk.W, padx=20)

        # Кнопка генерации
        generate_btn = ttk.Button(self.root, text="Сгенерировать пароль",
                             command=self.generate_password)
        generate_btn.pack(pady=10)

        # Поле отображения пароля
        self.password_entry = ttk.Entry(self.root, width=50, font=("Courier", 12))
        self.password_entry.pack(pady=5)

        copy_btn = ttk.Button(self.root, text="Копировать в буфер",
                         command=self.copy_to_clipboard)
        copy_btn.pack(pady=5)

        # Таблица истории
        ttk.Label(self.root, text="История паролей:").pack(pady=(20, 5))

        columns = ("ID", "Пароль", "Длина", "Символы")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
    def generate_password(self):
        # Проверка корректности длины
        length = self.password_length.get()
        if length < 4:
            messagebox.showerror("Ошибка", "Минимальная длина пароля — 4 символа")
            return
        if length > 64:
            messagebox.showerror("Ошибка", "Максимальная длина пароля — 64 символа")
            return

        # Формирование набора символов
        chars = ""
        if self.use_digits.get():
            chars += string.digits
        if self.use_letters.get():
            chars += string.ascii_letters
        if self.use_special.get():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
            return

        # Генерация пароля
        password = ''.join(random.choice(chars) for _ in range(length))

        # Отображение пароля
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

        # Добавление в историю
        self.add_to_history(password, length, chars)

    def copy_to_clipboard(self):
        password = self.password_entry.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена")
    def add_to_history(self, password, length, chars):
        entry = {
            "id": len(self.history) + 1,
            "password": password,
            "length": length,
            "characters": chars
        }
        self.history.append(entry)
        self.update_history_table()
        self.save_history()

    def update_history_table(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполнение таблицы
        for entry in self.history[-10:]:  # Последние 10 записей
            self.tree.insert("", tk.END, values=(
                entry["id"],
                entry["password"],
                entry["length"],
                len(entry["characters"])
            ))

    def save_history(self):
        try:
            with open("password_history.json", "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения истории: {e}")

    def load_history(self):
        if os.path.exists("password_history.json"):
            try:
                with open("password_history.json", "r", encoding="utf-8") as f:
                    self.history = json.load(f)
                self.update_history_table()
            except Exception as e:
                print(f"Ошибка загрузки истории: {e}")
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()


