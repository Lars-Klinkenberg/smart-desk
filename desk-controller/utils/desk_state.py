# app/utils/state.py


class DeskState:
    def __init__(self):
        self.height = 0  # Initial height of the desk
        self.is_moving = False
        self.latest_measurements = []  # a list of the latest measurements
        self.moveDeskTo = "DEFAULT"

    def get_height(self):
        return self.height

    def set_height(self, height):
        # save last measurements
        if self.height != 0:
            self.latest_measurements.append(self.height)

        self.height = height

    def start_moving(self):
        self.is_moving = True

    def stop_moving(self):
        self.is_moving = False
        self.reset_moving_direction()

    def currently_moving(self):
        return self.is_moving

    def should_desk_be_moved(self):
        return (self.moveDeskTo == "UP") or (self.moveDeskTo == "DOWN")
    
    def get_moving_direction(self):
        return self.moveDeskTo

    def set_moving_direction(self, direction):
        if (direction != "UP") or (direction != "DOWN"):
            return

        self.moveDeskTo = direction
        
    def reset_moving_direction(self):
        self.moveDeskTo = "DEFAULT"

# Create a global instance of the desk state
desk_state = DeskState()
