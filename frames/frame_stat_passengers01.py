import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.dates import MonthLocator, DateFormatter
import numpy as np


class FrameStatPassengers01(tk.Frame):
    def __init__(self, parent, df):
        super().__init__(parent)
        self.df = df.copy()
        self.configure(borderwidth=2, relief="ridge")

        # Получаем уникальные года из данных
        self.available_years = sorted(self.df["Year"].unique())
        self.selected_year = self.available_years[-1]  # По умолчанию выбираем последний год

        # Создаем интерфейс
        self.create_widgets()
        self.create_plot()

    def create_widgets(self):
        # Основной контейнер
        self.main_panel = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_panel.pack(fill=tk.BOTH, expand=True)

        # Панель управления слева
        control_frame = tk.Frame(self.main_panel, width=150, padx=10, pady=10, bg="#f0f0f0")
        self.main_panel.add(control_frame)

        # Заголовок
        tk.Label(
            control_frame,
            text="Фильтры",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0"
        ).pack(pady=(0, 15))

        # Выбор года для выделения
        tk.Label(
            control_frame,
            text="Выделить год:",
            font=("Arial", 11),
            bg="#f0f0f0"
        ).pack(anchor=tk.W, pady=(5, 5))

        self.year_var = tk.StringVar(value=str(self.selected_year))  # Преобразуем в строку

        for year in self.available_years:
            rb = tk.Radiobutton(
                control_frame,
                text=str(year),
                variable=self.year_var,
                value=str(year),  # Значение должно быть строкой
                command=self.update_plot,
                font=("Arial", 10),
                bg="#f0f0f0",
                activebackground="#f0f0f0",
                selectcolor="#d9d9d9"
            )
            rb.pack(anchor=tk.W, padx=5, pady=2)

        # Панель для графика
        self.plot_frame = tk.Frame(self.main_panel)
        self.main_panel.add(self.plot_frame)

    def create_plot(self):
        # Очищаем предыдущий график
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Получаем текущие настройки
        highlight_year = int(self.year_var.get())

        # Подготовка данных
        df_plot = self.df.copy()
        df_plot["Month"] = df_plot["Date"].dt.month

        # Группируем данные по году и месяцу
        grouped = df_plot.groupby(["Year", "Month"])["Total_Passengers"].sum().reset_index()

        # Создаем фигуру с увеличенным размером
        plt.style.use('seaborn-v0_8')  # Используем актуальный стиль
        fig, ax = plt.subplots(figsize=(12, 7), dpi=100)
        fig.patch.set_facecolor('#f5f5f5')
        ax.set_facecolor('#f9f9f9')

        # Месяца для оси X
        months = range(1, 13)
        month_names = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн',
                      'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']

        # Цветовая палитра для невыделенных лет
        palette = sns.color_palette("husl", len(self.available_years))

        # Рисуем линии для каждого года
        for i, year in enumerate(self.available_years):
            year_data = grouped[grouped["Year"] == year]
            # Убедимся, что данные есть для всех месяцев
            complete_data = year_data.set_index("Month").reindex(months).reset_index()

            if year == highlight_year:
                # Выделенный год - толстая линия с маркерами и подписями
                line = sns.lineplot(
                    data=complete_data,
                    x="Month",
                    y="Total_Passengers",
                    label=str(year),
                    linewidth=3.5,
                    marker='o',
                    markersize=10,
                    markerfacecolor='white',
                    markeredgewidth=2,
                    color='#e63946',  # Яркий цвет для выделения
                    ax=ax
                )

                # Добавляем подписи данных для выделенного года
                for _, row in complete_data.iterrows():
                    if not np.isnan(row['Total_Passengers']):
                        ax.text(
                            row['Month'],
                            row['Total_Passengers'] + (ax.get_ylim()[1] * 0.02),
                            f"{int(row['Total_Passengers'] / 1000)}K" if row['Total_Passengers'] >= 1000
                            else str(int(row['Total_Passengers'])),
                            ha='center',
                            va='bottom',
                            fontsize=10,
                            fontweight='bold',
                            color='#e63946'
                        )
            else:
                # Остальные годы - тонкие линии
                sns.lineplot(
                    data=complete_data,
                    x="Month",
                    y="Total_Passengers",
                    label=str(year),
                    linewidth=1.5,
                    alpha=0.7,
                    marker='o',
                    markersize=5,
                    color=palette[i],
                    ax=ax
                )

        # Настройки графика
        ax.set_title(
            "Сравнение пассажиропотока по месяцам",
            fontsize=16,
            fontweight='bold',
            pad=20
        )
        ax.set_xlabel(
            "Месяц",
            fontsize=13,
            fontweight='bold',
            labelpad=10
        )
        ax.set_ylabel(
            "Количество пассажиров",
            fontsize=13,
            fontweight='bold',
            labelpad=10
        )

        # Увеличиваем размер шрифта меток на осях
        ax.tick_params(axis='both', which='major', labelsize=11)

        # Устанавливаем метки месяцев на оси X
        ax.set_xticks(months)
        ax.set_xticklabels(month_names, fontsize=11)

        # Добавляем сетку для лучшей читаемости
        ax.grid(True, linestyle='--', alpha=0.6)

        # Улучшаем отображение больших чисел на оси Y
        ax.get_yaxis().set_major_formatter(
            plt.FuncFormatter(lambda x, p: format(int(x), ','))
        )  # Добавлена закрывающая скобка

        # Оптимизируем легенду
        legend = ax.legend(
            title='Год',
            bbox_to_anchor=(1.02, 1),
            loc='upper left',
            fontsize=11,
            title_fontsize=12,
            framealpha=0.9
        )

        # Выделяем текущий выбранный год в легенде
        for text in legend.get_texts():
            if text.get_text() == str(highlight_year):
                text.set_fontweight('bold')
                text.set_color('#e63946')

        fig.tight_layout()

        # Встраиваем график в Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_plot(self):
        # Обновляем график при изменении фильтров
        self.create_plot()