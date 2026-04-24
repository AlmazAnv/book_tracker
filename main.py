import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ========== ШАГ 3: СОЗДАЁМ ОКНО ==========
root = tk.Tk()
root.title("Book Tracker")
root.geometry("800x500")

# Список для хранения книг
books = []

# ========== ШАГ 4: ПОЛЯ ВВОДА ==========
frame_input = tk.LabelFrame(root, text="Добавить книгу", padx=10, pady=10)
frame_input.pack(padx=10, pady=10, fill="x")

tk.Label(frame_input, text="Название:").grid(row=0, column=0, sticky="w")
entry_title = tk.Entry(frame_input, width=30)
entry_title.grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_input, text="Автор:").grid(row=1, column=0, sticky="w")
entry_author = tk.Entry(frame_input, width=30)
entry_author.grid(row=1, column=1, padx=5, pady=2)

tk.Label(frame_input, text="Жанр:").grid(row=2, column=0, sticky="w")
entry_genre = tk.Entry(frame_input, width=30)
entry_genre.grid(row=2, column=1, padx=5, pady=2)

tk.Label(frame_input, text="Страниц:").grid(row=3, column=0, sticky="w")
entry_pages = tk.Entry(frame_input, width=10)
entry_pages.grid(row=3, column=1, padx=5, pady=2, sticky="w")

# ========== ШАГ 5: ФУНКЦИИ ДЛЯ КНОПКИ "ДОБАВИТЬ КНИГУ" ==========
def add_book():
    title = entry_title.get().strip()
    author = entry_author.get().strip()
    genre = entry_genre.get().strip()
    pages_str = entry_pages.get().strip()

    # Проверка на пустые поля
    if not title or not author or not genre or not pages_str:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
        return

    # Проверка, что страницы — число
    if not pages_str.isdigit():
        messagebox.showerror("Ошибка", "Количество страниц должно быть числом")
        return

    pages = int(pages_str)

    book = {
        "title": title,
        "author": author,
        "genre": genre,
        "pages": pages
    }

    books.append(book)
    update_table()  # обновляем таблицу (шаг 6)
    clear_inputs()

def clear_inputs():
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_pages.delete(0, tk.END)

# КНОПКА "ДОБАВИТЬ КНИГУ"
btn_add = tk.Button(frame_input, text="Добавить книгу", command=add_book)
btn_add.grid(row=4, column=0, columnspan=2, pady=10)

# ========== ШАГ 6: ТАБЛИЦА ДЛЯ ОТОБРАЖЕНИЯ КНИГ ==========
frame_table = tk.LabelFrame(root, text="Список книг")
frame_table.pack(fill="both", expand=True, padx=10, pady=10)

# Создаём таблицу (Treeview)
columns = ("Название", "Автор", "Жанр", "Страниц")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(fill="both", expand=True)

def update_table():
    # Очищаем таблицу
    for row in tree.get_children():
        tree.delete(row)
    
    # Заполняем заново
    for book in books:
        tree.insert("", tk.END, values=(book["title"], book["author"], book["genre"], book["pages"]))

# ========== ШАГ 7: ФИЛЬТРАЦИЯ ==========
frame_filter = tk.LabelFrame(root, text="Фильтр")
frame_filter.pack(fill="x", padx=10, pady=5)

tk.Label(frame_filter, text="Жанр:").grid(row=0, column=0)
filter_genre_entry = tk.Entry(frame_filter, width=20)
filter_genre_entry.grid(row=0, column=1)

tk.Label(frame_filter, text="Страниц >").grid(row=0, column=2)
filter_pages_entry = tk.Entry(frame_filter, width=10)
filter_pages_entry.grid(row=0, column=3)

def apply_filter():
    genre_filter = filter_genre_entry.get().strip().lower()
    pages_filter = filter_pages_entry.get().strip()

    filtered = books.copy()

    if genre_filter:
        filtered = [b for b in filtered if genre_filter in b["genre"].lower()]

    if pages_filter and pages_filter.isdigit():
        filtered = [b for b in filtered if b["pages"] > int(pages_filter)]

    # Очищаем таблицу
    for row in tree.get_children():
        tree.delete(row)

    # Показываем отфильтрованные книги
    for book in filtered:
        tree.insert("", tk.END, values=(book["title"], book["author"], book["genre"], book["pages"]))

def reset_filter():
    filter_genre_entry.delete(0, tk.END)
    filter_pages_entry.delete(0, tk.END)
    update_table()  # показываем все книги

btn_filter = tk.Button(frame_filter, text="Применить фильтр", command=apply_filter)
btn_filter.grid(row=0, column=4, padx=10)

btn_reset = tk.Button(frame_filter, text="Сбросить фильтр", command=reset_filter)
btn_reset.grid(row=0, column=5)

# ========== ШАГ 8: СОХРАНЕНИЕ И ЗАГРУЗКА JSON ==========
def save_to_json():
    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)
    messagebox.showinfo("Сохранено", "Данные сохранены в books.json")

def load_from_json():
    global books
    if os.path.exists("books.json"):
        with open("books.json", "r", encoding="utf-8") as f:
            books = json.load(f)
        update_table()
        messagebox.showinfo("Загружено", "Данные загружены из books.json")
    else:
        messagebox.showwarning("Нет файла", "Файл books.json не найден")

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Сохранить в JSON", command=save_to_json).pack(side="left", padx=5)
tk.Button(frame_buttons, text="Загрузить из JSON", command=load_from_json).pack(side="left", padx=5)

# ========== ЗАПУСК ПРОГРАММЫ ==========
root.mainloop()