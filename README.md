Centralized crpyto exchanes are valuable sources for obtaining trading data.
Data is needed for many purposes, one of them is backtesting of trading strategies.

There are plenty of scripts out there which does the job. 
Here is mine, which I tried to make as easy to understand as possible.



# Implementation details
##My generic folder structure:
- [x] config: Contains exchange access credentials
- [x] data: storage for downloaded and converted data
- [x] scripts: Scripts you can execute
- [x] source: Classes implementing the functionality

## Implementation
```mermaid
classDiagram
    class bitfinex_download_candles_py{

    }
    bitfinex_download_candles_py -- HistoricDataExporter

    class binance_download_candles_py{

    }
    binance_download_candles_py -- HistoricDataExporter
    
    class HistoricDataExporter{
      downloadData(pair, start_date, end_date, candle_size_str):
    }

    
    class bitfinex_convert_candles_py{

    }
    bitfinex_convert_candles_py -- BitfinexHistoricCandleConverter
    class BitfinexHistoricCandleConverter{
        convertToPickle(pair, download_data_folder, pickle_data_folder)
        getAsDataframe(pickle_file)
    }	
```
