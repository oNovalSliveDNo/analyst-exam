import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from frames.frame01 import Frame01


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Аэропорт 360")
        self.geometry("1500x1000")

        # Переменная для хранения DataFrame
        self.current_df = None

        # Создаем меню
        self.create_menu()

        # Конфигурация grid для главного окна
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Создаем основной фрейм (пока пустой)
        self.frame1 = None

        # При первом открытии сразу вызываем диалог выбора файла
        self.first_open_file()

    def create_menu(self):
        """Создание меню приложения"""
        menubar = tk.Menu(self)

        # Меню File
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open file", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Close file", command=self.close_file)
        menubar.add_cascade(label="File", menu=file_menu)

        self.config(menu=menubar)

    def first_open_file(self):
        """Обработчик первого открытия файла при запуске"""
        self.open_file(initial=True)

    def open_file(self, initial=False):
        """Обработчик открытия файла"""
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )

        if not file_path:  # Если пользователь отменил выбор
            if initial:  # Если это первый запуск и файл не выбран
                if messagebox.askyesno(
                        "Внимание",
                        "Файл не выбран. Хотите выбрать файл сейчас?"
                ):
                    self.open_file(initial=True)
                else:
                    self.destroy()  # Закрываем приложение
            return

        try:
            # Читаем CSV файл
            self.current_df = pd.read_csv(file_path, parse_dates=["Date"])

            # Уничтожаем старый фрейм, если он есть
            if self.frame1 is not None:
                self.frame1.destroy()

            # Создаем новый фрейм с передачей DataFrame
            self.frame1 = Frame01(self, self.current_df)
            self.frame1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")
            if initial:
                self.open_file(initial=True)  # Повторяем попытку для первого открытия

    def close_file(self):
        """Обработчик закрытия файла"""
        if self.frame1 is not None:
            self.frame1.destroy()
            self.frame1 = None
        self.current_df = None
        print("Файл закрыт, данные очищены")


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()