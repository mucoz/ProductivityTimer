import tkinter as tk
from app_constants import AppConstants
import screeninfo


class TerminationWindow:
    def __init__(self, master_window=None, fullscreen_on_active_monitor_only=False):
        """
        master_window: Termination penceresini açan ana pencere (MagneticWindow)
        fullscreen_on_active_monitor_only: True ise sadece aktif monitörde tam ekran yapar
        """
        self.master_window = master_window
        self.fullscreen_on_active_monitor_only = fullscreen_on_active_monitor_only
        self.window = None
        self.is_open = False
        
        if master_window:
            self._create_window()
    
    def _create_window(self):
        """Pencereyi oluştur"""
        if self.is_open:
            return
            
        self.is_open = True
        
        if self.master_window and self.master_window.winfo_exists():
            self.master_window.attributes('-topmost', False)
        
        if self.master_window and self.master_window.winfo_exists():
            self.window = tk.Toplevel(self.master_window)
        else:
            self.window = tk.Tk()
        
        self.window.bind('<Escape>', self._close_window)
        self.window.protocol("WM_DELETE_WINDOW", self._close_window)
        self._create_ui_elements()
    
    def _set_fullscreen(self):
        """Tam ekran ayarlarını yapar"""
        if self.fullscreen_on_active_monitor_only:
            # Sadece aktif monitörde tam ekran
            active_monitor = self._get_active_monitor()
            if active_monitor:
                self.window.geometry(f"{active_monitor.width}x{active_monitor.height}+{active_monitor.x}+{active_monitor.y}")
                self.window.overrideredirect(True)  # Captionless
            else:
                self.window.attributes("-fullscreen", True)
                self.window.overrideredirect(True)
        else:
            # Tüm ekranlarda tam ekran (eski davranış)
            self.window.attributes("-fullscreen", True)
            self.window.overrideredirect(True)
    
    def _get_active_monitor(self):
        """Ana pencerenin bulunduğu monitörü döndür"""
        if not self.master_window or not self.master_window.winfo_exists():
            return None
        
        try:
            win_x = self.master_window.winfo_x()
            win_y = self.master_window.winfo_y()
            win_center_x = win_x + self.master_window.winfo_width() // 2
            win_center_y = win_y + self.master_window.winfo_height() // 2
            
            monitors = screeninfo.get_monitors()
            for monitor in monitors:
                if (monitor.x <= win_center_x < monitor.x + monitor.width and
                    monitor.y <= win_center_y < monitor.y + monitor.height):
                    return monitor
        except Exception as e:
            print(f"Monitör bulma hatası: {e}")
        
        return None
    
    def _close_window(self, event=None):
        """Pencereyi kapat ve önceki pencereyi aktif et"""
        if not self.window:
            return
        
        self.window.destroy()
        self.window = None
        self.is_open = False
        
        if self.master_window and self.master_window.winfo_exists():
            try:
                self.master_window.lift()
                self.master_window.focus_force()
                self.master_window.attributes('-topmost', True)
                self.master_window.attributes('-topmost', False)
            except Exception as e:
                print(f"Pencere aktifleştirme hatası: {e}")
    
    def _create_ui_elements(self):
        """UI elemanlarını oluştur"""
        if not self.window:
            return
        
        # Tam ekran ayarlarını yap
        self._set_fullscreen()
        
        self.window.configure(bg=AppConstants.COLOR_BLACK)
        self.window.attributes("-topmost", True)
        
        self.window.grab_set()
        self.window.focus_set()
        
        main_frame = tk.Frame(self.window, bg=AppConstants.COLOR_BLACK)
        main_frame.place(relx=0.5, rely=0.4, anchor="center")
        
        check_label = tk.Label(
            main_frame,
            text="✓",
            font=("Arial", 80, "bold"),
            bg=AppConstants.COLOR_BLACK,
            fg=AppConstants.COLOR_ORANGE
        )
        check_label.pack(pady=(0, 20))
        
        label_message = tk.Label(
            main_frame, 
            text="Work Completed!\n\nPress 'ESC' to continue...",
            font=AppConstants.LARGE_FONT,
            bg=AppConstants.COLOR_BLACK,
            fg=AppConstants.COLOR_ORANGE,
            justify="center"
        )
        label_message.pack()
        
        esc_label = tk.Label(
            main_frame,
            text="[ ESC ]",
            font=("Arial", 14),
            bg=AppConstants.COLOR_BLACK,
            fg="gray"
        )
        esc_label.pack(pady=(30, 0))
        
        self.window.update_idletasks()
    
    def display(self):
        """Pencereyi göster"""
        if not self.window:
            self._create_window()
        
        if self.window:
            self.window.mainloop()
    
    def close(self):
        """Pencereyi dışarıdan kapatmak için"""
        if self.window and self.window.winfo_exists():
            self._close_window()