from view import App
from model import SeasonalTrendModel

class SeasonalTrendController:
    def __init__(self):
        self.view = App()
        self.model = SeasonalTrendModel()

    def run(self):
        self.view.run()

