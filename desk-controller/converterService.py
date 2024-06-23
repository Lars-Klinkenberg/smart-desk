class ConverterService:
    # converts serial string to hex value array
    def serialToHex(self, data):
        return data.hex("-").split("-")

    # splits serial Data into a list of valid hex chunks
    def splitInValidChunks(self, serialData):
        splittedData = self.serialToHex(serialData)
        
        chunkedData = []
        tempArr = []

        for hexValue in splittedData:
            if(hexValue == "5a"):
                if(len(tempArr) == 5):
                    chunkedData.append(tempArr)
                tempArr = []
                
            tempArr.append(hexValue)
            
        # TODO: save remaining values to buffer if not complete
            
        return chunkedData