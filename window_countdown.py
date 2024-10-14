import tkinter as tk
from tkinter import ttk
from window_graph import GraphWindow
from window_list import ListWindow
from window_termination import TerminationWindow
from controller_mouse import Mouse
from controller_screen import Screen
from app_state import AppState
from app_constants import AppConstants
from threading import Thread
from db_connection import DBConnector
from sql_queries import SQLQueries
from typing import cast
import datetime
import time

class CountdownWindow:
    def __init__(self, database):
        self.window = tk.Tk()
        self.window.title("Count down")
        self._graph_window = None
        self._list_window = None
        self._db = database
        self._adjust_window_position()
        self._make_window_draggable()
        self._create_ui_elements()
        self._reset_timer()
        self._initialize_database(database)

    def _adjust_window_position(self):
        # get taskbar height. it will be used for magnetic effect
        AppState.taskbar_height = Screen.get_taskbar_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_coordinate = screen_width//2 - AppConstants.COUNTDOWN_WINDOW_WIDTH//2
        y_coordinate = screen_height//2 - AppConstants.COUNTDOWN_WINDOW_HEIGHT//2 - AppState.taskbar_height
        self.window.geometry('{}x{}+{}+{}'.format(AppConstants.COUNTDOWN_WINDOW_WIDTH,
                                                  AppConstants.COUNTDOWN_WINDOW_HEIGHT,
                                                  x_coordinate, y_coordinate))

        self.window.resizable(False, False)
        self.window.minsize(AppConstants.COUNTDOWN_WINDOW_WIDTH, AppConstants.COUNTDOWN_WINDOW_HEIGHT)
        self.window.attributes('-topmost', True)
        self.window.overrideredirect(True)
        self.window.config(bg=AppConstants.COLOR_BLACK)

    def _make_window_draggable(self):
        # bind drag and drop feature to the main window
        self.window.bind('<ButtonPress-1>', self._start_moving_window)
        self.window.bind('<ButtonRelease-1>', self._stop_moving_window)
        self.window.bind('<B1-Motion>', self._on_window_move)

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
        # styles for progressbar
        style = ttk.Style()
        style.theme_use('default')
        style.configure('green.Horizontal.TProgressbar', foreground='green', background='green',
                            thickness=AppConstants.PROGRESSBAR_THICKNESS)
        style.configure('blue.Horizontal.TProgressbar', foreground='blue', background='blue',
                            thickness=AppConstants.PROGRESSBAR_THICKNESS)
        style.configure('red.Horizontal.TProgressbar', foreground='red', background='red',
                            thickness=AppConstants.PROGRESSBAR_THICKNESS)
        # window layout
        frame_countdown = tk.Frame(self.window, bg=AppConstants.COLOR_BLACK)
        frame_info = tk.Frame(self.window, bg=AppConstants.COLOR_BLACK)
        frame_buttons = tk.Frame(self.window, bg=AppConstants.COLOR_BLACK)
        frame_speed = tk.Frame(self.window, bg=AppConstants.COLOR_BLACK)
        frame_activity = tk.Frame(self.window, bg=AppConstants.COLOR_BLACK)
        frame_settings = tk.Frame(self.window, bg=AppConstants.COLOR_BLACK)
        frame_countdown.grid(row=0, column=1, pady=10)
        frame_info.grid(row=1, column=1)
        frame_buttons.grid(row=2, column=1, pady=5)
        frame_speed.grid(row=0, column=0, rowspan=3, sticky='ns', padx=4)
        frame_activity.grid(row=0, column=2, rowspan=3, sticky='ns', padx=4)
        frame_settings.grid(row=3, columnspan=3, sticky='ew', padx=10)
        # timer boxes
        self.text_hour = tk.Entry(frame_countdown, width=3, font=AppConstants.MAIN_FONT, bg=AppConstants.COLOR_BLACK,
                                  fg=AppConstants.COLOR_ORANGE, justify='center')
        self.text_minute = tk.Entry(frame_countdown, width=3, font=AppConstants.MAIN_FONT, bg=AppConstants.COLOR_BLACK,
                                  fg=AppConstants.COLOR_ORANGE, justify='center')
        self.text_second = tk.Entry(frame_countdown, width=3, font=AppConstants.MAIN_FONT, bg=AppConstants.COLOR_BLACK,
                                    fg=AppConstants.COLOR_ORANGE, justify='center')
        self.text_hour.grid(row=0, column=0, padx=5)
        self.text_minute.grid(row=0, column=1, padx=5)
        self.text_second.grid(row=0, column=2, padx=5)

        # info label
        self.label_info = tk.Label(frame_info, text='Ready.', bg=AppConstants.COLOR_BLACK, fg=AppConstants.COLOR_ORANGE)
        self.label_info.grid(row=0, column=0)
        self.label_percentage = tk.Label(frame_info, text='0.0%', bg=AppConstants.COLOR_BLACK, fg=AppConstants.COLOR_ORANGE)
        self.label_percentage.grid(row=1, column=0)
        # work and reset buttons
        button_work = tk.Button(frame_buttons, text='Work', bg=AppConstants.COLOR_ORANGE, command=self._start_timer)
        button_work.grid(row=0, column=0, padx=(0, 5))
        button_reset = tk.Button(frame_buttons, text='Reset', bg=AppConstants.COLOR_ORANGE, command=self._reset_timer)
        button_reset.grid(row=0, column=1, padx=(5, 0))

        # speed progressbar
        self.progressbar_speed = ttk.Progressbar(frame_speed, orient='vertical', mode='determinate',
                                                 style='green.Horizontal.TProgressbar')
        self.progressbar_speed.grid(row=0, column=0, rowspan=3, padx=10, pady=10)
        self.progressbar_activity = ttk.Progressbar(frame_activity, orient='vertical', mode='determinate',
                                                 style='green.Horizontal.TProgressbar')
        self.progressbar_activity.grid(row=0, column=2, padx=10, pady=10)

        # always on top checkbox
        self.checkbox_ontop_value = tk.IntVar()
        self.checkbox_ontop = tk.Checkbutton(frame_settings, text='On Top |', variable=self.checkbox_ontop_value,
                                             command=self._toggle_always_on_top, bg=AppConstants.COLOR_BLACK, fg=AppConstants.COLOR_ORANGE)
        self.checkbox_ontop.select()
        self.checkbox_ontop.pack(side=tk.LEFT)

        # close button
        self.label_close = tk.Label(frame_settings, text='Close', bg=AppConstants.COLOR_BLACK, fg=AppConstants.COLOR_ORANGE)
        self.label_close.pack(side=tk.RIGHT)
        self.label_close.bind('<Button-1>', lambda event: self._close_app(event))

        # graph button
        self.label_details = tk.Label(frame_settings, text='Graph |', bg=AppConstants.COLOR_BLACK, fg=AppConstants.COLOR_ORANGE)
        self.label_details.pack(side=tk.RIGHT)
        self.label_details.bind('<Button-1>', lambda event: self._show_graph(event))

        # list button
        self.label_list = tk.Label(frame_settings, text='List |', bg=AppConstants.COLOR_BLACK, fg=AppConstants.COLOR_ORANGE)
        self.label_list.pack(side=tk.RIGHT)
        self.label_list.bind('<Button-1>', self._show_list)

    def _initialize_database(self, database):
        db = cast(DBConnector, database)
        db.connect()
        db.execute_query(SQLQueries.CREATE_DATABASE)
        # get today's work
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        work_completed_today = db.fetch_data(SQLQueries.GET_TODAYS_WORK, (today, ))
        if work_completed_today:
            AppState.activity_done = work_completed_today[0][0]
        else:
            AppState.activity_done = 0
        self._update_activity_bar()
        db.disconnect()

    def _start_timer(self):
        if not AppState.timer_is_running:
            AppState.timer_is_running = True
            AppState.timer_thread = None
            AppState.animation_thread = None
            AppState.speed_thread = None
            AppState.timer_thread = Thread(target=self._start_count_down)
            AppState.animation_thread = Thread(target=self._start_info_animation)
            AppState.speed_thread = Thread(target=self._start_speed_animation)
            AppState.timer_thread.start()
            AppState.animation_thread.start()
            AppState.speed_thread.start()

    def _start_count_down(self):
        try:
            h = int(self.text_hour.get())
            m = int(self.text_minute.get())
            s = int(self.text_second.get())
        except ValueError:
            self._reset_timer()
            return
        total_seconds = h * 3600 + m * 60 + s
        if total_seconds == 0:
            self._reset_timer()
            return
        while total_seconds > 0 and AppState.timer_is_running:
            timer = datetime.timedelta(seconds=total_seconds)
            time.sleep(1)
            # reduce total time by one second
            total_seconds -= 1
            remaining_time = datetime.timedelta(seconds=total_seconds)
            if AppState.timer_is_running:
                self._update_timer(remaining_time)
                AppState.activity_done += 1
                self._update_activity_bar()
        self._reset_timer()
        self._update_todays_work(AppState.activity_done)
        if total_seconds < 1:
            # if finished completely (without reset), show break screen
            self._finish_work_screen

    def _update_timer(self, remaining_time):
        self.text_hour.delete(0, tk.END)
        self.text_minute.delete(0, tk.END)
        self.text_second.delete(0, tk.END)
        self.text_hour.insert(0, str(remaining_time).split(":")[0])
        self.text_minute.insert(0, str(remaining_time).split(":")[1])
        self.text_second.insert(0, str(remaining_time).split(":")[2])

    def _update_activity_bar(self):
        result = (AppState.activity_done / AppConstants.WORKING_TIME_LIMIT_IN_SECONDS) * 100
        self.progressbar_activity["value"] = result
        if 50 < result <= 90:
            self.progressbar_activity["style"] = "blue.Horizontal.TProgressbar"
        elif result > 90:
            self.progressbar_activity["style"] = "red.Horizontal.TProgressbar"
        else:
            self.progressbar_activity["style"] = "green.Horizontal.TProgressbar"
        # update percentage label
        self.label_percentage.configure(text=str(round(self.progressbar_activity["value"], 1)) + "%")

    def _finish_work_screen(self):
        termination_window = TerminationWindow()
        termination_window.display()

    def _start_info_animation(self):
        chars = ["--", "\\", "|", "/"]
        i = 0
        while AppState.timer_is_running:
            self.label_info.configure(text='Working... ' + chars[i])
            time.sleep(0.1)
            i += 1
            if i == 4:
                i = 0
        self.label_info.configure(text='Ready.')

    def _start_speed_animation(self):
        last_mouse_pos = Mouse.get_mouse_pos()
        last_time = time.time()
        self.progressbar_speed.start()
        while AppState.timer_is_running:
            time.sleep(0.1)
            current_mouse_pos = Mouse.get_mouse_pos()
            current_time = time.time()
            speed = Mouse.calculate_speed(last_mouse_pos, current_mouse_pos, last_time, current_time)
            normalized_speed = Mouse.normalize_speed(speed, 0, 8000, 0, 100)
            self.progressbar_speed["value"] = normalized_speed
            if 50 < normalized_speed <= 90:
                self.progressbar_speed["style"] = "blue.Horizontal.TProgressbar"
            elif normalized_speed > 90:
                self.progressbar_speed["style"] = "red.Horizontal.TProgressbar"
            else:
                self.progressbar_speed["style"] = "green.Horizontal.TProgressbar"
            last_mouse_pos = current_mouse_pos
            last_time = current_time
        self.progressbar_speed.stop()

    def _reset_timer(self):
        AppState.timer_is_running = False
        self.text_hour.delete(0, tk.END)
        self.text_hour.insert(0, "0")
        self.text_minute.delete(0, tk.END)
        self.text_minute.insert(0, "0")
        self.text_second.delete(0, tk.END)
        self.text_second.insert(0, "0")
        self.label_info.configure(text='Ready.')
        if AppState.timer_thread:
            AppState.timer_thread = None
        if AppState.animation_thread:
            AppState.animation_thread = None
        if AppState.speed_thread:
            AppState.speed_thread = None

    def _toggle_always_on_top(self):
        if self.checkbox_ontop_value.get() == 1:
            self.window.attributes("-topmost", True)
        else:
            self.window.attributes("-topmost", False)

    def _close_app(self, e):
        if AppState.timer_is_running:
            self._reset_timer()
            self._update_todays_work(AppState.activity_done)
        if AppState.graph_is_open:
            self.grap_window.close(e)
        if AppState.list_is_open:
            self.list_window.close(e)
        self.window.destroy()

    def _update_todays_work(self, work_completed):
        db = cast(DBConnector, self._db)
        db.connect()
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        result = db.fetch_data(SQLQueries.GET_WORK_BY_DATE, (today, ))
        if result:
            db.execute_query(SQLQueries.UPDATE_WORK_BY_DATE, (work_completed, today))
        else:
            db.execute_query(SQLQueries.ADD_WORK_BY_DATE, (today, work_completed))
        db.disconnect()

    def _show_graph(self, e):
        if not AppState.graph_is_open:
            self.graph_window = GraphWindow(self.window, self._db)
            self.graph_window.display()
        else:
            self.graph_window.close(e)

    def _show_list(self, e):
        if not AppState.list_is_open:
            self.list_window = ListWindow(self.window)
            self.list_window.display()
        else:
            self.list_window.close(e)

    def display(self):
        self.window.mainloop()


