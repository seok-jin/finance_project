from stock_ticker.stock_base import Get_stock_ticker


class Main():
    def __init__(self):
        # STEP 01. 기초 정보 수집 및 가공
        Get_stock_ticker()


if __name__ == '__main__':
    Main()
