# app/utils/state.py


class DeskState:
    def __init__(self):
        self.height = 0  # Initial height of the desk
        self.is_moving = False

    def get_height(self):
        return self.height

    def set_height(self, height):
        self.height = height

    def start_moving(self):
        self.is_moving = True

    def stop_moving(self):
        self.is_moving = False


# Create a global instance of the desk state
desk_state = DeskState()
