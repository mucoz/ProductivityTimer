import tkinter as tk
from app_constants import AppConstants

class TerminationWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.bind('<Escape>', self._close_window)
        self._create_ui_elements()

    def _close_window(self):
        self.window.destroy()

    def _create_ui_elements(self):
        self.window.config(bg=AppConstants.COLOR_BLACK)
        self.window.attributes("-fullscreen", True)
        self.window.attributes("-topmost", True)

        main_frame = tk.Frame(self.window, bg=AppConstants.COLOR_BLACK)
        main_frame.pack(pady=self.window.winfo_screenheight() / 4)
        label_message = tk.Label(main_frame, text="Work Completed. \n\nPress 'ESC' to continue...",
                                             font=AppConstants.LARGE_FONT,
                                             bg=AppConstants.COLOR_BLACK,
                                             fg=AppConstants.COLOR_ORANGE)
        label_message.grid(row=0, column=0)
        self.window.focus_set()

    def display(self):
        self.window.mainloop()
