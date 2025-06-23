import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


class Frame10(tk.Frame):
    def __init__(self, parent, style, current_dataframe):
        super().__init__(parent)
        self.configure(borderwidth=2, relief="groove")

        self.STYLE = style
        self.current_dataframe = current_dataframe
        self.create_widgets()

    def create_widgets(self):
        """Метод для создания виджетов фрейма"""

        df = self.current_dataframe # pd.read_csv("transformed.csv", parse_dates=["Date"])
        latest_date = df['Date'].max().date()

        df_cancelled = df[df['IsCancelled'] == True]
        today_cancelled = df_cancelled[df_cancelled['Date'].dt.date == latest_date].shape[0]

        last_week_start = latest_date - timedelta(days=latest_date.weekday() + 7)
        last_week_end = last_week_start + timedelta(days=6)
        month_start = datetime(latest_date.year, latest_date.month, 1).date()
        quarter = (latest_date.month - 1) // 3 + 1
        quarter_start = datetime(latest_date.year, 3 * (quarter - 1) + 1, 1).date()
        year_start = datetime(latest_date.year, 1, 1).date()
        last_year_date = datetime(latest_date.year - 1, latest_date.month, latest_date.day).date()

        week_cancelled = df_cancelled[(df_cancelled['Date'].dt.date >= last_week_start) &
                                      (df_cancelled['Date'].dt.date <= last_week_end)].shape[0]

        month_cancelled = df_cancelled[(df_cancelled['Date'].dt.date >= month_start) &
                                       (df_cancelled['Date'].dt.date < latest_date)].shape[0]

        quarter_cancelled = df_cancelled[(df_cancelled['Date'].dt.date >= quarter_start) &
                                         (df_cancelled['Date'].dt.date < latest_date)].shape[0]

        year_cancelled = df_cancelled[(df_cancelled['Date'].dt.date >= year_start) &
                                      (df_cancelled['Date'].dt.date < latest_date)].shape[0]

        last_year_cancelled = df_cancelled[df_cancelled['Date'].dt.date == last_year_date].shape[0]

        def calc_delta(current, reference):
            if reference == 0:
                return 0
            return round((current - reference) / reference * 100, 1)

        delta_week = calc_delta(today_cancelled, week_cancelled)
        delta_month = calc_delta(today_cancelled, month_cancelled)
        delta_quarter = calc_delta(today_cancelled, quarter_cancelled)
        delta_year = calc_delta(today_cancelled, year_cancelled)
        delta_last_year = calc_delta(today_cancelled, last_year_cancelled)

        rows = ['Неделя', 'Месяц', 'Квартал', 'Год', 'Прошлый год']
        columns = ['Кол-во за период', 'Δ от периода']

        cell_text = [
            [f"{week_cancelled}", f"{'+' if delta_week > 0 else ''}{delta_week}%"],
            [f"{month_cancelled}", f"{'+' if delta_month > 0 else ''}{delta_month}%"],
            [f"{quarter_cancelled}", f"{'+' if delta_quarter > 0 else ''}{delta_quarter}%"],
            [f"{year_cancelled}", f"{'+' if delta_year > 0 else ''}{delta_year}%"],
            [f"{last_year_cancelled}", f"{'+' if delta_last_year > 0 else ''}{delta_last_year}%"]
        ]

        colors = []
        for row in cell_text:
            row_colors = ['white']
            delta_value = float(row[1].replace('%', '').replace('+', ''))
            row_colors.append('#51cf66' if delta_value < 0 else '#ff6b6b')
            colors.append(row_colors)

        fig, ax = plt.subplots(figsize=self.STYLE["figsize"], facecolor='#fff0f0')
        fig.suptitle(f"ДАТА: {latest_date.strftime('%d.%m.%Y')}",
                     fontsize=self.STYLE["title_fontsize"],
                     x=self.STYLE["title_X"],  # позиция по X
                     y=self.STYLE["title_Y"],
                     weight=self.STYLE["title_weight"],
                     ha=self.STYLE["title_ha"]  # выравнивание
                     )

        ax.text(self.STYLE["kpi_1"],
                self.STYLE["kpi_2"],
                f"КОЛ-ВО ОТМЕНЁННЫХ РЕЙСОВ: {today_cancelled}",
                fontsize=self.STYLE["kpi_fontsize"],
                ha=self.STYLE["kpi_ha"],
                va=self.STYLE["kpi_va"],
                weight=self.STYLE["kpi_weight"],
                bbox=dict(facecolor='#fa5252',
                          alpha=0.2,
                          pad=self.STYLE["kpi_pad"]
                          )
                )

        table = ax.table(cellText=cell_text,
                         rowLabels=rows,
                         colLabels=columns,
                         rowColours=['#ffe3e3'] * len(rows),
                         colColours=['#ffe3e3'] * len(columns),
                         cellColours=colors,
                         cellLoc='center',
                         loc='center',
                         bbox=self.STYLE["bbox_table"]
                         )

        table.auto_set_font_size(False)
        table.set_fontsize(self.STYLE["table_fontsize"])
        table.scale(*self.STYLE["scale_table"])

        for (row, col), cell in table.get_celld().items():
            if row == 0:
                cell.set_text_props(weight='bold', fontsize=self.STYLE["header_fontsize"])
            cell.set_edgecolor('#dee2e6')
            cell.set_height(self.STYLE["cell_height"])

        ax.axis('off')
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
