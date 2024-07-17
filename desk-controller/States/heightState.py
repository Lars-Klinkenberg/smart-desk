from Services.deskService import DeskService


class HeightState:
    latestHeight = -1

    def __init__(self, deskService: DeskService) -> None:
        self.deskService = deskService

    def readHeight(self) -> None:
        height = self.deskService.getCurrentHeight()

        if height <= 0:
            return

        self.latestHeight = height

    def getCurrentHeight(self) -> float:
        if self.latestHeight >= 0:
            return self.latestHeight

        return 0
