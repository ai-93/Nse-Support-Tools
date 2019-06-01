# Nse-Support-Tools
This is an alternative to [nsetools python library](https://pypi.org/project/nsetools/) to fetch realtime data from [www.nseindia.com](www.nseindia.com).

Version: 0.1

# Feature List
List of supported features
```
- Get single stock quote
- Get all stock quote for all symbols
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

# TODO
```
- Fetch sectoral and industry data for stocks
- Cleanup payload for each function
- Add documentation
- Create pip installable library
...
```

# Usage
Example: Get all stock quotes
```
    from NseSupport import Nse

    nse = Nse()

    nse.get_all_stock_quotes()

    print(nse.quote_list)
```