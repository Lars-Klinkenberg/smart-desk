from utils.desk_state import desk_state
from controllers.desk_hardware_controller import desk_hardware_controller
from utils.converter_service import converter_service
from utils.serial_service import serial_service
from utils.gpio_service import gpio_service


class DeskController:
    """
    Controller class for the desk
    """

    def desk_status(self, height) -> str:
        """
        returns the current status of the desk

        Returns:
            str: UP or DOWN or UNDEFINED
        """

        if height <= 0:
            return "UNDEFINED"

        if height == desk_hardware_controller.SITTING_HEIGHT:
            return "DOWN"

        if height == desk_hardware_controller.STANDING_HEIGHT:
            return "UP"

        return "UNDEFINED"

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

    def move(self, direction):
        print("MOVING TO:", direction)
        gpio_service.enable_write_to_serial()
        desk_state.start_moving()
        desk_hardware_controller.send_move_signal(direction)
        desk_hardware_controller.write_default_till_max_reached(direction)
        gpio_service.disable_write_to_serial()
        desk_state.stop_moving()


desk_controller = DeskController()
