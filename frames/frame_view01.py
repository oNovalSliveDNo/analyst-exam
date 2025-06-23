import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats


class FrameOverview01(tk.Frame):
    def __init__(self, parent, dataframe, style):
        super().__init__(parent)
        self.df = dataframe
        self.style = style
        self.create_plot()

    def create_plot(self):
        latest_date = self.df['Date'].max().date()
        today_df = self.df[self.df['Date'].dt.date == latest_date]
        hourly = today_df.groupby("Hour")["Total_Passengers"].sum().reset_index()

        # Рассчитываем статистики
        mean_val = hourly["Total_Passengers"].mean()
        median_val = hourly["Total_Passengers"].median()
        std_dev = hourly["Total_Passengers"].std()

        # Определяем "зеленый коридор" (нормальный диапазон)
        lower_bound = mean_val - 0.5 * std_dev  # Можно настроить коэффициент
        upper_bound = mean_val + 0.5 * std_dev

        # Настройка стиля
        sns.set_theme(style="whitegrid")
        plt.rcParams['font.family'] = 'Arial'

        # Создание фигуры с динамическим размером
        fig, ax = plt.subplots(figsize=(8, 4), facecolor='none', dpi=100)  # Уменьшенный размер
        ax.set_facecolor('#f8f9fa')
        fig.patch.set_alpha(0)

        # Зеленый коридор (нормальный диапазон)
        ax.axhspan(lower_bound, upper_bound, facecolor='#a7c4bc', alpha=0.3,
                   label=f'Нормальный диапазон ({lower_bound:,.0f}-{upper_bound:,.0f})')

        # Средняя линия
        ax.axhline(mean_val, color='#2a9d8f', linestyle='--', linewidth=2,
                   alpha=0.7, label=f'Среднее: {mean_val:,.0f}')

        # Медиана
        ax.axhline(median_val, color='#e76f51', linestyle=':', linewidth=2,
                   alpha=0.7, label=f'Медиана: {median_val:,.0f}')

        # Основной график
        line = sns.lineplot(
            data=hourly,
            x="Hour",
            y="Total_Passengers",
            marker="o",
            markersize=8,
            markeredgecolor='white',
            markerfacecolor='#e63946',
            linewidth=3,
            ax=ax,
            color='#457b9d',
            label='Пассажиропоток'
        )

        # Метки данных с цветом в зависимости от положения относительно коридора
        for x, y in zip(hourly["Hour"], hourly["Total_Passengers"]):
            color = '#1d3557' if lower_bound <= y <= upper_bound else '#e63946'
            ax.text(
                x, y + 0.05 * y, f'{y:,.0f}',
                color=color,
                fontsize=8,  # Уменьшенный размер шрифта
                fontweight='bold',
                ha='center',
                va='bottom'
            )

        # Подсветка точек вне коридора
        outliers = hourly[~hourly["Total_Passengers"].between(lower_bound, upper_bound)]
        if not outliers.empty:
            ax.scatter(
                outliers["Hour"],
                outliers["Total_Passengers"],
                s=100,  # Уменьшенный размер точек
                facecolors='none',
                edgecolors='#e63946',
                linewidths=2,
                label='Отклонения от нормы'
            )

        # Настройка заголовка
        ax.set_title(
            f"АНАЛИЗ ПАССАЖИРОПОТОКА С СТАТИСТИКОЙ\n{latest_date.strftime('%d.%m.%Y')}",
            fontsize=12,  # Уменьшенный размер шрифта
            fontweight='bold',
            color='#1d3557',
            pad=15  # Уменьшенный отступ
        )

        # Подписи осей
        ax.set_xlabel("Час дня", fontsize=10, fontweight='bold', color='#1d3557', labelpad=8)
        ax.set_ylabel("Количество пассажиров", fontsize=10, fontweight='bold', color='#1d3557', labelpad=8)

        # Настройка осей
        ax.tick_params(axis='both', which='major', labelsize=8, colors='#1d3557')
        ax.set_xticks(np.arange(0, 24, 1))
        ax.set_xlim(-0.5, 23.5)

        # Форматирование чисел
        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

        # Сетка
        ax.grid(True, linestyle='--', alpha=0.7, color='#adb5bd')

        # Границы
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)
        for spine in ['bottom', 'left']:
            ax.spines[spine].set_color('#495057')

        # Легенда (выносим за пределы графика справа)
        ax.legend(
            loc='center left',
            frameon=True,
            framealpha=0.9,
            facecolor='white',
            edgecolor='#495057',
            fontsize=8,  # Уменьшенный размер шрифта
            bbox_to_anchor=(1.05, 0.5),
            borderaxespad=0.5
        )

        # Настройка расположения элементов
        plt.tight_layout()  # Автоматическая подгонка элементов

        # Встраиваем график
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()

        # Используем grid вместо pack для лучшего контроля
        canvas.get_tk_widget().pack(expand=True, fill="both", padx=5, pady=5)

        # Привязываем изменение размера фрейма к обновлению графика
        self.bind("<Configure>", lambda event: self.on_resize(canvas, fig))

    def on_resize(self, canvas, fig):
        # Получаем текущие размеры фрейма
        width = self.winfo_width() / 100  # Преобразуем в дюймы (примерно)
        height = self.winfo_height() / 100

        # Устанавливаем новые размеры фигуры
        fig.set_size_inches(max(4, width - 1), max(3, height - 1))  # Минимальные размеры 4x3

        # Устанавливаем новые параметры расположения
        fig.tight_layout()

        # Перерисовываем canvas
        canvas.draw()