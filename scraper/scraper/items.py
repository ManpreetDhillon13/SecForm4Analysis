from scrapy import Field, Item

class Form4TransactionItem(Item):

    company = Field() 
    issuerTradingSymbol = Field()
    reportDate = Field()
    ownerId = Field()
    ownerName = Field()

    securityTitle = Field()
    transactionDate = Field()
    sharesTraded = Field()
    pricePerShare = Field()
