import requests, json, threading, queue
from bs4 import BeautifulSoup
from datetime import datetime
import csv

class Nse:
    def __init__(self):
        self.nse_get_quote_url = "https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol="
        self.nse_get_euity_list_url = "http://www.nseindia.com/content/equities/EQUITY_L.csv"
        self.nse_nifty_gainers_url = "http://www.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json"
        self.nse_nifty_losers_url = "http://www.nseindia.com/live_market/dynaContent/live_analysis/losers/niftyLosers1.json"
        self.nse_top_fno_gainers_url = "https://www.nseindia.com/live_market/dynaContent/live_analysis/gainers/fnoGainers1.json"
        self.nse_top_fno_loser_url = "https://www.nseindia.com/live_market/dynaContent/live_analysis/losers/fnoLosers1.json"
        self.nse_advance_decline_url = "http://www.nseindia.com/common/json/indicesAdvanceDeclines.json"
        self.nse_indices_list_url = "http://www.nseindia.com/homepage/Indices1.json"
        self.nse_most_active_monthly_url = "https://www.nseindia.com/products/dynaContent/equities/equities/json/mostActiveMonthly.json"
        self.nse_year_high_url = "https://www.nseindia.com/products/dynaContent/equities/equities/json/online52NewHigh.json"
        self.nse_year_low_url = "https://www.nseindia.com/products/dynaContent/equities/equities/json/online52NewLow.json"
        self.nse_nifty_preopen_url = "https://www.nseindia.com/live_market/dynaContent/live_analysis/pre_open/nifty.json"
        self.nse_fno_preopen_url = "https://www.nseindia.com/live_market/dynaContent/live_analysis/pre_open/fo.json"
        self.nse_bank_nifty_preopen_url = "https://www.nseindia.com/content/fo/fo_mktlots.csv"

        self.symbol = None
        self.response = None
        self.stock_quote = None
        self.nse_equity_list = None
        self.nifty_gainers = None
        self.nifty_losers = None
        self.top_fno_gainers = None
        self.top_fno_losers = None
        self.advance_decline_ratio = None
        self.indices_list = None
        self.most_active_monthly = None
        self.year_high = None
        self.year_low = None
        self.nifty_preopen = None
        self.fno_preopen = None
        self.bank_nifty_preopen = None
        self.response_time = None

        self.symbol_list = []

        self.queue = queue.Queue()
        self.threads = list()

        self.quote_list = []
    
    def chunk_list(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i+n]

    def get_stock_quote(self):
        self.response = requests.get(self.nse_get_quote_url+self.symbol)
        self.response_time = self.response.elapsed.total_seconds()

        if self.response.status_code == 200:
            soup = BeautifulSoup(self.response.content, 'html.parser')
            self.stock_quote = json.loads(soup.html.find("div", id="responseDiv").string)

        return self.stock_quote
    
    def get_equity_list(self):
        self.response = requests.get(self.nse_get_euity_list_url)
        self.response_time = self.response.elapsed.total_seconds()

        if self.response.status_code == 200:
            llist = []
            flist = []

            for item in self.response.content.splitlines():
                item = item.decode('utf-8', 'ignore')
                llist.append(item)

            for row in csv.DictReader(llist,["SYMBOL", "NAME OF COMPANY", " SERIES", " DATE OF LISTING", " PAID UP VALUE", " MARKET LOT", " ISIN NUMBER", " FACE VALUE"]):
                flist.append(dict(row))
            
            self.nse_equity_list = flist[1:]

        return self.nse_equity_list

    def get_nifty_gainers(self):
        self.response = requests.get(self.nse_nifty_gainers_url)
        self.response_time = self.response.elapsed.total_seconds()

        if self.response.status_code == 200:
            self.nifty_gainers = json.loads(self.response.content)

        return self.nifty_gainers

    def get_nifty_losers(self):
        self.response = requests.get(self.nse_nifty_losers_url)
        self.response_time = self.response.elapsed.total_seconds()

        if self.response.status_code == 200:
            self.nifty_losers = json.loads(self.response.content)

        return self.nifty_losers

    def get_top_fno_gainers(self):
        self.response = requests.get(self.nse_top_fno_gainers_url)
        self.response_time = self.response.elapsed.total_seconds()

        if self.response.status_code == 200:
            self.top_fno_gainers = json.loads(self.response.content)

        return self.top_fno_gainers

    def get_top_fno_losers(self):
        self.response = requests.get(self.nse_top_fno_loser_url)
        self.response_time = self.response.elapsed.total_seconds()

        if self.response.status_code == 200:
            self.top_fno_losers = json.loads(self.response.content)

        return self.top_fno_losers

    def get_advance_decline_ratio(self):
        self.response = requests.get(self.nse_advance_decline_url)
        self.response_time = self.response.elapsed.total_seconds()

        if self.response.status_code == 200:
            self.advance_decline_ratio = json.loads(self.response.content)

        return self.advance_decline_ratio

    def get_indices_list(self):
        self.response = requests.get(self.nse_indices_list_url)
        self.response_time = self.response.elapsed.total_seconds()

        if self.response.status_code == 200:
            self.indices_list = json.loads(self.response.content)

        return self.indices_list

    def get_most_active_monthly(self):
        self.response = requests.get(self.nse_most_active_monthly_url)
        self.response_time = self.response.elapsed.total_seconds()

        if self.response.status_code == 200:
            self.most_active_monthly = json.loads(self.response.content)

        return self.most_active_monthly

    def get_year_high(self):
        self.response = requests.get(self.nse_year_high_url)
        self.response_time = self.response.elapsed.total_seconds()

        if self.response.status_code == 200:
            self.year_high = json.loads(self.response.content)

        return self.year_high

    def get_year_low(self):
        self.response = requests.get(self.nse_year_low_url)
        self.response_time = self.response.elapsed.total_seconds()

        if self.response.status_code == 200:
            self.year_low = json.loads(self.response.content)

        return self.year_low

    def get_nifty_preopen(self):
        self.response = requests.get(self.nse_nifty_preopen_url)
        self.response_time = self.response.elapsed.total_seconds()

        if self.response.status_code == 200:
            self.nifty_preopen = json.loads(self.response.content)

        return self.nifty_preopen

    def get_fno_preopen(self):
        self.response = requests.get(self.nse_fno_preopen_url)
        self.response_time = self.response.elapsed.total_seconds()

        if self.response.status_code == 200:
            self.fno_preopen = json.loads(self.response.content)

        return self.fno_preopen

    def get_bank_nifty_preopen(self):
        self.response = requests.get(self.nse_bank_nifty_preopen_url)
        self.response_time = self.response.elapsed.total_seconds()

        if self.response.status_code == 200:
            self.bank_nifty_preopen = json.loads(self.response.content)

        return self.bank_nifty_preopen
    
    def get_symbol_list(self):
        self.get_equity_list()

        for item in self.nse_equity_list:
            self.symbol_list.append(item['SYMBOL'])
        
        self.symbol_list = list(set(self.symbol_list))

        return self.symbol_list
    
    def get_stock_quote_threaded(self, symbol_list,  queue):
        quote_list = []
        for item in symbol_list:
            try:
                self.response = requests.get(self.nse_get_quote_url+item)
                self.response_time = self.response.elapsed.total_seconds()

                stock_quote = [
                        {
                            item: self.response.status_code
                        }
                    ]

                if self.response.status_code == 200:
                    soup = BeautifulSoup(self.response.content, 'html.parser')
                    stock_quote = json.loads(soup.html.find("div", id="responseDiv").string)
                quote_list.append(stock_quote)
            except:
                quote_list.append([item])
        queue.put(quote_list)
    
    def get_all_stock_quotes(self):
        start = datetime.now()

        self.get_symbol_list()

        number_of_threads = 5

        chunk_list = list(self.chunk_list(self.symbol_list, number_of_threads))

        for item in chunk_list:
            th = threading.Thread(
                target = self.get_stock_quote_threaded, args = (item, self.queue)
            )
            self.threads.append(th)
            th.start()

        for index, thread in enumerate(self.threads):
            thread.join()
            q_list = self.queue.get()
            self.quote_list = self.quote_list + q_list

        end = datetime.now()
        print("Ex time: {}".format(end - start))







