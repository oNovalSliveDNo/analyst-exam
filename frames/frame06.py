import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


class Frame06(tk.Frame):
    def __init__(self, parent, style, current_dataframe):
        super().__init__(parent)
        self.configure(borderwidth=2, relief="groove")

        self.STYLE = style
        self.current_dataframe = current_dataframe
        self.create_widgets()

    def create_widgets(self):
        """Метод для создания виджетов фрейма"""
        df = self.current_dataframe # pd.read_csv("transformed.csv", parse_dates=["Date"])
        df_minor_delay = df[df['DelayCategory'] == 'Малая']
        latest_date = df['Date'].max()
        today = latest_date.date()

        today_minor_delay = df_minor_delay[df_minor_delay['Date'].dt.date == today].shape[0]

        last_week_start = today - timedelta(days=today.weekday() + 7)
        last_week_end = last_week_start + timedelta(days=6)
        month_start = datetime(today.year, today.month, 1).date()
        quarter = (today.month - 1) // 3 + 1
        quarter_start = datetime(today.year, 3 * (quarter - 1) + 1, 1).date()
        year_start = datetime(today.year, 1, 1).date()
        last_year_date = datetime(today.year - 1, today.month, today.day).date()

        last_year_value = df_minor_delay[df_minor_delay['Date'].dt.date == last_year_date].shape[0]

        weekly_avg = df_minor_delay[(df_minor_delay['Date'].dt.date >= last_week_start) &
                                    (df_minor_delay['Date'].dt.date <= last_week_end)].shape[0] / 7

        month_avg = df_minor_delay[(df_minor_delay['Date'].dt.date >= month_start) &
                                   (df_minor_delay['Date'].dt.date < latest_date.date())].shape[0] / (
                            latest_date.day - 1)

        quarter_avg = df_minor_delay[(df_minor_delay['Date'].dt.date >= quarter_start) &
                                     (df_minor_delay['Date'].dt.date < latest_date.date())].shape[0] / (
                          (latest_date.date() - quarter_start).days)

        year_avg = df_minor_delay[(df_minor_delay['Date'].dt.date >= year_start) &
                                  (df_minor_delay['Date'].dt.date < latest_date.date())].shape[0] / (
                       (latest_date.date() - year_start).days)

        def get_daily_counts(df_input, start_date, end_date):
            return df_input[(df_input['Date'].dt.date >= start_date) & (df_input['Date'].dt.date <= end_date)] \
                .groupby(df_input['Date'].dt.date).size()

        weekly_median = get_daily_counts(df_minor_delay, last_week_start, last_week_end).median()
        month_median = get_daily_counts(df_minor_delay, month_start, latest_date.date() - timedelta(days=1)).median()
        quarter_median = get_daily_counts(df_minor_delay, quarter_start,
                                          latest_date.date() - timedelta(days=1)).median()
        year_median = get_daily_counts(df_minor_delay, year_start, latest_date.date() - timedelta(days=1)).median()

        def calc_delta(current, reference):
            if reference == 0:
                return 0
            return round((current - reference) / reference * 100, 1)

        delta_week = calc_delta(today_minor_delay, weekly_avg)
        delta_month = calc_delta(today_minor_delay, month_avg)
        delta_quarter = calc_delta(today_minor_delay, quarter_avg)
        delta_year = calc_delta(today_minor_delay, year_avg)
        delta_last_year = calc_delta(today_minor_delay, last_year_value)

        delta_week_median = calc_delta(today_minor_delay, weekly_median)
        delta_month_median = calc_delta(today_minor_delay, month_median)
        delta_quarter_median = calc_delta(today_minor_delay, quarter_median)
        delta_year_median = calc_delta(today_minor_delay, year_median)

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
            [f"{last_year_value}", "-", f"{'+' if delta_last_year > 0 else ''}{delta_last_year}%", "-"]
        ]

        colors_combined = []
        for row in cell_text_combined:
            row_colors = ['white', 'white']
            for delta_text in row[2:]:
                if delta_text == "-":
                    row_colors.append('white')
                else:
                    delta_value = float(delta_text.replace('%', '').replace('+', ''))
                    row_colors.append('#51cf66' if delta_value < 0 else '#ff6b6b')
            colors_combined.append(row_colors)

        fig, ax = plt.subplots(figsize=self.STYLE["figsize"], facecolor='#fff8f2')
        fig.suptitle(f"ДАТА: {latest_date.strftime('%d.%m.%Y')}",
                     fontsize=self.STYLE["title_fontsize"],
                     x=self.STYLE["title_X"],  # позиция по X
                     y=self.STYLE["title_Y"],
                     weight=self.STYLE["title_weight"],
                     ha=self.STYLE["title_ha"]  # выравнивание
                     )

        ax.text(self.STYLE["kpi_1"], self.STYLE["kpi_2"],
                f"КОЛ-ВО РЕЙСОВ\nС МАЛОЙ ЗАДЕРЖКОЙ: {today_minor_delay}",
                fontsize=self.STYLE["kpi_fontsize"],
                ha=self.STYLE["kpi_ha"],
                va=self.STYLE["kpi_va"],
                weight=self.STYLE["kpi_weight"],
                bbox=dict(facecolor='#ffc078',
                          alpha=0.2,
                          pad=self.STYLE["kpi_pad"]))

        table_combined = ax.table(cellText=cell_text_combined,
                                  rowLabels=rows,
                                  colLabels=columns,
                                  rowColours=['#fff3e0'] * len(rows),
                                  colColours=['#fff3e0'] * len(columns),
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

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10)
