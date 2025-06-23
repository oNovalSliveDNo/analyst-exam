import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from textwrap import wrap


class FrameOverview02(tk.Frame):
    def __init__(self, parent, dataframe, style):
        super().__init__(parent)
        self.df = dataframe
        self.style = style
        self.create_plot()

    def create_plot(self):
        latest_date = self.df['Date'].max().date()
        today_df = self.df[self.df['Date'].dt.date == latest_date]
        delay_data = today_df[today_df["DelayGroup"] != "Не указана"]
        delay_counts = delay_data["DelayGroup"].value_counts()

        # Создаем фигуру с динамическим размером, основанным на размере фрейма
        fig = plt.Figure(facecolor=self.style["facecolor"])

        # Изменяем компоновку: добавляем 2 подграфика - узкий для заголовка и основной для диаграммы
        gs = fig.add_gridspec(1, 2, width_ratios=[0.1, 0.9])
        ax_title = fig.add_subplot(gs[0])
        ax = fig.add_subplot(gs[1])

        # Скрываем оси для заголовка
        ax_title.axis('off')

        # Добавляем вертикальный заголовок слева
        title_text = f"АНАЛИЗ ПРИЧИН ЗАДЕРЖЕК\n{latest_date.strftime('%d.%m.%Y')}"
        ax_title.text(
            0.5, 0.5,
            title_text,
            rotation=90,
            va='center',
            ha='center',
            fontsize=14,
            fontweight='bold',
            multialignment='center'
        )

        # Автоматическая подстройка отступов
        fig.subplots_adjust(left=0.15, right=0.7, top=0.9, bottom=0.15)

        # Генерация красивых цветов
        colors = sns.color_palette("husl", len(delay_counts))

        # Рисуем красивую круговую диаграмму (убраны labels)
        wedges, texts, autotexts = ax.pie(
            delay_counts,
            labels=None,
            autopct=lambda p: f'{p:.1f}%\n({int(p / 100 * sum(delay_counts))})',
            startangle=140,
            colors=colors,
            wedgeprops={
                'linewidth': 1,
                'edgecolor': 'white'
            },
            textprops={'fontsize': 9, 'fontweight': 'bold'},
            pctdistance=0.85
        )

        # Настройка внешнего вида процентов
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')

        # Добавляем белую рамку вокруг каждого сегмента
        for wedge in wedges:
            wedge.set_edgecolor('white')
            wedge.set_linewidth(1.5)

        # Обертка длинных меток для легенды
        wrapped_labels = ["\n".join(wrap(label, 20)) for label in delay_counts.index]

        # Добавляем легенду справа
        legend = ax.legend(
            wedges,
            wrapped_labels,
            title="Причины",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            fontsize=9,
            title_fontsize=11,
            facecolor='#f5f5f5'
        )
        legend.get_title().set_fontweight('bold')

        # Делаем диаграмму равномерной
        ax.axis('equal')

        # Добавляем подпись внизу
        fig.text(
            0.5, 0.02,
            "Данные по задержкам рейсов",
            ha='center',
            fontsize=10,
            fontweight='bold'
        )

        # Создаем canvas с автоматическим определением размера
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()

        # Упаковываем canvas с заполнением всего доступного пространства
        canvas.get_tk_widget().pack(expand=True, fill="both", padx=5, pady=5)

        # Привязываем изменение размера фрейма к обновлению графика
        self.bind("<Configure>", lambda e: self.update_plot_size(fig, canvas))

    def update_plot_size(self, fig, canvas):
        # Получаем текущие размеры фрейма
        width = self.winfo_width() / 100  # конвертируем в дюймы (примерно)
        height = self.winfo_height() / 100

        # Устанавливаем новый размер фигуры
        fig.set_size_inches(width * 0.9, height * 0.9)  # 90% от размера фрейма

        # Перерисовываем canvas
        canvas.draw_idle()