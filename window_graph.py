import tkinter as tk
from tkinter import Canvas
from app_state import AppState
from app_constants import AppConstants
from typing import cast
from db_connection import DBConnector
from sql_queries import SQLQueries
import datetime


class GraphWindow:
    def __init__(self, parent_window, database):
        self.window = tk.Tk()
        AppState.graph_is_open = True
        self.parent_window = parent_window
        self.window.title("Graph Window")
        self._get_all_work(database)
        self._adjust_window_position()
        self._make_window_draggable()
        self._create_ui_elements()

    def _get_all_work(self, database):
        db = cast(DBConnector, database)
        db.connect()
        eight_hours_in_seconds = 8 * 60 * 60
        data = db.fetch_data(SQLQueries.GET_ALL_WORK_COMPLETED)
        results = [(data, round((work_completed / eight_hours_in_seconds) * 100, 1)) for date, work_completed in data]
        db.disconnect()
        AppState.all_work = results

    def _adjust_window_position(self):
        parent_x = self.parent_window.winfo_x()
        parent_y = self.parent_window.winfo_y()
        self.window.geometry('{}x{}+{}+{}'.format(AppConstants.GRAPH_WINDOW_WIDTH,
                                                  AppConstants.GRAPH_WINDOW_HEIGHT,
                                                  parent_x, parent_y + AppConstants.COUNTDOWN_WINDOW_HEIGHT))

        self.window.resizable(False, False)
        self.window.minsize(AppConstants.GRAPH_WINDOW_WIDTH, AppConstants.GRAPH_WINDOW_HEIGHT)
        self.window.attributes('-topmost', True)
        self.window.overrideredirect(True)
        self.window.config(bg=AppConstants.COLOR_BLACK)

    def _make_window_draggable(self):
        self.window.bind("<ButtonPress-1>", self._start_moving_window)
        self.window.bind("<ButtonRelease-1>", self._stop_moving_window)
        self.window.bind("<B1-Motion>", self._on_window_move)

    def _start_moving_window(self, event):
        AppState.drag_start_x = event.x
        AppState.drag_start_y = event.y

    def _stop_moving_window(self, event):
        AppState.drag_start_x = None
        AppState.drag_start_y = None

    def _on_window_move(self, event):
        dx = event.x - AppState.drag_start_x
        dy = event.y - AppState.drag_start_y
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        win_width = self.window.winfo_width()
        win_height = self.window.winfo_height()
        win_x = self.window.winfo_x()
        win_y = self.window.winfo_y()
        x = win_x + dx
        y = win_y + dy

        self.window.geometry(f"+{x}+{y}")

    def _create_ui_elements(self):
        canvas = Canvas(self.window, width=180, height=200, bg=AppConstants.COLOR_BLACK, highlightthickness=0)
        canvas.place(x=10, y=0)
        canvas_height = 180
        canvas_width = 180
        margin = 25
        max_percentage = 100
        y_scale = (canvas_height - 2 * margin) / max_percentage
        dates = [datetime.datetime.strptime(date, '%Y-%m-%d') for date, _ in AppState.all_work]
        num_dates = len(dates)
        x_scale = (canvas_width - 2 * margin) / (num_dates - 1) if num_dates > 1 else 0
        canvas.create_line(margin, canvas_height - margin, canvas_width - margin, canvas_height - margin, fill='white')
        canvas.create_line(margin, canvas_height - margin, margin, margin, fill='white')
        for i in range(0, max_percentage + 1, 10):
            y = canvas_height - margin - i *y_scale
            canvas.create_line(margin - 1, y, margin, y, fill='white')
            if i % 20 == 0:
                canvas.create_text(margin - 6, y, text=str(i), anchor=tk.E, fill=AppConstants.COLOR_ORANGE)
        prev_x = None
        prev_y = None
        for i, (date_str, percentage) in enumerate(AppState.all_work):
            x = margin + i * x_scale
            y = canvas_height - margin - percentage * y_scale
            canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill='white')
            if prev_x is not None and prev_y is not None:
                canvas.create_line(prev_x, prev_y, x, y, fill=AppConstants.COLOR_ORANGE)
            prev_x = x
            prev_y = y
            if i == int((len(AppState.all_work) - 1) / 2):
                canvas.create_text(x, canvas_height - margin + 10, text='Percentage/Days', anchor=tk.W, angle=0,
                                   fill=AppConstants.COLOR_ORANGE)


    def display(self):
        self.window.mainloop()

    def close(self, event):
        AppState.graph_is_open = False
        self.window.destroy()