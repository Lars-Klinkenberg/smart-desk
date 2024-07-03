from flask_classful import FlaskView, route


class HeightController(FlaskView):
    def __init__(self, args):
        self.gpio = args.get("gpio_service")
        self.desk = args.get("desk")

    @route("move/<direction>")
    def move_desk(self, direction):
        self.gpio.enable_write_to_serial()
        self.desk.move_desk(direction)
        self.gpio.disable_write_to_serial()
        return "", 200

    @route("height")
    def get_current_height(self):
        self.gpio.enable_write_to_serial()
        height = self.desk.getCurrentHeight()
        self.gpio.disable_write_to_serial()

        if height <= 0:
            return "0", 500

        return str(height), 200
