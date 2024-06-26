class ConverterService:
    # converts serial string to hex value array
    def serialToHex(self, data):
        return data.hex("-").split("-")

    # splits serial Data into a list of valid hex chunks
    def splitInValidChunks(self, serialData):
        splittedData = self.serialToHex(serialData)
        chunkedData = []
        tempArr = []

        # iterate through serialData
        for hexValue in splittedData:
            # check for start bits
            if(hexValue == "5a"):
                # only append if temp arr not empty (e.g. in first iteration)
                if(len(tempArr) > 0):
                    chunkedData.append(tempArr)
                tempArr = []
                
            tempArr.append(hexValue)
            
        
        #  save last tempArr if not empty
        if(len(tempArr) > 0):
            chunkedData.append(tempArr)
            
        return chunkedData
    
    # 
    def convertHexArrToNumber(self, hexArr):

        if(len(hexArr) < 5):
            return -1

        if(hexArr[0] != "5a"):
            return -1
    
        if((hexArr[1] == "00") & (hexArr[2] == "00") &( hexArr[3] == "00")):
            return -1
        
        data0 = self.hex_to_number(hexArr[1])
        data1 = self.hex_to_number(hexArr[2])
        data2 = self.hex_to_number(hexArr[3])
        
        if(data0 == -1):
            return -1
        if(data1 == -1):
            return -1
        if(data2 == -1):
            return -1
        
        
        got_height = 0.0
    
        # get decimal
        decimal = ((int(hexArr[4], 16) + 256) % 256) / 10
        
        # data0 = hunderter | data1 = zehner | data2 = einser | decimal = komma
        # got_height = data0 * 100 + data1 * 10 + data2 + decimal * 0.1
        got_height = data0 * 100 + data1 * 10 + data2
        
        # TODO: calc sum for numbers under 100cm
        maxHeight = 150
        if(got_height > maxHeight):
            got_height = got_height / 10

        return got_height
    
    #turns an hex value into a number (0-9)
    def hex_to_number(self, segment):
        # 8 bit to 7 Segment so first bit can be 0 or 1
        SEGMENT_DICT = {
            "3f" : 0,
            "bf" : 0,
            "06" : 1,
            "86" : 1,
            "5b" : 2,
            "db" : 2,
            "4f" : 3,
            "cf" : 3,
            "66" : 4,
            "e6" : 4,
            "6d" : 5,
            "ed" : 5,
            "7d" : 6,
            "fd" : 6,
            "07" : 7,
            "87" : 7,
            "7f" : 8,
            "ff" : 8,
            "6f" : 9,
            "ef" : 9
        }
        try:
            # return SEGMENT_MAP.index(segment)
            return SEGMENT_DICT[segment]
        except:
            return -1
        