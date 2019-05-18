"""
Name: Ryan Golub & Ali Namin
Directory ID: 114586131 & 114783462
Date: 5/17/19
Assignment: Final Project
"""

import urllib.request
import json

class Coin:
    """Stores Cryptocurrency coin information"""
    def __init__(self, data):
        self.id = int(data['id'])
        self.symbol = data['symbol']
        self.name = data['name']

class Social:
    """Stores Cryptocurrency social information"""
    def __init__(self, data, coin):
        self.coin = coin
        self.reddit = data['reddit']
        self.twitter = data['twitter']

class Market:
    """Stores Cryptocurrency market information"""
    def __init__(self, data, coin):
        self.coin = coin
        self.name = data['name']
        self.base = data['base']
        self.quote = data['quote']
        self.price = data['price']
        self.price_usd = data['price_usd']
        self.volume = data['volume']
        self.volume_usd = data['volume_usd']
        self.time = data['time']

class Ticker:
    """Stores Cryptocurrency Ticker information"""
    def __init__(self, data, coin):
        self.coin = coin
        self.rank = data['rank']
        self.price_usd = data['price_usd']
        self.percent_change_24h = data['percent_change_24h']
        self.percent_change_1h = data['percent_change_1h']
        self.percent_change_7d = data['percent_change_7d']
        self.market_cap_usd = data['market_cap_usd']
        self.volume24 = data['volume24']
        self.volume24_native = data['volume24_native']
        self.csupply = data['csupply']
        self.price_btc = data['price_btc']
        self.tsupply = data['tsupply']
        self.msupply = data['msupply']

class CryptoAPIGetter:
    """Wrapper class for CoinLore cryptocurrency api"""

    def __init__(self):
        """Retrieves all available cryptocurrency info from api"""

        self.request_url = 'https://api.coinlore.com/api/'
        # retrieve available cryptocurrencies
        self.coins = self.requestCoinsInfo()

    def processRequest(self, url):
        """Processes a request from CoinLore api

        Parameters:
            url (str): url to retrieve jason data from

        Returns:
            dictionary: processed json from url query
        """

        # Retrieve api request
        with urllib.request.urlopen(url) as request:
            data = json.loads(request.read().decode())
            return data

    def getCoinInfo(self, symbol = '', id = -1, name = ''):
        """Retrieves cryptocurrency stored in object

        Parameters:
            symbol (str): cryptocurrency ticker symbol
            id (int): cryptocurrency identification number
            name (str): cryptocurrency name

        Returns:
            Coin: requested cryptocurrency or None if it doesnt exist
        """

        for coin in self.coins:
            if symbol != '':
                if symbol.lower() == coin.symbol.lower():
                    return coin
            elif id != -1:
                if id == coin.id:
                    return coin
            elif name != '':
                if name.lower() == coin.name.lower():
                    return coin
            else:
                return None

    def isValidCoin(self, symbol = '', id = -1, name = ''):
        """Checks if cryptocurrency is available from api

        Parameters:
            symbol (str): cryptocurrency ticker symbol
            id (int): cryptocurrency identification number
            name (str): cryptocurrency name

        Returns:
            boolean: True if currency exists false otherwise
        """

        coin = self.getCoinInfo(symbol, id, name)

        if coin == None:
            return False

        return True

    def requestCoinsInfo(self):
        """Requests all cryptocurrencies from api and returns them

        Returns:
            list of Coin: list of coins availabe in API
        """

        processed = []
        url = self.request_url + 'tickers'
        data = self.processRequest(url)['data']
        for coin in data:
            processed.append(Coin(coin))

        return processed

    def getTickerData(self, symbol = '', id = -1, name = ''):
        """Gets ticker information from currency symbol, id or name

        Parameters:
            symbol (str): cryptocurrency ticker symbol
            id (int): cryptocurrency identification number
            name (str): cryptocurrency name

        Returns:
            Ticker: ticker of requested coin or None if coin doesn't exist
        """

        # Check currency is valid
        coin = self.getCoinInfo(symbol, id, name)
        if coin == None:
            return None

        # Run request for currency ticker data
        url = self.request_url + 'ticker/?id=' + str(coin.id)
        data = self.processRequest(url)

        return Ticker(data[0], coin)

    def getGlobalData(self):
        """Retrieves global cryptocurrency market informaton from api

        Returns:
            dictionary: contains information about the global crypto market
        """

        # Run request for global crypto market data
        url = self.request_url + 'global/'
        data = self.processRequest(url)

        return data[0]

    def getCoinMarket(self, symbol = '', id = -1, name = ''):
        """Retrieves first 50 markets for specific currency

        Parameters:
            symbol (str): cryptocurrency ticker symbol
            id (int): cryptocurrency identification number
            name (str): cryptocurrency name

        Returns:
            list of Market: list containing market information for currency
        """

        # Check cryptocurrency is valid
        coin = self.getCoinInfo(symbol, id, name)
        if coin == None:
            return None

        # Run request for cryptocurrency markets
        url = self.request_url + 'coin/markets/?id=' + str(coin.id)
        data = self.processRequest(url)

        # Transform response to list of Market objects
        market = []
        for mark in data:
            market.append(Market(mark, coin))

        return market

    def getSocialStats(self, symbol = '', id = -1, name = ''):
        """Retrieves social stats for specified cryptocurrency

        Parameters:
            symbol (str): cryptocurrency ticker symbol
            id (int): cryptocurrency identification number
            name (str): cryptocurrency name

        Returns:
            Social: social object for specified currency
        """

        # Check if cryptocurrency is valid
        coin = self.getCoinInfo(symbol, id, name)
        if coin == None:
            return None

        # Run request for social media data of cryptocurrency
        url = self.request_url + 'coin/social_stats/?id=' + str(coin.id)
        data = self.processRequest(url)

        return Social(data, coin)

