import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import numpy as np
from matplotlib import ticker
from matplotlib.animation import FuncAnimation


class FrameOverview03(tk.Frame):
    def __init__(self, parent, dataframe, style):
        super().__init__(parent)
        self.df = dataframe
        self.style = {
            "bg_color": "#2E3440",
            "bar_color": "#88C0D0",
            "highlight_color": "#BF616A",
            "text_color": "#E5E9F0",
            "grid_color": "#4C566A",
            "title_font": {"family": "sans-serif", "weight": "bold", "size": 14},
            "label_font": {"family": "sans-serif", "size": 12},
            "tick_font": {"family": "sans-serif", "size": 10},
            "annotation_font": {"family": "sans-serif", "size": 9, "weight": "bold"},
            "palette": "mako"
        }
        self.create_plot()

    def create_plot(self):
        # Prepare data
        latest_date = self.df['Date'].max().date()
        self.today = latest_date
        today_df = self.df[self.df['Date'].dt.date == latest_date]
        self.top_routes = today_df.groupby("Airport_arr")["Total_Passengers"].sum().sort_values(ascending=False).head(
            10)

        # Create figure with dynamic size
        self.fig, self.ax = plt.subplots(figsize=(6, 4), facecolor=self.style["bg_color"])  # Smaller initial size
        self.fig.subplots_adjust(left=0.3, right=0.95, top=0.9, bottom=0.1)

        # Setup style
        plt.style.use('dark_background')
        sns.set_theme(style="darkgrid", palette=self.style["palette"])

        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(expand=True, fill="both", padx=5, pady=5)

        # Bind resize event
        self.bind("<Configure>", self.on_resize)

        # Create initial plot
        self.setup_plot()
        self.create_animation()

    def setup_plot(self):
        """Setup the initial plot configuration"""
        self.ax.clear()
        self.ax.set_facecolor(self.style["bg_color"])
        self.ax.grid(True, color=self.style["grid_color"], linestyle='--', alpha=0.7)

        for spine in self.ax.spines.values():
            spine.set_edgecolor(self.style["grid_color"])

        # Set titles and labels
        self.ax.set_title(
            f"ТОП-10 САМЫХ ЗАГРУЖЕННЫХ НАПРАВЛЕНИЙ\n{self.today.strftime('%d %B %Y').upper()}",
            fontdict={
                "family": "sans-serif",
                "weight": "bold",
                "size": self.scale_font(12),  # Scaled font
                "color": self.style["text_color"]
            },
            pad=self.scale_value(20)
        )

        self.ax.set_xlabel(
            "ОБЩЕЕ КОЛИЧЕСТВО ПАССАЖИРОВ",
            fontdict={
                "family": "sans-serif",
                "size": self.scale_font(10),
                "color": self.style["text_color"]
            },
            labelpad=self.scale_value(10)
        )

        self.ax.set_ylabel(
            "АЭРОПОРТ НАЗНАЧЕНИЯ",
            fontdict={
                "family": "sans-serif",
                "size": self.scale_font(10),
                "color": self.style["text_color"]
            },
            labelpad=self.scale_value(10)
        )

        self.ax.tick_params(
            axis='both',
            colors=self.style["text_color"],
            labelsize=self.scale_font(8)
        )
        self.ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

    def create_animation(self):
        """Create the animation"""

        def animate(i):
            y_data = self.top_routes.index[:i + 1]
            x_data = self.top_routes.values[:i + 1]

            self.ax.clear()
            self.setup_plot()  # Reapply styling

            bars = self.ax.barh(y_data, x_data, color=self.style["bar_color"], height=0.7)

            # Highlight the top bar
            if i > 0:
                bars[-1].set_color(self.style["highlight_color"])

            # Add value labels
            for bar in bars:
                width = bar.get_width()
                self.ax.text(
                    width + max(self.top_routes.values) * 0.02,
                    bar.get_y() + bar.get_height() / 2,
                    f'{width:,.0f}',
                    ha='left',
                    va='center',
                    fontdict={
                        "family": "sans-serif",
                        "size": self.scale_font(8),
                        "weight": "bold",
                        "color": self.style["text_color"]
                    }
                )

            return bars,

        self.anim = FuncAnimation(
            self.fig, animate, frames=len(self.top_routes), interval=500, blit=False, repeat=False
        )

    def on_resize(self, event):
        """Handle window resize event"""
        if event.width < 10 or event.height < 10:  # Ignore minimal sizes
            return

        # Calculate new figure size (in inches, considering DPI)
        dpi = self.fig.get_dpi()
        new_width = event.width / dpi - 1  # Subtract some padding
        new_height = event.height / dpi - 1

        # Set minimum size
        new_width = max(4, new_width)
        new_height = max(3, new_height)

        # Update figure size
        self.fig.set_size_inches(new_width, new_height)

        # Adjust subplot parameters dynamically
        left = 0.35 - (0.05 * (6 / new_width))  # Adjust left margin based on width
        right = 0.95 - (0.1 * (6 / new_width))
        top = 0.9 - (0.1 * (4 / new_height))

        self.fig.subplots_adjust(left=left, right=right, top=top, bottom=0.15)

        # Redraw the canvas
        self.canvas.draw()

    def scale_font(self, base_size):
        """Scale font size based on figure dimensions"""
        fig_width, fig_height = self.fig.get_size_inches()
        return max(6, base_size * min(fig_width / 6, fig_height / 4))

    def scale_value(self, base_value):
        """Scale padding/margin values based on figure dimensions"""
        fig_width, fig_height = self.fig.get_size_inches()
        return base_value * min(fig_width / 6, fig_height / 4)