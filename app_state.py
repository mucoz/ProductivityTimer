

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
