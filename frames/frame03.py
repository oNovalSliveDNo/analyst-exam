import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta


class Frame03(tk.Frame):
    def __init__(self, parent, style, current_dataframe):
        super().__init__(parent)
        self.configure(borderwidth=2, relief="groove")

        self.STYLE = style
        self.current_dataframe = current_dataframe

        self.create_passengers_chart()

    def create_passengers_chart(self):
        try:
            # Читаем данные
            df = self.current_dataframe # = pd.read_csv("transformed.csv", parse_dates=["Date"])

            # Берём последний день
            latest_date = df['Date'].max().date()
            df_latest = df[df['Date'].dt.date == latest_date]
            today_passengers = df_latest['Total_Passengers'].sum()

            # Вычисляем метрики
            last_week_start = latest_date - timedelta(days=latest_date.weekday() + 7)
            last_week_end = last_week_start + timedelta(days=6)
            weekly_sum = df[(df['Date'].dt.date >= last_week_start) &
                            (df['Date'].dt.date <= last_week_end)]['Total_Passengers'].sum()
            weekly_avg_p = weekly_sum / 7

            month_start = datetime(latest_date.year, latest_date.month, 1).date()
            month_sum = df[(df['Date'].dt.date >= month_start) &
                           (df['Date'].dt.date < latest_date)]['Total_Passengers'].sum()
            month_avg_p = month_sum / (latest_date.day - 1)

            quarter_start = datetime(latest_date.year, 4, 1).date()
            quarter_sum = df[(df['Date'].dt.date >= quarter_start) &
                             (df['Date'].dt.date < latest_date)]['Total_Passengers'].sum()
            quarter_avg_p = quarter_sum / (latest_date - quarter_start).days

            year_start = datetime(latest_date.year, 1, 1).date()
            year_sum = df[(df['Date'].dt.date >= year_start) &
                          (df['Date'].dt.date < latest_date)]['Total_Passengers'].sum()
            year_avg_p = year_sum / (latest_date - year_start).days

            def get_daily_passenger_counts(start_date, end_date):
                return df[(df['Date'].dt.date >= start_date) &
                          (df['Date'].dt.date <= end_date)] \
                    .groupby(df['Date'].dt.date)['Total_Passengers'].sum()

            weekly_median_p = get_daily_passenger_counts(last_week_start, last_week_end).median()
            month_median_p = get_daily_passenger_counts(month_start, latest_date - timedelta(days=1)).median()
            quarter_median_p = get_daily_passenger_counts(quarter_start, latest_date - timedelta(days=1)).median()
            year_median_p = get_daily_passenger_counts(year_start, latest_date - timedelta(days=1)).median()

            last_year_date = datetime(latest_date.year - 1, latest_date.month, latest_date.day).date()
            last_year_passengers = df[df['Date'].dt.date == last_year_date]['Total_Passengers'].sum()

            def calc_delta(current, reference):
                if reference == 0:
                    return 0
                return round((current - reference) / reference * 100, 1)

            delta_p_week = calc_delta(today_passengers, weekly_avg_p)
            delta_p_month = calc_delta(today_passengers, month_avg_p)
            delta_p_quarter = calc_delta(today_passengers, quarter_avg_p)
            delta_p_year = calc_delta(today_passengers, year_avg_p)
            delta_p_last_year = calc_delta(today_passengers, last_year_passengers)

            delta_p_week_median = calc_delta(today_passengers, weekly_median_p)
            delta_p_month_median = calc_delta(today_passengers, month_median_p)
            delta_p_quarter_median = calc_delta(today_passengers, quarter_median_p)
            delta_p_year_median = calc_delta(today_passengers, year_median_p)

            # Создаем фигуру matplotlib
            fig, ax = plt.subplots(figsize=self.STYLE["figsize"], facecolor='#eefaf9')
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
                    f"КОЛ-ВО ПАССАЖИРОВ\nЗА ДЕНЬ: {int(today_passengers)}",
                    fontsize=self.STYLE["kpi_fontsize"],
                    ha=self.STYLE["kpi_ha"],
                    va=self.STYLE["kpi_va"],
                    weight=self.STYLE["kpi_weight"],
                    bbox=dict(facecolor='#00b894',
                              alpha=0.2,
                              pad=self.STYLE["kpi_pad"]))

            # Таблица с метриками
            rows = ['Неделя', 'Месяц', 'Квартал', 'Год', 'Прошлый год']
            columns = ['Среднее', 'Медиана', 'Δ от ср.', 'Δ от мед.']

            cell_text_passengers = [
                [f"{int(weekly_avg_p)}", f"{int(weekly_median_p)}", f"{'+' if delta_p_week > 0 else ''}{delta_p_week}%",
                 f"{'+' if delta_p_week_median > 0 else ''}{delta_p_week_median}%"],
                [f"{int(month_avg_p)}", f"{int(month_median_p)}", f"{'+' if delta_p_month > 0 else ''}{delta_p_month}%",
                 f"{'+' if delta_p_month_median > 0 else ''}{delta_p_month_median}%"],
                [f"{int(quarter_avg_p)}", f"{int(quarter_median_p)}",
                 f"{'+' if delta_p_quarter > 0 else ''}{delta_p_quarter}%",
                 f"{'+' if delta_p_quarter_median > 0 else ''}{delta_p_quarter_median}%"],
                [f"{int(year_avg_p)}", f"{int(year_median_p)}", f"{'+' if delta_p_year > 0 else ''}{delta_p_year}%",
                 f"{'+' if delta_p_year_median > 0 else ''}{delta_p_year_median}%"],
                [f"{int(last_year_passengers)}", "-", f"{'+' if delta_p_last_year > 0 else ''}{delta_p_last_year}%",
                 "-"]
            ]

            colors_passengers = []
            for row in cell_text_passengers:
                row_colors = ['white', 'white']
                for delta_text in row[2:]:
                    if delta_text == "-":
                        row_colors.append('white')
                    else:
                        delta_value = float(delta_text.replace('%', '').replace('+', ''))
                        row_colors.append('#ff7675' if delta_value < 0 else '#55efc4')
                colors_passengers.append(row_colors)

            table_passengers = ax.table(
                cellText=cell_text_passengers,
                rowLabels=rows,
                colLabels=columns,
                rowColours=['#f8f9fa'] * len(rows),
                colColours=['#f8f9fa'] * len(columns),
                cellColours=colors_passengers,
                cellLoc='center',
                loc='center',
                bbox=self.STYLE["bbox_table"]
            )

            table_passengers.auto_set_font_size(False)
            table_passengers.set_fontsize(self.STYLE["table_fontsize"])
            table_passengers.scale(*self.STYLE["scale_table"])

            for (row, col), cell in table_passengers.get_celld().items():
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
