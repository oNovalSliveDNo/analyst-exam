import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns


def apply_common_style(ax, title, xlabel="", ylabel=""):
    ax.set_title(title, fontsize=14, weight='bold', pad=15)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    sns.despine()
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")


def add_value_labels(ax, orient="v"):
    """Добавляет подписи к столбцам"""
    for container in ax.containers:
        if orient == "v":
            ax.bar_label(container, fmt='%d', label_type='edge', padding=3, fontsize=9)
        else:
            ax.bar_label(container, fmt='%d', label_type='edge', padding=3, fontsize=9)


class FrameStatFlight03(tk.Frame):
    def __init__(self, parent, df):
        super().__init__(parent)
        self.df = df.copy()
        self.configure(borderwidth=2, relief="ridge")
        self.create_plot()

    def create_plot(self):
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.set_theme(style="whitegrid")
        plot = sns.countplot(data=self.df, x="TimeOfDay", order=["Ночь", "Утро", "День", "Вечер"], palette="pastel", ax=ax)
        apply_common_style(ax, "Распределение рейсов по времени суток", "Время суток", "Количество рейсов")
        add_value_labels(ax, orient="v")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)