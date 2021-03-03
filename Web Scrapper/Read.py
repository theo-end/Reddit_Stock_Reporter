import csv

def Read_Ticker_List(file_name):    #This Function reads in a list of stock tickers from a .csv file
    with open(file_name) as f:      #Opens the file
        r = csv.reader(f)           #Initializes the read object
        tickers = []                #Makes the ticker stoage list
        for line in r:              #Adds the read-in ticker to the ticker list
          tickers.extend(line)
    
    return tickers                  #Returns the final list of tickers

stock_tickers = Read_Ticker_List('stock_tickers.csv')
stock_ticker_letters = Read_Ticker_List('Stock_Ticker_Letters.csv')
stock_ticker_words = Read_Ticker_List('stock_ticker_words.csv')
stock_tickers_abbr = Read_Ticker_List('Stock_Ticker_Abbreviations.csv')