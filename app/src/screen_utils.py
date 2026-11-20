from src.classes import Screen


current_screen: Screen = Screen()

def update_screen(current_resolution_dict, resolution=""):
    global current_screen
    current_screen = Screen(current_resolution_dict, resolution=resolution)
    
def get_screen() -> Screen:
    global current_screen
    return current_screen