class CryptoAnalyzer:
    """Class that allows us to analyze data recieved from CoinLore api"""

    main_prompt = """\n ---- Main Menu ----
Select the information you with to view
 1) Global Crypto Market
 2) Crypto Ticker
 3) Crypto Coin Markets
 4) Crypto Social Media
 5) Quit
 --> """

    def __init__(self):
        self.api = CryptoAPIGetter()

    def start(self):
        """Starts the analysis program"""

        while True:
            self.prompt()
            print("\n\n Press Enter for Main Menu")
            input(" > ")

    def prompt(self):
        """Prompts user for what information they would like to see about
        cryptocurrencies of their choice"""

        collecting = True

        # Determine what information the user wants to view
        while collecting:
            inp = input(self.main_prompt).strip()

            if inp == '1':
                collecting = False
                self.displayGlobalInfo()
            elif inp == '2':
                collecting = False
                coins = self.selectCurrencies()
                self.displayTickerInfo(coins)
            elif inp == '3':
                collecting = False
                coins = self.selectCurrencies()
                n = self.getNumMarkets()
                self.displayCryptoMarkets(coins, n)
            elif inp == '4':
                collecting = False
                coins = self.selectCurrencies()
                self.displayCryptoSocial(coins)
            elif inp == '5':
                exit()
            else:
                print("\n Invalid option try again.")

    def selectCurrencies(self):
        """Prompts the user for which currencies they would like to analyze

        Returns:
            list of Coin: list contining users requested cryptocurrencies
        """

        info = """\n What Crypto currencies would you like to view?
 Separate the names by commas"""
        print(info)

        inp = input(" --> ").strip().split(',')

        coins = []

        # Determine if entered cryptocurrency is valid
        for coin in inp:
            coin = coin.strip()
            if self.api.isValidCoin(name=coin):
                coins.append(self.api.getCoinInfo(name = coin))
            else:
                print(" " + coin + " is invalid currency, skipping.\n")

        return coins

    def displayGlobalInfo(self):
        """Displays Global Market data from CoinLore API"""

        data = self.api.getGlobalData()

        print("\n -- Global Cryptocurrency Market --")
        print(" Number of Currencies: " + str(data['coins_count']))
        print(" Number of Active Markets: " + str(data['active_markets']))
        print(" Market Capitalization: $" + str(int(data['total_mcap'])))
        print(" Total Market Volume: $" + str(int(data['total_volume'])))
        print(" Market Cap Change: $" + str(data['mcap_change']))
        print(" Volume Change: $" + str(data['volume_change']))
        print(" Average Change Percentage: " + str(data['avg_change_percent']) + "%")

    def displayTickerInfo(self, coins):
        """Displays ticker information for specified cryptocurrencies

        Parameters:
            coins (list of Coin): cryptocurrencies to be analyzed
        """

        tickers = []
        for coin in coins:
            tickers.append(self.api.getTickerData(symbol=coin.symbol))

        for ticker in tickers:
            print("\n -- Ticker Info for " + ticker.coin.name.upper() + " --")
            print(" Rank: " + str(ticker.rank))
            print(" Price (USD): " + str(ticker.price_usd))
            print(" Change 1 hour: " + str(ticker.percent_change_1h) + "%")
            print(" Change 24 hours: " + str(ticker.percent_change_24h) + "%")
            print(" Change 7 days: " + str(ticker.percent_change_7d) + "%")
            print(" Market Capitalization (USD): $" + str(ticker.market_cap_usd))
            print(" Volume 24 hours: $" + str(ticker.volume24))
            print(" Circulating Supply: " + str(ticker.csupply))
            print(" Total Supply: " + str(ticker.tsupply))
            print(" BTC conversion: " + str(ticker.price_btc) + " BTC")

    def getNumMarkets(self):
        """Requests user for the number of crypto markets they would like to
        analyze"""

        # Prompt the user for number of markets requested until valid input
        n = 0
        print(" How many markets would you like to see for each coin?")
        while n <= 0:
            try:
                n = int(input(" --> "))
            except:
                n = 0

            if n <= 0:
                print(" Invalid number, try again.")

        return n

    def displayCryptoMarkets(self, coins, n):
        """Displays a specified number of crypto markets a specified
        cryptocurrency.

        Parameters:
            coins (list of coin): cryptocurrencies to analyze
            n (int): number of markets to analyze
        """

        for coin in coins:
            markets = self.api.getCoinMarket(symbol=coin.symbol)

            print("\n ---- " + coin.name.upper() + " Markets ----")

            i = 0
            for market in markets:
                print("\n -- " + market.name + " --")
                print(" Base: " + market.base)
                print(" Quote: " + market.quote)
                print(" Price (USD): $" + str(market.price_usd))
                print(" Volume (USD): $" + str(market.volume_usd))
                print(" Time: " + str(market.time))
                i = i + 1
                if i >= n:
                    break

    def displayCryptoSocial(self, coins):
        """Displays Social Media information for selected cryptocurrencies

        Parameters:
            coins (list of Coin): Cryptocurrencies to be analyzed
        """

        for coin in coins:
            social = self.api.getSocialStats(symbol = coin.symbol)

            print("\n -- Social Info for " + coin.name.upper() + " --")
            print(" Reddit:")
            print("\tAverage Active Users: " + str(int(social.reddit['avg_active_users'])))
            print("\tNumber of Subscribers: " + str(social.reddit['subscribers']))
            print(" Twitter:")
            print("\tNumber of Followers: " + str(social.twitter['followers_count']))
            print("\tNumber of Status: " + str(social.twitter['status_count']))


def main():
    # Start crypto analyzer program
    prompter = CryptoAnalyzer()
    prompter.start()

if __name__ == '__main__':
    main()
