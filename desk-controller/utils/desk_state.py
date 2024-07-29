# app/utils/state.py


class DeskState:
    def __init__(self):
        self.height = 0  # Initial height of the desk
        self.last_final_height = 0
        self.is_moving = False
        self.latest_measurements = []  # a list of the latest measurements
        self.moveDeskTo = "DEFAULT"

    def get_height(self):
        return self.height

    def set_height(self, height):
        # save last measurements
        if height <= 0:
            return

        # TODO : replace with get current height
        # after init last height is 0
        if self.last_final_height == 0:
            self.last_final_height = height

        self.height = height
        self.latest_measurements.append(height)

        if len(self.latest_measurements) > 10:
            self.latest_measurements.pop(0)

    def start_moving(self):
        self.reset_moving_direction()
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
        self.moveDeskTo = direction

    def reset_moving_direction(self):
        self.moveDeskTo = "DEFAULT"

    def handle_moving_request(self, direction):
        if (direction != "UP") and (direction != "DOWN"):
            return False

        self.set_moving_direction(direction)
        return True

    def get_latest_measurements(self):
        return self.latest_measurements

    def clear_latest_measurements(self):
        self.last_final_height = self.latest_measurements.pop()
        self.latest_measurements = []

    def get_last_final_height(self):
        return self.last_final_height


# Create a global instance of the desk state
desk_state = DeskState()
