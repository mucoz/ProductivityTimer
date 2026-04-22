import ctypes
from typing import List, Tuple, Optional
import screeninfo


class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long)]


class Screen:
    @staticmethod
    def get_taskbar_height(monitor_index: int = 0) -> int:
        """Belirtilen monitördeki görev çubuğu yüksekliğini döndürür"""
        try:
            user32 = ctypes.windll.user32
            # MONITORINFO yapısı
            class MONITORINFO(ctypes.Structure):
                _fields_ = [
                    ("cbSize", ctypes.c_uint),
                    ("rcMonitor", RECT),
                    ("rcWork", RECT),
                    ("dwFlags", ctypes.c_uint)
                ]
            
            # Tüm monitörleri al
            monitors = screeninfo.get_monitors()
            if monitor_index >= len(monitors):
                monitor_index = 0
            
            target_monitor = monitors[monitor_index]
            
            # Belirtilen monitörün çalışma alanını bul
            def monitor_enum_proc(hMonitor, hdcMonitor, lprcMonitor, dwData):
                monitor_info = MONITORINFO()
                monitor_info.cbSize = ctypes.sizeof(MONITORINFO)
                if user32.GetMonitorInfoW(hMonitor, ctypes.byref(monitor_info)):
                    # Monitörün konumunu kontrol et
                    if (monitor_info.rcMonitor.left == target_monitor.x and 
                        monitor_info.rcMonitor.top == target_monitor.y):
                        # Çalışma alanı yüksekliğini hesapla
                        monitor_height = monitor_info.rcMonitor.bottom - monitor_info.rcMonitor.top
                        work_height = monitor_info.rcWork.bottom - monitor_info.rcWork.top
                        taskbar_height = monitor_height - work_height
                        # Veriyi aktar
                        ctypes.cast(dwData, ctypes.POINTER(ctypes.c_int))[0] = taskbar_height
                        return False  # Bulduk, durdur
                return True  # Devam et
            
            taskbar_height = ctypes.c_int(0)
            enum_proc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p, 
                                          ctypes.POINTER(RECT), ctypes.c_void_p)
            user32.EnumDisplayMonitors(None, None, enum_proc(monitor_enum_proc), 
                                      ctypes.addressof(taskbar_height))
            
            if taskbar_height.value > 0:
                return taskbar_height.value
            
        except Exception:
            pass
        
        # Fallback: Ana monitörün görev çubuğu yüksekliğini hesapla
        try:
            user32 = ctypes.windll.user32
            screen_width = user32.GetSystemMetrics(0)
            screen_height = user32.GetSystemMetrics(1)
            work_area = RECT()
            SPI_GETWORKAREA = 0x0030
            ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(work_area), 0)
            taskbar_height = screen_height - work_area.bottom
            return taskbar_height if taskbar_height > 0 else 0
        except:
            return 40  # Varsayılan görev çubuğu yüksekliği
    
    @staticmethod
    def get_all_monitors_taskbar_info() -> List[Tuple[int, int, int, int, int]]:
        """
        Tüm monitörler için görev çubuğu bilgilerini döndürür
        Return: List of (monitor_x, monitor_y, monitor_width, monitor_height, taskbar_height)
        """
        monitors_info = []
        monitors = screeninfo.get_monitors()
        
        for i, monitor in enumerate(monitors):
            taskbar_height = Screen.get_taskbar_height(i)
            monitors_info.append((
                monitor.x, monitor.y, 
                monitor.width, monitor.height, 
                taskbar_height
            ))
        
        return monitors_info
    
    @staticmethod
    def get_monitor_at_position(x: int, y: int) -> Optional[Tuple[int, int, int, int, int]]:
        """Verilen koordinattaki monitörün bilgilerini döndürür"""
        monitors = screeninfo.get_monitors()
        for monitor in monitors:
            if (monitor.x <= x < monitor.x + monitor.width and
                monitor.y <= y < monitor.y + monitor.height):
                taskbar_height = Screen.get_taskbar_height(monitors.index(monitor))
                return (monitor.x, monitor.y, monitor.width, monitor.height, taskbar_height)
        return None