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