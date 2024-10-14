

class AppState:
    window_expanded = False
    graph_is_open=  False
    list_is_open = False
    timer_is_running = False
    timer_thread = None
    animation_thread = None
    speed_thread = None
    drag_start_x = None
    drag_start_y = None
    activity_done = 0 # in seconds
    all_work = None
    list_items = None
    snapped_left = False
    snapped_right = False
    snapped_up = False
    snapped_down = False
    snapped_top_left = False
    snapped_top_right = False
    snapped_bottom_right = False
    snapped_bottom_left = False
    cursor_in_corner = False
    taskbar_height = 0
