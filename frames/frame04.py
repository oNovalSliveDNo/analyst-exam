import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta


class Frame04(tk.Frame):
    def __init__(self, parent, style, current_dataframe):
        super().__init__(parent)
        self.configure(borderwidth=2, relief="groove")

        self.STYLE = style

        self.current_dataframe = current_dataframe

        self.create_cargo_chart()

    def create_cargo_chart(self):
        try:
            # Читаем данные
            df = self.current_dataframe # = pd.read_csv("transformed.csv", parse_dates=["Date"])

            # Берём последний день
            latest_date = df['Date'].max().date()
            df_latest = df[df['Date'].dt.date == latest_date]

            # Средний груз на рейс за сегодня
            today_cargo = df_latest['Total_Cargo'].sum() / len(df_latest)

            # Функция для расчета среднего груза за период
            def avg_cargo_per_flight(start_date, end_date):
                df_period = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]
                return df_period.groupby(df_period['Date'].dt.date).apply(
                    lambda x: x['Total_Cargo'].sum() / len(x))

            # Определяем периоды
            last_week_start = latest_date - timedelta(days=latest_date.weekday() + 7)
            last_week_end = last_week_start + timedelta(days=6)
            month_start = datetime(latest_date.year, latest_date.month, 1).date()
            quarter_start = datetime(latest_date.year, 4, 1).date()
            year_start = datetime(latest_date.year, 1, 1).date()

            # Рассчитываем средние значения
            weekly_avg_c = avg_cargo_per_flight(last_week_start, last_week_end).mean()
            month_avg_c = avg_cargo_per_flight(month_start, latest_date - timedelta(days=1)).mean()
            quarter_avg_c = avg_cargo_per_flight(quarter_start, latest_date - timedelta(days=1)).mean()
            year_avg_c = avg_cargo_per_flight(year_start, latest_date - timedelta(days=1)).mean()

            # Рассчитываем медианные значения
            weekly_median_c = avg_cargo_per_flight(last_week_start, last_week_end).median()
            month_median_c = avg_cargo_per_flight(month_start, latest_date - timedelta(days=1)).median()
            quarter_median_c = avg_cargo_per_flight(quarter_start, latest_date - timedelta(days=1)).median()
            year_median_c = avg_cargo_per_flight(year_start, latest_date - timedelta(days=1)).median()

            # Данные за прошлый год
            last_year_date = datetime(latest_date.year - 1, latest_date.month, latest_date.day).date()
            df_last_year = df[df['Date'].dt.date == last_year_date]
            last_year_cargo = df_last_year['Total_Cargo'].sum() / len(df_last_year) if len(df_last_year) > 0 else 0

            # Функция для расчета дельты
            def calc_delta(current, reference):
                if reference == 0:
                    return 0
                return round((current - reference) / reference * 100, 1)

            # Рассчитываем дельты
            delta_c_week = calc_delta(today_cargo, weekly_avg_c)
            delta_c_month = calc_delta(today_cargo, month_avg_c)
            delta_c_quarter = calc_delta(today_cargo, quarter_avg_c)
            delta_c_year = calc_delta(today_cargo, year_avg_c)
            delta_c_last_year = calc_delta(today_cargo, last_year_cargo)

            delta_c_week_median = calc_delta(today_cargo, weekly_median_c)
            delta_c_month_median = calc_delta(today_cargo, month_median_c)
            delta_c_quarter_median = calc_delta(today_cargo, quarter_median_c)
            delta_c_year_median = calc_delta(today_cargo, year_median_c)

            # Создаем фигуру matplotlib
            fig, ax = plt.subplots(figsize=self.STYLE["figsize"], facecolor='#fffaf3')
            fig.suptitle(f"ДАТА: {latest_date.strftime('%d.%m.%Y')}",
                         fontsize=self.STYLE["title_fontsize"],
                         x=self.STYLE["title_X"],  # позиция по X
                         y=self.STYLE["title_Y"],
                         weight=self.STYLE["title_weight"],
                         ha=self.STYLE["title_ha"]  # выравнивание
                         )

            # Основной KPI
            ax.text(self.STYLE["kpi_1"],
                    self.STYLE["kpi_2"],
                    f"СРЕДНИЙ ВЕС\nНА РЕЙС: {int(today_cargo)} кг",
                    fontsize=self.STYLE["kpi_fontsize"],
                    ha=self.STYLE["kpi_ha"],
                    va=self.STYLE["kpi_va"],
                    weight=self.STYLE["kpi_weight"],
                    bbox=dict(facecolor='#fdcb6e',
                              alpha=0.25,
                              pad=self.STYLE["kpi_pad"]))

            # Подготовка данных для таблицы
            rows = ['Неделя', 'Месяц', 'Квартал', 'Год', 'Прошлый год']
            columns = ['Среднее', 'Медиана', 'Δ от ср.', 'Δ от мед.']

            cell_text_cargo = [
                [f"{int(weekly_avg_c)}", f"{int(weekly_median_c)}", f"{'+' if delta_c_week > 0 else ''}{delta_c_week}%",
                 f"{'+' if delta_c_week_median > 0 else ''}{delta_c_week_median}%"],
                [f"{int(month_avg_c)}", f"{int(month_median_c)}", f"{'+' if delta_c_month > 0 else ''}{delta_c_month}%",
                 f"{'+' if delta_c_month_median > 0 else ''}{delta_c_month_median}%"],
                [f"{int(quarter_avg_c)}", f"{int(quarter_median_c)}",
                 f"{'+' if delta_c_quarter > 0 else ''}{delta_c_quarter}%",
                 f"{'+' if delta_c_quarter_median > 0 else ''}{delta_c_quarter_median}%"],
                [f"{int(year_avg_c)}", f"{int(year_median_c)}", f"{'+' if delta_c_year > 0 else ''}{delta_c_year}%",
                 f"{'+' if delta_c_year_median > 0 else ''}{delta_c_year_median}%"],
                [f"{int(last_year_cargo)}", "-", f"{'+' if delta_c_last_year > 0 else ''}{delta_c_last_year}%", "-"]
            ]

            # Цвета для ячеек с дельтами
            colors_cargo = []
            for row in cell_text_cargo:
                row_colors = ['white', 'white']
                for delta_text in row[2:]:
                    if delta_text == "-":
                        row_colors.append('white')
                    else:
                        delta_value = float(delta_text.replace('%', '').replace('+', ''))
                        row_colors.append('#fab1a0' if delta_value < 0 else '#81ecec')
                colors_cargo.append(row_colors)

            # Создание таблицы
            table_cargo = ax.table(
                cellText=cell_text_cargo,
                rowLabels=rows,
                colLabels=columns,
                rowColours=['#f8f9fa'] * len(rows),
                colColours=['#f8f9fa'] * len(columns),
                cellColours=colors_cargo,
                cellLoc='center',
                loc='center',
                bbox=self.STYLE["bbox_table"]
            )

            # Настройка стиля таблицы
            table_cargo.auto_set_font_size(False)
            table_cargo.set_fontsize(self.STYLE["table_fontsize"])
            table_cargo.scale(*self.STYLE["scale_table"])

            for (row, col), cell in table_cargo.get_celld().items():
                if row == 0:
                    cell.set_text_props(weight='bold', fontsize=self.STYLE["header_fontsize"])
                cell.set_edgecolor('#dee2e6')
                cell.set_height(self.STYLE["cell_height"])

            ax.axis('off')
            plt.tight_layout()

            # Встраиваем график в Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            error_label = tk.Label(self, text=f"Ошибка при создании графика: {str(e)}", fg="red")
            error_label.pack(pady=20)
