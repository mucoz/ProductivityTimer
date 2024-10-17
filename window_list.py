import tkinter as tk
from app_state import AppState
from app_constants import AppConstants
from file_compressor import HuffmanCompression
import os
from magnetic_window import MagneticWindow


class ListWindow:
    def __init__(self, parent_window):
        self.window = MagneticWindow(width=AppConstants.LIST_WINDOW_WIDTH, height=AppConstants.LIST_WINDOW_HEIGHT,
                                     bgColor=AppConstants.COLOR_BLACK, x=parent_window.winfo_x(),
                                     y=parent_window.winfo_y(), y_offset=AppConstants.COUNTDOWN_WINDOW_HEIGHT,
                                     magnetic_threshold=AppConstants.WINDOW_SNAP_THREASHOLD)
        AppState.list_is_open = True
        self.parent_window = parent_window
        self.window.title("List Window")
        self._create_ui_elements()

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
