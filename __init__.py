from config.log_class import *
from stock_ticker.stock_base import *

class Main():
    def __init__(self):
        self.logging = Logging()
        self.logging.logger.debug("main class init")
        Get_stock_ticker()

if __name__ =='__main__':
    Main()