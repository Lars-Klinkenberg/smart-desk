class ConverterService:
    MAX_HEIGHT = 130

    # converts serial string to hex value array
    def serial_to_hex(self, data):
        return data.hex("-").split("-")

    # splits serial Data into a list of valid hex chunks
    def split_in_valid_chunks(self, serial_data):
        splitted_data = self.serial_to_hex(serial_data)
        chunked_data = []
        temp_arr = []

        # iterate through serialData
        for hex_value in splitted_data:
            # check for start bits
            if hex_value == "5a":
                # only append if temp arr not empty (e.g. in first iteration)
                if len(temp_arr) > 0:
                    chunked_data.append(temp_arr)
                temp_arr = []

            temp_arr.append(hex_value)

        #  save last tempArr if not empty
        if len(temp_arr) > 0:
            chunked_data.append(temp_arr)

        return chunked_data

    #
    def convert_hex_arr_to_number(self, hex_arr):
        if len(hex_arr) < 5:
            return -1

        if hex_arr[0] != "5a":
            return -1

        if (hex_arr[1] == "00") & (hex_arr[2] == "00") & (hex_arr[3] == "00"):
            return -1

        data0 = self.hex_to_number(hex_arr[1])
        data1 = self.hex_to_number(hex_arr[2])
        data2 = self.hex_to_number(hex_arr[3])

        if data0 == -1:
            return -1
        if data1 == -1:
            return -1
        if data2 == -1:
            return -1

        got_height = data0 * 100 + data1 * 10 + data2

        if got_height > self.MAX_HEIGHT:
            got_height = got_height / 10

        return got_height

    # turns an hex value into a number (0-9)
    def hex_to_number(self, segment):
        # 8 bit to 7 Segment so first bit can be 0 or 1
        SEGMENT_DICT = {
            "3f": 0,
            "bf": 0,
            "06": 1,
            "86": 1,
            "5b": 2,
            "db": 2,
            "4f": 3,
            "cf": 3,
            "66": 4,
            "e6": 4,
            "6d": 5,
            "ed": 5,
            "7d": 6,
            "fd": 6,
            "07": 7,
            "87": 7,
            "7f": 8,
            "ff": 8,
            "6f": 9,
            "ef": 9,
        }
        try:
            return SEGMENT_DICT[segment]
        except:
            return -1

converter_service = ConverterService()