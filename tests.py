"""
Name: & Ryan Golub & Ali Namin
Directory ID: 114586131 & 114783462 
Date: 5/17/19
Assignment: Final Project
"""

from Crypto import CryptoAPIGetter
import pytest

"""Tests CryptoAPIGetter to make sure desired results are achieved"""

api = CryptoAPIGetter()

def test_coin_info():
    coin = api.getCoinInfo(symbol = "BTC")
    assert coin.name.lower() == 'bitcoin'

    coin = api.getCoinInfo(id=90)
    assert coin.symbol == "BTC"

    coin = api.getCoinInfo(name="bitcoin")
    assert coin.id == 90

def test_is_valid_coin():
    assert api.isValidCoin(symbol = "BTC") == True
    assert api.isValidCoin(id = 90) == True
    assert api.isValidCoin(name = "bitcoin") == True

    assert api.isValidCoin(symbol = "FAKE") == False
    assert api.isValidCoin(id = -400) == False
    assert api.isValidCoin(name = "fakecoin") == False

def test_ticker_data():
    ticker = api.getTickerData(symbol = "FAKE")
    assert ticker == None

    ticker = api.getTickerData(symbol = "BTC")
    assert ticker.coin.name.lower() == "bitcoin"

def test_global_data():
    data = api.getGlobalData()
    assert data['coins_count'] > 0

def test_market_data():
    markets = api.getCoinMarket(symbol = "FAKE")
    assert markets == None

    markets = api.getCoinMarket(symbol = "BTC")
    assert len(markets) > 0
    assert markets[0].name != ""

def test_social_data():
    social = api.getSocialStats(symbol = "FAKE")
    assert social == None

    social = api.getSocialStats(symbol = "BTC")
    assert social.reddit != None
    assert social.twitter != None
