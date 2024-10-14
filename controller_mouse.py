import win32api


class Mouse:
    @staticmethod
    def get_mouse_pos():
        x, y = win32api.GetCursorPos()
        return x, y

    @staticmethod
    def calculate_speed(last_pos, current_pos, last_time, current_time):
        distance = ((current_pos[0] - last_pos[0]) ** 2 + (current_pos[1] - last_pos[1]) ** 2) ** 0.5
        time_difference = current_time - last_time
        speed = distance / time_difference
        return speed

    @staticmethod
    def normalize_speed(speed, min_speed, max_speed, min_range, max_range):
        return ((speed - min_speed) / (max_speed - min_speed)) * (max_range - min_range) + min_range