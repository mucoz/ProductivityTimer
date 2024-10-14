import ctypes


class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long)]


class Screen:
    @staticmethod
    def get_taskbar_height():
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        work_area = RECT()
        SPI_GETWORKAREA = 0x0030
        ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(work_area), 0)
        taskbar_height = screen_height - work_area.bottom
        return taskbar_height
