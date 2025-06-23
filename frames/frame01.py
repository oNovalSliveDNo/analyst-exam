import seaborn as sns
import tkinter as tk
from tkinter import ttk
from frames.frame02 import Frame02
from frames.frame03 import Frame03
from frames.frame04 import Frame04
from frames.frame05 import Frame05
from frames.frame06 import Frame06
from frames.frame07 import Frame07
from frames.frame08 import Frame08
from frames.frame09 import Frame09
from frames.frame10 import Frame10
from frames.frame_view01 import FrameOverview01
from frames.frame_view02 import FrameOverview02
from frames.frame_view03 import FrameOverview03
from frames.frame_stat_passengers01 import FrameStatPassengers01
from frames.frame_stat_passengers02 import FrameStatPassengers02
from frames.frame_stat_flight03 import FrameStatFlight03
from frames.frame_stat_flight04 import FrameStatFlight04
from frames.frame_stat_flight05 import FrameStatFlight05
from frames.frame_stat_flight06 import FrameStatFlight06


class Frame01(tk.Frame):
    def __init__(self, parent, current_dataframe):
        super().__init__(parent)
        self.configure(borderwidth=2, relief="groove")

        # Стили для графиков
        self.STYLE1 = {
            "figsize": (10, 6),
            "title_fontsize": 12,
            "title_Y": 0.07,
            "title_X": 0.97,
            "title_weight": "bold",
            "title_ha": "right",
            "kpi_fontsize": 16,
            "kpi_weight": "normal",
            "kpi_1": 0.02,
            "kpi_2": 1.09,
            "kpi_pad": 10,
            "kpi_ha": "left",
            "kpi_va": "top",
            "table_fontsize": 14,
            "header_fontsize": 14,
            "bbox_table": [0.27, 0.12, 0.73, 0.7],
            "scale_table": (1, 2),
            "cell_height": 0.15
        }

        # Красивый единый стиль графиков
        self.GRAPH_STYLE = {
            "palette": "crest",  # Выразительная цветовая палитра
            "title_fontsize": 14,
            "label_fontsize": 12,
            "tick_fontsize": 10,
            "grid": True,
            "facecolor": "#f8f9fa",  # Светлый фон
            "edgecolor": "#dee2e6",  # Цвет сетки и рамки
            "line_color": "#2a9d8f",
            "bar_color": "#264653",
            "pie_colors": sns.color_palette("Set2")
        }

        self.current_dataframe = current_dataframe
        self.create_widgets()

    def create_widgets(self):
        """Метод для создания виджетов фрейма"""
        # Создаем Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)

        # Создаем вкладки
        self.tab0 = ttk.Frame(self.notebook)
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        self.tab4 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab0, text="Данные")
        self.notebook.add(self.tab1, text="KPI на сегодня")
        self.notebook.add(self.tab2, text="Обзор на сегодня")
        self.notebook.add(self.tab3, text="Cтатистика Пассажиропоток")
        self.notebook.add(self.tab4, text="Cтатистика Рейсы")

        # Добавляем содержимое вкладок
        self.create_tab0_content()
        self.create_tab1_content()
        self.create_tab2_content()
        self.create_tab3_content()
        self.create_tab4_content()

    def create_tab0_content(self):
        """Создаем содержимое вкладки с данными"""
        # Панель с информацией о DataFrame
        info_frame = ttk.Frame(self.tab0)
        info_frame.pack(fill="x", padx=5, pady=5)

        # Информация о размере DataFrame с улучшенным шрифтом
        ttk.Label(info_frame,
                  text=f"Записей: {len(self.current_dataframe)}, Колонок: {len(self.current_dataframe.columns)}",
                  font=('Segoe UI', 10, 'bold')).pack(side="left", padx=5)

        # Стилизованная кнопка для отображения информации о типах данных
        ttk.Button(info_frame, text="Показать типы данных",
                   command=self.show_dtypes,
                   style='Accent.TButton').pack(side="right", padx=5)

        # Создаем фрейм для таблицы с прокруткой
        table_frame = ttk.Frame(self.tab0)
        table_frame.pack(expand=True, fill="both", padx=5, pady=5)

        # Создаем Treeview для отображения данных
        self.create_data_table(table_frame)

        # Фрейм для отображения информации о типах данных
        self.dtypes_frame = ttk.Frame(self.tab0)
        self.dtypes_label = ttk.Label(self.dtypes_frame, text="", font=('Segoe UI', 9))
        self.dtypes_label.pack(padx=5, pady=5)

    def create_data_table(self, parent):
        """Создает таблицу для отображения данных"""
        # Создаем стиль для Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading",
                        font=('Segoe UI', 10, 'bold'),
                        background="#4fc3f7",  # голубой цвет шапки
                        foreground="black")
        style.configure("Treeview",
                        font=('Segoe UI', 9),
                        rowheight=25,
                        background="white",  # основной цвет фона
                        fieldbackground="white")
        style.map("Treeview",
                  background=[('selected', '#0277bd')],  # цвет выделенной строки
                  foreground=[('selected', 'white')])

        # Чередование цветов строк
        style.map("Treeview.Row",
                  background=[('!selected', '#f5f5f5'), ('!selected', 'white')])  # светло-серый и белый

        # Создаем Treeview с прокруткой
        scroll_y = ttk.Scrollbar(parent, orient="vertical")
        scroll_x = ttk.Scrollbar(parent, orient="horizontal")

        self.data_table = ttk.Treeview(parent,
                                       yscrollcommand=scroll_y.set,
                                       xscrollcommand=scroll_x.set,
                                       style="Treeview")

        scroll_y.config(command=self.data_table.yview)
        scroll_x.config(command=self.data_table.xview)

        # Настройка колонок
        self.data_table["columns"] = list(self.current_dataframe.columns)
        self.data_table["show"] = "headings"

        # Заголовки колонок
        for column in self.current_dataframe.columns:
            self.data_table.heading(column, text=column)
            self.data_table.column(column, width=100, anchor="center")

        # Добавляем данные с чередованием цветов
        for i, (_, row) in enumerate(self.current_dataframe.iterrows()):
            tag = 'even' if i % 2 == 0 else 'odd'
            self.data_table.insert("", "end", values=list(row), tags=(tag,))

        # Настраиваем теги для чередования цветов
        self.data_table.tag_configure('even', background='#f5f5f5')  # светло-серый
        self.data_table.tag_configure('odd', background='white')  # белый

        # Размещаем элементы
        self.data_table.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        # Настройка grid
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)

    def show_dtypes(self):
        """Отображает информацию о типах данных"""
        dtypes_info = "\n".join([f"{col.ljust(25)}{dtype}"
                                 for col, dtype in self.current_dataframe.dtypes.items()])

        if not self.dtypes_frame.winfo_ismapped():
            self.dtypes_frame.pack(fill="x", padx=5, pady=5)
            self.dtypes_label.config(text=dtypes_info)
        else:
            self.dtypes_frame.pack_forget()

    def create_tab1_content(self):
        """Создаем содержимое первой вкладки"""
        # Конфигурация grid для tab1
        self.tab1.grid_columnconfigure(0, weight=1)
        self.tab1.grid_columnconfigure(1, weight=1)
        self.tab1.grid_columnconfigure(2, weight=1)

        self.tab1.grid_rowconfigure(0, weight=1)
        self.tab1.grid_rowconfigure(1, weight=1)
        self.tab1.grid_rowconfigure(2, weight=1)
        self.tab1.grid_rowconfigure(3, weight=1)

        # Создаем фреймы во вкладке 1
        self.frame2 = Frame02(self.tab1, self.STYLE1, self.current_dataframe)
        self.frame2.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.frame3 = Frame03(self.tab1, self.STYLE1, self.current_dataframe)
        self.frame3.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.frame4 = Frame04(self.tab1, self.STYLE1, self.current_dataframe)
        self.frame4.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        self.frame5 = Frame05(self.tab1, self.STYLE1, self.current_dataframe)
        self.frame5.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.frame6 = Frame06(self.tab1, self.STYLE1, self.current_dataframe)
        self.frame6.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.frame7 = Frame07(self.tab1, self.STYLE1, self.current_dataframe)
        self.frame7.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

        self.frame8 = Frame08(self.tab1, self.STYLE1, self.current_dataframe)
        self.frame8.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        self.frame9 = Frame09(self.tab1, self.STYLE1, self.current_dataframe)
        self.frame9.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        self.frame10 = Frame10(self.tab1, self.STYLE1, self.current_dataframe)
        self.frame10.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

    def create_tab2_content(self):
        """Создаем содержимое вкладки Обзор на сегодня"""
        self.tab2.grid_rowconfigure(1, weight=1)
        self.tab2.grid_rowconfigure(2, weight=1)
        self.tab2.grid_columnconfigure(1, weight=1)
        self.tab2.grid_columnconfigure(2, weight=1)

        overview1 = FrameOverview01(self.tab2, self.current_dataframe, self.GRAPH_STYLE)
        overview1.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=5, pady=5)

        overview2 = FrameOverview02(self.tab2, self.current_dataframe, self.GRAPH_STYLE)
        overview2.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        overview3 = FrameOverview03(self.tab2, self.current_dataframe, self.GRAPH_STYLE)
        overview3.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

    def create_tab3_content(self):
        """Создаем содержимое вкладки Общая статистика пассажиропотока"""

        # Создаем PanedWindow с вертикальной ориентацией
        self.paned = ttk.PanedWindow(self.tab3, orient="vertical")
        self.paned.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Настраиваем расширение PanedWindow
        self.tab3.grid_columnconfigure(0, weight=1)
        self.tab3.grid_rowconfigure(0, weight=1)

        # Добавляем фреймы в PanedWindow
        self.stat_frame1 = FrameStatPassengers01(self.paned, self.current_dataframe)
        self.paned.add(self.stat_frame1, weight=1)

        self.stat_frame2 = FrameStatPassengers02(self.paned, self.current_dataframe)
        self.paned.add(self.stat_frame2, weight=1)

    def create_tab4_content(self):
        """Создаем содержимое вкладки Общая статистика рейсов"""

        for i in range(2):
            self.tab4.grid_columnconfigure(i, weight=1)
        for j in range(2):
            self.tab4.grid_rowconfigure(j, weight=1)

        self.stat_frame3 = FrameStatFlight03(self.tab4, self.current_dataframe)
        self.stat_frame3.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.stat_frame4 = FrameStatFlight04(self.tab4, self.current_dataframe)
        self.stat_frame4.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.stat_frame5 = FrameStatFlight05(self.tab4, self.current_dataframe)
        self.stat_frame5.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.stat_frame6 = FrameStatFlight06(self.tab4, self.current_dataframe)
        self.stat_frame6.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
