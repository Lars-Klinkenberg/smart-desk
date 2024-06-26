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
            return 0

        if(hexArr[0] != "5a"):
            return 0
    
        if((hexArr[1] == "00") & (hexArr[2] == "00") &( hexArr[3] == "00")):
            return 0
        
        data0 = self.hex_to_number(hexArr[1])
        data1 = self.hex_to_number(hexArr[2])
        data2 = self.hex_to_number(hexArr[3])
        
        got_height = 0.0
    
        # get decimal
        decimal = ((int(hexArr[4], 16) + 256) % 256) / 10
        
        # data0 = hunderter | data1 = zehner | data2 = einser | decimal = komma
        # got_height = data0 * 100 + data1 * 10 + data2 + decimal * 0.1
        got_height = data0 * 100 + data1 * 10 + data2
        
        # TODO: calc sum for numbers under 100cm
        
        return got_height
    
    #turns an hex value into a number (0-9)
    def hex_to_number(self, segment):
    # Map values to numbers
        SEGMENT_MAP = ["3f", "06", "5b", "4f", "67", "6d", "7d", "07", "7f", "6f"]
        try:
            return SEGMENT_MAP.index(segment)
        except:
            return -1
        
    # returns false if avg of latestMeasurements is in tolerance to the last element in latestMeasurements
    def isHeightChanging(self, latestMeasurements, tolerance = 1):
        if(len(latestMeasurements) < 100):
            return True
        else:
            latestMeasurements.pop(0)
        
        last_height = latestMeasurements.pop()
        avg = sum(latestMeasurements) / len(latestMeasurements)
        
        if(avg < last_height):
            return last_height - tolerance >= avg
        
        if(avg > last_height):
            return last_height + tolerance <= avg
        
        if(avg == last_height):
            return False
        
        # return default
        return True