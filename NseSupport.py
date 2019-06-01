import requests
import json
import threading
import queue
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import SupportUrls


class Nse:
    def __init__(self):
        self.queue = queue.Queue()
        self.threads = list()
        self.number_of_threads = 5

        self.stock_quote = None
        self.nifty_gainers = None
        self.nifty_losers = None
        self.top_fno_gainers = None
        self.top_fno_losers = None
        self.advance_decline_ratio = None
        self.most_active_monthly = None
        self.year_high = None
        self.year_low = None
        self.nifty_preopen = None
        self.fno_preopen = None
        self.bank_nifty_preopen = None

        self.http_response = None
        self.http_json_response = None

        self.symbol = None
        self.symbol_list = []
        self.quote_list = []
        self.nse_equity_list = []
        self.indices_list = []

    def chunk_list(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i+n]

    def reset_threads(self):
        self.threads = list()
        self.queue = queue.Queue()
        self.quote_list = []

    def http_get_json(self, url):
        self.http_response = requests.get(url)

        if self.http_response.status_code == 200:
            self.http_json_response = json.loads(self.http_response.content)

        return self.http_json_response

    def get_stock_quote(self):
        self.http_response = requests.get(
            SupportUrls.nse_get_quote_url + self.symbol)

        if self.http_response.status_code == 200:
            soup = BeautifulSoup(self.http_response.content, 'html.parser')
            self.stock_quote = json.loads(
                soup.html.find("div", id="responseDiv").string)

        return self.stock_quote

    def get_equity_list(self):
        self.http_response = requests.get(SupportUrls.nse_get_euity_list_url)

        if self.http_response.status_code == 200:
            csv_rows = []
            for item in self.http_response.content.splitlines():
                item = item.decode('utf-8', 'ignore')
                csv_rows.append(item)

            for row in csv.DictReader(csv_rows, csv_rows[0].split(",")):
                self.nse_equity_list.append(dict(row))

        return self.nse_equity_list[1:]

    def get_nifty_gainers(self):
        self.nifty_gainers = self.http_get_json(
            SupportUrls.nse_nifty_gainers_url)
        return self.nifty_gainers

    def get_nifty_losers(self):
        self.nifty_losers = self.http_get_json(
            SupportUrls.nse_nifty_losers_url)
        return self.nifty_losers

    def get_top_fno_gainers(self):
        self.top_fno_gainers = self.http_get_json(
            SupportUrls.nse_top_fno_gainers_url)
        return self.top_fno_gainers

    def get_top_fno_losers(self):
        self.top_fno_losers = self.http_get_json(
            SupportUrls.nse_top_fno_loser_url)
        return self.top_fno_losers

    def get_advance_decline_ratio(self):
        self.advance_decline_ratio = self.http_get_json(
            SupportUrls.nse_advance_decline_url)
        return self.advance_decline_ratio

    def get_indices_list(self):
        self.indices_list = self.http_get_json(
            SupportUrls.nse_indices_list_url)
        return self.indices_list

    def get_most_active_monthly(self):
        self.most_active_monthly = self.http_get_json(
            SupportUrls.nse_most_active_monthly_url)
        return self.most_active_monthly

    def get_year_high(self):
        self.year_high = self.http_get_json(SupportUrls.nse_year_high_url)
        return self.year_high

    def get_year_low(self):
        self.year_low = self.http_get_json(SupportUrls.nse_year_low_url)
        return self.year_low

    def get_nifty_preopen(self):
        self.nifty_preopen = self.http_get_json(
            SupportUrls.nse_nifty_preopen_url)
        return self.nifty_preopen

    def get_fno_preopen(self):
        self.fno_preopen = self.http_get_json(SupportUrls.nse_fno_preopen_url)
        return self.fno_preopen

    def get_bank_nifty_preopen(self):
        self.bank_nifty_preopen = self.http_get_json(
            SupportUrls.nse_bank_nifty_preopen_url)
        return self.bank_nifty_preopen

    def get_symbol_list(self):
        self.get_equity_list()

        for item in self.nse_equity_list:
            self.symbol_list.append(item['SYMBOL'])

        self.symbol_list = list(set(self.symbol_list))

        return self.symbol_list

    def get_stock_quote_list(self, symbol_list,  queue):
        quote_list = []
        for item in symbol_list:
            try:
                self.symbol = item
                self.get_stock_quote()
                quote_list.append(self.stock_quote)
            except:
                quote_list.append([item])
        queue.put(quote_list)

    def get_bulk_stock_quotes(self, *args, **kwargs):
        start = datetime.now()
        symbol_list = None
        self.reset_threads()

        for ar in args:
            symbol_list = ar
        
        if symbol_list != None:
            self.symbol_list = symbol_list
        elif len(self.symbol_list) == 0:
            self.get_symbol_list()

        if len(self.symbol_list) < self.number_of_threads:
            self.number_of_threads = len(self.symbol_list)

        chunk_list = list(self.chunk_list(self.symbol_list, self.number_of_threads))

        for item in chunk_list:
            th = threading.Thread(
                target=self.get_stock_quote_list, args=(item, self.queue)
            )
            self.threads.append(th)
            th.start()

        for index, thread in enumerate(self.threads):
            thread.join()
            q_list = self.queue.get()
            self.quote_list = self.quote_list + q_list

        end = datetime.now()
        print("Execution time: {}".format(end - start))
        return self.quote_list
