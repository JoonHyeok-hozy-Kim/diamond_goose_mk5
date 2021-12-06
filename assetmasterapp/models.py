from django.db import models
import yfinance as yf

# Create your models here.

ASSET_TYPES = (
    ('EQUITY','Equity'),
    ('ETF','ETF(Equity Trade Fund)'),
    ('BOND','Bond'),
    ('REITS','Reits'),
    ('PENSION','Pension'),
    ('CRYPTO','Crypto Asset'),
)

MARKET_CHOICES = (
    ('KSE', 'Korean Stock Exchange(KSE)'),
    ('NASDAQ', 'NASDAQ'),
    ('NYSE', 'NewYork Stock Exchange(NYSE)'),
    ('NA', 'Not Applicable')
)

CURRENCY_CHOICES = (
    ('KRW', 'KRW(￦)'),
    ('USD', 'USD($)'),
)

class Asset(models.Model):
    asset_type = models.CharField(max_length=100, choices=ASSET_TYPES, null=False)
    market = models.CharField(max_length=100, choices=MARKET_CHOICES, null=False)
    ticker = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=200, null=True)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, null=False)
    image = models.ImageField(upload_to='assetmaster/', null=True)

    current_price = models.FloatField(default=0, null=False)

    @property
    def current_price(self):
        yfinance_markets = ['NASDAQ','NYSE']
        other_markets = ['KSE']

        if self.market in yfinance_markets:
            ticker_data = yf.Ticker(self.ticker)
            today_ticker_data = ticker_data.history(period='1d')
            return round(today_ticker_data['Close'][0], 2)

        elif self.market in other_markets:
            return 0

        else:
            if self.asset_type == 'CRYPTO':
                return 0

        return -1
