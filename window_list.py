import tkinter as tk
from app_state import AppState
from app_constants import AppConstants
from file_compressor import HuffmanCompression
import os


class ListWindow:
    def __init__(self, parent_window):
        self.window = tk.Tk()
        AppState.list_is_open = True
        self.parent_window = parent_window
        self.window.title("List Window")
        self._adjust_window_position()
        self._make_window_draggable()
        self._create_ui_elements()

    def _adjust_window_position(self):
        parent_x = self.parent_window.winfo_x()
        parent_y = self.parent_window.winfo_y()
        self.window.geometry('{}x{}+{}+{}'.format(AppConstants.LIST_WINDOW_WIDTH,
                                                  AppConstants.LIST_WINDOW_HEIGHT,
                                                  parent_x, parent_y + AppConstants.COUNTDOWN_WINDOW_HEIGHT))

        self.window.resizable(False, False)
        self.window.minsize(AppConstants.LIST_WINDOW_WIDTH, AppConstants.LIST_WINDOW_HEIGHT)
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
        self.textbox_list = tk.Text(self.window, font=AppConstants.LIST_FONT,
                                    bg=AppConstants.COLOR_BLACK_MATTE,
                                    fg=AppConstants.COLOR_ORANGE,
                                    insertbackground=AppConstants.LIST_CURSOR_COLOR,
                                    height=AppConstants.LIST_HEIGHT,
                                    width=AppConstants.LIST_WIDTH)
        self.textbox_list.pack(padx=5, pady=5)
        if not os.path.exists(AppConstants.LIST_FILE_NAME):
            return
        else:
            data = HuffmanCompression.read_compressed_file(AppConstants.LIST_FILE_NAME)
            self.textbox_list.delete("1.0", tk.END)
            self.textbox_list.insert(tk.END, data)

    def display(self):
        self.window.mainloop()

    def close(self, event):
        self.save_list()
        AppState.list_is_open = False
        self.window.destroy()

    def save_list(self):
        data = self.textbox_list.get("1.0", "end-1c")
        if not data:
            data = " "
        HuffmanCompression.compress_data(data, AppConstants.LIST_FILE_NAME)
