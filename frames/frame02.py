import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta


class Frame02(tk.Frame):
    def __init__(self, parent, style, current_dataframe):
        super().__init__(parent)
        self.configure(borderwidth=2, relief="groove")

        # Стили для графика
        self.STYLE = style
        self.current_dataframe = current_dataframe

        # Создаем контейнер для графика
        self.create_flight_metrics_chart()

    def create_flight_metrics_chart(self):
        try:
            # Читаем данные
            df = self.current_dataframe # pd.read_csv("transformed.csv", parse_dates=["Date"])

            # Берём последний день
            latest_date = df['Date'].max().date()
            df_latest = df[df['Date'].dt.date == latest_date]
            today_flights = df_latest.shape[0]

            # Вычисляем метрики (ваш код)
            last_week_start = latest_date - timedelta(days=latest_date.weekday() + 7)
            last_week_end = last_week_start + timedelta(days=6)
            weekly_avg = df[(df['Date'].dt.date >= last_week_start) & (df['Date'].dt.date <= last_week_end)].shape[
                             0] / 7

            month_start = datetime(latest_date.year, latest_date.month, 1).date()
            month_avg = df[(df['Date'].dt.date >= month_start) & (df['Date'].dt.date < latest_date)].shape[0] / (
                    latest_date.day - 1)

            quarter_start = datetime(latest_date.year, 4, 1).date()
            quarter_avg = df[(df['Date'].dt.date >= quarter_start) & (df['Date'].dt.date < latest_date)].shape[0] / (
                (latest_date - quarter_start).days)

            year_start = datetime(latest_date.year, 1, 1).date()
            year_avg = df[(df['Date'].dt.date >= year_start) & (df['Date'].dt.date < latest_date)].shape[0] / (
                (latest_date - year_start).days)

            def get_daily_counts(start_date, end_date):
                return df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)] \
                    .groupby(df['Date'].dt.date).size()

            weekly_median = get_daily_counts(last_week_start, last_week_end).median()
            month_median = get_daily_counts(month_start, latest_date - timedelta(days=1)).median()
            quarter_median = get_daily_counts(quarter_start, latest_date - timedelta(days=1)).median()
            year_median = get_daily_counts(year_start, latest_date - timedelta(days=1)).median()

            last_year_date = datetime(latest_date.year - 1, latest_date.month, latest_date.day).date()
            last_year_flights = df[df['Date'].dt.date == last_year_date].shape[0]

            def calc_delta(current, reference):
                if reference == 0:
                    return 0
                return round((current - reference) / reference * 100, 1)

            delta_week = calc_delta(today_flights, weekly_avg)
            delta_month = calc_delta(today_flights, month_avg)
            delta_quarter = calc_delta(today_flights, quarter_avg)
            delta_year = calc_delta(today_flights, year_avg)
            delta_last_year = calc_delta(today_flights, last_year_flights)

            delta_week_median = calc_delta(today_flights, weekly_median)
            delta_month_median = calc_delta(today_flights, month_median)
            delta_quarter_median = calc_delta(today_flights, quarter_median)
            delta_year_median = calc_delta(today_flights, year_median)

            # Создаем фигуру matplotlib
            fig, ax = plt.subplots(figsize=self.STYLE["figsize"], facecolor='#fef6e6')
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
                    f"КОЛИЧЕСТВО РЕЙСОВ\nЗА ДЕНЬ: {today_flights}",
                    fontsize=self.STYLE["kpi_fontsize"],
                    ha=self.STYLE["kpi_ha"],
                    va=self.STYLE["kpi_va"],
                    weight=self.STYLE["kpi_weight"],
                    bbox=dict(facecolor='#2a7fff',
                              alpha=0.2,
                              pad=self.STYLE["kpi_pad"]))

            # Объединённая таблица
            rows = ['Неделя', 'Месяц', 'Квартал', 'Год', 'Прошлый год']
            columns = ['Среднее', 'Медиана', 'Δ от ср.', 'Δ от мед.']

            cell_text_combined = [
                [f"{int(weekly_avg)}", f"{int(weekly_median)}", f"{'+' if delta_week > 0 else ''}{delta_week}%",
                 f"{'+' if delta_week_median > 0 else ''}{delta_week_median}%"],
                [f"{int(month_avg)}", f"{int(month_median)}", f"{'+' if delta_month > 0 else ''}{delta_month}%",
                 f"{'+' if delta_month_median > 0 else ''}{delta_month_median}%"],
                [f"{int(quarter_avg)}", f"{int(quarter_median)}", f"{'+' if delta_quarter > 0 else ''}{delta_quarter}%",
                 f"{'+' if delta_quarter_median > 0 else ''}{delta_quarter_median}%"],
                [f"{int(year_avg)}", f"{int(year_median)}", f"{'+' if delta_year > 0 else ''}{delta_year}%",
                 f"{'+' if delta_year_median > 0 else ''}{delta_year_median}%"],
                [f"{last_year_flights}", "-", f"{'+' if delta_last_year > 0 else ''}{delta_last_year}%", "-"]
            ]

            colors_combined = []
            for row in cell_text_combined:
                row_colors = ['white', 'white']
                for delta_text in row[2:]:
                    if delta_text == "-":
                        row_colors.append('white')
                    else:
                        delta_value = float(delta_text.replace('%', '').replace('+', ''))
                        row_colors.append('#ff6b6b' if delta_value < 0 else '#51cf66')
                colors_combined.append(row_colors)

            table_combined = ax.table(cellText=cell_text_combined,
                                      rowLabels=rows,
                                      colLabels=columns,
                                      rowColours=['#f8f9fa'] * len(rows),
                                      colColours=['#f8f9fa'] * len(columns),
                                      cellColours=colors_combined,
                                      cellLoc='center',
                                      loc='center',
                                      bbox=self.STYLE["bbox_table"])

            table_combined.auto_set_font_size(False)
            table_combined.set_fontsize(self.STYLE["table_fontsize"])
            table_combined.scale(*self.STYLE["scale_table"])

            for (row, col), cell in table_combined.get_celld().items():
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
            # Если что-то пошло не так, показываем сообщение об ошибке
            error_label = tk.Label(self, text=f"Ошибка при создании графика: {str(e)}", fg="red")
            error_label.pack(pady=20)
