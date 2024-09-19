# app/utils/state.py


class DeskState:
    def __init__(self):
        self.height = 0  # Initial height of the desk
        self.last_final_height = 0
        self.latest_measurements = []  # a list of the latest measurements

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

    def get_latest_measurements(self):
        return self.latest_measurements

    def clear_latest_measurements(self):
        if self.latest_measurements:
            self.last_final_height = self.latest_measurements.pop()
        else:
            self.last_final_height = self.height
        self.latest_measurements = []

    def get_last_final_height(self):
        return self.last_final_height


# Create a global instance of the desk state
desk_state = DeskState()
