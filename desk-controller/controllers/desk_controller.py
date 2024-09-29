from utils.desk_state import desk_state
from utils.converter_service import converter_service
from utils.serial_service import serial_service

class DeskController:
    """
    Controller class for the desk
    """

    # returns measured height
    def measure_desk_height(self, timeout=None):
        # read current height data and iterate over chunks
        height_temp = serial_service.read(timeout)
        height_splitted = converter_service.split_in_valid_chunks(height_temp)
        all_heights = []

        for t in height_splitted:
            height = converter_service.convert_hex_arr_to_height(t)

            # only count valid heights
            if height <= 0:
                continue

            all_heights.append(converter_service.convert_hex_arr_to_height(t))

        if len(all_heights) <= 0:
            return

        height = round(sum(all_heights) / len(all_heights))
        desk_state.set_height(height)
        return height

    def height_has_changed(self):
        measurements = desk_state.get_latest_measurements()
        if(len(measurements) <= 5):
            return False

        if desk_state.get_last_final_height() == measurements[len(measurements) -1]:
            return False
        
        # check if every item in the list is equal
        return all(x == measurements[0] for x in measurements)

    def reset_height_has_changed(self):
        desk_state.clear_latest_measurements()

desk_controller = DeskController()
