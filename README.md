# Nse-Support-Tools
This is an alternative to [nsetools python library](https://pypi.org/project/nsetools/) to fetch realtime data from [www.nseindia.com](www.nseindia.com).

Version: 0.1

# Feature List
List of supported features
```
- Get single stock quote
- Get all stock quote for all symbols or for only specified symbols
- Get equity instrument list
- Get nifty gainers
- Get nifty losers
- Get fno gainers
- Get fno losers
- Get advance decline ratio
- Get Indices list
- Get most active monthly
- Get year high
- Get year low
- Get nifty preopen
- Get fno preopen
- Get bank nifty preopen
```

# Dependencies
Install dependencies. Requires python3 and pip
```
    pip install requirements.txt
```

# Usage
Example: Get all stock quotes (all or only for specified list)

Due to the nature of this function, its execution time may run into a couple of minutes.
This is because stock quotes need to be fetched for each symbol individually as Nse does not currently provide consilidated stock quotes for all symbols.
```
    from NseSupport import Nse

    nse = Nse()

    nse.get_bulk_stock_quotes() // get stock quotes for all symbols
    print(nse.quote_list)

    symbol_list = ["TATAMOTORS", "INFY","VEDL","IOC","NTPC"]
    nse.get_bulk_stock_quotes(symbol_list) // get stock quotes for only specified symbols
    print(nse.quote_list)
```

Example: Get NIFTY gainers

Get list of all NIFTY  gainers
```
    from NseSupport import Nse

    nse = Nse()

    nse.get_nifty_gainers()

    print(nse.nifty_gainers)
```

# TODO
```
- Fetch sectoral and industry data for stocks
- Cleanup payload for each function
- Add documentation
- Create pip installable library
- Improve Error handeling
- Test Cases
...
```