from controllers.db_controller import DatabaseController


class SettingController(DatabaseController):
    def saveNewProfile(self):
        pass
    
    def updateExistingProfile(self, profileId):
        pass

    def saveSettings(self, settings):
        if(self.profileExists()):
            self.updateExistingProfile()
        
        self.saveNewProfile()
        
    def profileExists(self, profileId):
        pass