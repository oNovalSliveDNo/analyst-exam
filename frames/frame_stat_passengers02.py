import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
import pandas as pd
import numpy as np


class FrameStatPassengers02(tk.Frame):
    def __init__(self, parent, df):
        super().__init__(parent)
        self.df = df.copy()
        self.configure(borderwidth=2, relief="ridge")

        # Добавляем информацию о годах
        self.df['Year'] = pd.to_datetime(self.df['Date']).dt.year
        self.years_range = f"{self.df['Year'].min()}-{self.df['Year'].max()}"

        self.create_plot()

    def create_plot(self):
        # Подготовка данных для тепловой карты
        heat_data = self.df.groupby(["DayOfWeek", "Hour"])["Total_Passengers"].mean().unstack()

        # Подготовка данных для линейного графика (среднее по всем дням недели)
        line_data = self.df.groupby(["Hour", "DayOfWeek"])["Total_Passengers"].mean().unstack()
        mean_line = line_data.mean(axis=1)  # Среднее по всем дням недели

        # Рассчитываем статистики для нижнего графика
        median_value = mean_line.median()
        mean_value = mean_line.mean()
        std_dev = mean_line.std()
        lower_bound = median_value - 0.5 * std_dev
        upper_bound = median_value + 0.5 * std_dev

        # Создание фигуры с двумя subplots
        fig = plt.figure(figsize=(10, 8), dpi=100)
        gs = GridSpec(2, 1, height_ratios=[3, 1.5])  # Явно задаем высоту нижнего графика

        # Первый subplot - тепловая карта
        ax1 = fig.add_subplot(gs[0])

        # Настройка цветовой палитры
        cmap = sns.color_palette("YlOrRd", as_cmap=True)

        # Создание тепловой карты с аннотацией
        heatmap = sns.heatmap(
            heat_data,
            cmap=cmap,
            ax=ax1,
            annot=True,
            fmt=".0f",
            annot_kws={"size": 8},
            linewidths=0.5,
            linecolor="white",
            cbar_kws={'shrink': 0.8, 'label': 'Кол-во пассажиров'}
        )

        # Улучшение заголовка и подписей
        ax1.set_title(
            f"Средний пассажиропоток по дням и часам (данные за {self.years_range} годы)",
            fontsize=14,
            pad=20,
            fontweight="bold"
        )

        # Улучшение подписей осей
        ax1.set_xlabel(
            "Час",
            fontsize=12,
            labelpad=10,
            fontweight="bold"
        )
        ax1.set_ylabel(
            "День недели",
            fontsize=12,
            labelpad=10,
            fontweight="bold"
        )

        # Улучшение подписей тиков
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        ax1.set_yticklabels(
            days,
            rotation=0,
            fontsize=10
        )
        ax1.set_xticklabels(
            [f"{int(h)}:00" for h in ax1.get_xticks()],
            rotation=45,
            fontsize=9
        )

        # Второй subplot - линейный график среднего значения по всем дням недели
        ax2 = fig.add_subplot(gs[1], sharex=ax1)  # sharex для совпадения осей X

        # Ярко-зеленая полоса допустимых значений
        ax2.axhspan(lower_bound, upper_bound, facecolor='#00FF00', alpha=0.3, label='Допустимый диапазон')

        # Линии медианы и среднего
        ax2.axhline(median_value, color='red', linestyle='--', linewidth=1.5, label='Медиана')
        ax2.axhline(mean_value, color='purple', linestyle='-.', linewidth=1.5, label='Среднее')

        # Построение средней линии с маркировкой аномалий
        for hour, value in mean_line.items():
            if value < lower_bound or value > upper_bound:
                # Аномальные значения отмечаем красным
                ax2.plot(hour, value, 'ro', markersize=6)
                ax2.text(
                    hour, value, f'{int(value)}',
                    ha='center', va='bottom',
                    fontsize=8, color='red',
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='red', boxstyle='round,pad=0.2')
                )
            else:
                # Нормальные значения отмечаем синим
                ax2.plot(hour, value, 'bo', markersize=4)
                ax2.text(
                    hour, value, f'{int(value)}',
                    ha='center', va='bottom',
                    fontsize=8,
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2')
                )

        # Соединяем точки линией
        ax2.plot(mean_line.index, mean_line, color='blue', linewidth=1, alpha=0.5)

        # Настройка осей и подписей
        ax2.set_title(
            "Средний пассажиропоток по часам (усредненный по всем дням недели)",
            fontsize=12,
            pad=10,
            fontweight="bold"
        )
        ax2.set_xlabel("Час", fontsize=10)
        ax2.set_ylabel("Пассажиры", fontsize=10)
        ax2.grid(True, linestyle='--', alpha=0.7)

        # Установка целочисленных значений на оси X (часы)
        ax2.set_xticks(np.arange(0, 24))
        ax2.set_xticklabels([f"{h}:00" for h in range(24)], rotation=45)

        # Выравнивание ширины графиков
        plt.setp(ax1.get_xticklabels(), visible=False)  # Скрыть метки часов на верхнем графике

        # Создаем пространство справа для легенды и статистики
        plt.subplots_adjust(right=0.75)

        # Выносим легенду в отдельную область справа
        ax2.legend(
            loc='center left',
            bbox_to_anchor=(1.05, 0.5),
            frameon=True,
            framealpha=1.0,
            edgecolor='black'
        )

        # Выносим статистику в отдельную область справа под легендой
        stats_text = (
            f"Статистика:\n\n"
            f"Медиана: {median_value:.0f}\n"
            f"Среднее: {mean_value:.0f}\n"
            f"Стандартное отклонение: {std_dev:.0f}\n"
            f"Допустимый диапазон:\n"
            f"[{lower_bound:.0f}, {upper_bound:.0f}]"
        )

        ax2.text(
            1.05, 0.25, stats_text,
            transform=ax2.transAxes,
            verticalalignment='top',
            bbox=dict(
                boxstyle='round',
                facecolor='white',
                alpha=0.8,
                edgecolor='gray'
            ),
            fontsize=10
        )

        # Оптимизация расположения элементов
        plt.subplots_adjust(hspace=0.3)  # Регулировка вертикального расстояния между графиками
        fig.tight_layout(rect=[0, 0, 0.85, 1])  # Оставляем 15% пространства справа

        # Создание canvas
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
