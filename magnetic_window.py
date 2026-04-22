import tkinter as tk
from typing import Optional, Tuple, Dict
from controller_screen import Screen


class MagneticWindow(tk.Tk):
    def __init__(
        self,
        width: int,
        height: int,
        bgColor: str,
        x: Optional[int] = None,
        y: Optional[int] = None,
        x_offset: int = 0,
        y_offset: int = 0,
        magnetic_threshold: int = 20,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        
        # Pencere özellikleri
        self.width = width
        self.height = height
        self.magnetic_threshold = magnetic_threshold
        
        # Tüm monitörlerin görev çubuğu bilgilerini al
        self.monitors_info = Screen.get_all_monitors_taskbar_info()
        
        # Monitör bilgilerini dictionary'de sakla (koordinatlara göre)
        self.monitor_bounds: Dict[str, Tuple[int, int, int, int, int]] = {}
        for monitor_x, monitor_y, monitor_w, monitor_h, taskbar_h in self.monitors_info:
            key = f"{monitor_x}_{monitor_y}_{monitor_w}_{monitor_h}"
            self.monitor_bounds[key] = (monitor_x, monitor_y, monitor_w, monitor_h, taskbar_h)
        
        # Pencere başlangıç pozisyonu
        if x is None:
            # İlk monitörün ortasına yerleştir
            first_monitor = self.monitors_info[0] if self.monitors_info else (0, 0, 1920, 1080, 40)
            x = first_monitor[0] + first_monitor[2] // 2 - width // 2
        if y is None:
            first_monitor = self.monitors_info[0] if self.monitors_info else (0, 0, 1920, 1080, 40)
            y = first_monitor[1] + first_monitor[3] // 2 - height // 2
        
        # Pencereyi oluştur
        self.geometry(f'{width}x{height}+{x + x_offset}+{y + y_offset}')
        self.resizable(False, False)
        self.minsize(width, height)
        self.attributes('-topmost', True)
        self.overrideredirect(True)
        self.configure(bg=bgColor)
        
        # Sürükleme için değişkenler
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.drag_start_window_x = 0
        self.drag_start_window_y = 0
        self.is_dragging = False
        
        # Mouse event bindings
        self.bind('<ButtonPress-1>', self._on_mouse_down)
        self.bind('<ButtonRelease-1>', self._on_mouse_up)
        self.bind('<B1-Motion>', self._on_mouse_drag)
    
    def _get_monitor_at_position(self, x: int, y: int) -> Optional[Tuple[int, int, int, int, int]]:
        """Verilen koordinattaki monitörün bilgilerini döndürür"""
        for monitor_x, monitor_y, monitor_w, monitor_h, taskbar_h in self.monitors_info:
            if (monitor_x <= x < monitor_x + monitor_w and
                monitor_y <= y < monitor_y + monitor_h):
                return (monitor_x, monitor_y, monitor_w, monitor_h, taskbar_h)
        return None
    
    def _get_usable_bounds(self, monitor_info: Tuple[int, int, int, int, int]) -> Tuple[int, int, int, int]:
        """
        Monitörün kullanılabilir alanını döndürür (görev çubuğu hariç)
        monitor_info: (x, y, width, height, taskbar_height)
        """
        monitor_x, monitor_y, monitor_width, monitor_height, taskbar_height = monitor_info
        
        # Varsayılan olarak tüm monitör alanı
        usable_x = monitor_x
        usable_y = monitor_y
        usable_width = monitor_width
        usable_height = monitor_height
        
        # Görev çubuğu varsa, onu çıkar (genellikle alt taraftadır)
        if taskbar_height > 0:
            usable_height = monitor_height - taskbar_height
            # Not: Görev çubuğu bazı sistemlerde farklı kenarlarda olabilir
            # Bu basit yaklaşım görev çubuğunun altta olduğunu varsayar
        
        return (usable_x, usable_y, usable_width, usable_height)
    
    def _on_mouse_down(self, event):
        """Mouse butonuna basıldığında"""
        self.is_dragging = True
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root
        self.drag_start_window_x = self.winfo_x()
        self.drag_start_window_y = self.winfo_y()
    
    def _on_mouse_up(self, event):
        """Mouse butonu bırakıldığında"""
        self.is_dragging = False
    
    def _on_mouse_drag(self, event):
        """Mouse sürüklendiğinde"""
        if not self.is_dragging:
            return
        
        # Yeni pencere pozisyonu
        new_x = self.drag_start_window_x + (event.x_root - self.drag_start_x)
        new_y = self.drag_start_window_y + (event.y_root - self.drag_start_y)
        
        # Pencerenin bulunduğu monitörü bul (pencere merkezine göre)
        window_center_x = new_x + self.width // 2
        window_center_y = new_y + self.height // 2
        current_monitor = self._get_monitor_at_position(window_center_x, window_center_y)
        
        if current_monitor is None:
            # Monitör bulunamazsa ilk monitörü kullan
            current_monitor = self.monitors_info[0] if self.monitors_info else (0, 0, 1920, 1080, 40)
        
        # Kullanılabilir alanı al
        usable_x, usable_y, usable_width, usable_height = self._get_usable_bounds(current_monitor)
        
        # Kenar yapışma mantığı
        # Sol kenar
        if abs(new_x - usable_x) < self.magnetic_threshold:
            new_x = usable_x
        
        # Sağ kenar
        right_boundary = usable_x + usable_width
        if abs((new_x + self.width) - right_boundary) < self.magnetic_threshold:
            new_x = right_boundary - self.width
        
        # Üst kenar
        if abs(new_y - usable_y) < self.magnetic_threshold:
            new_y = usable_y
        
        # Alt kenar
        bottom_boundary = usable_y + usable_height
        if abs((new_y + self.height) - bottom_boundary) < self.magnetic_threshold:
            new_y = bottom_boundary - self.height
        
        # Pencereyi yeni pozisyona taşı
        self.geometry(f'+{new_x}+{new_y}')
    
