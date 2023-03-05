from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import Form4TransactionItem
import time

class Form4Spider(CrawlSpider):
    name = 'form4'
    company_xpath = "//issuerName/text()"
    trading_sym_xpath = "//issuerTradingSymbol/text()"
    report_date_xpath = "//periodOfReport/text()"
    owner_id_xpath = "//reportingOwner/reportingOwnerId/rptOwnerCik/text()"
    owner_name_xpath = "//reportingOwner/reportingOwnerId/rptOwnerName/text()"
    transactions_xpath = "//nonDerivativeTable/nonDerivativeTransaction"
    security_title_xpath = ".//securityTitle/value/text()"
    transaction_code_xpath = ".//transactionAmounts/transactionAcquiredDisposedCode/value/text()"
    transaction_date_xpath = ".//transactionDate/value/text()"
    shares_traded_xpath = ".//transactionAmounts/transactionShares/value/text()"                    
    share_price_xpath = ".//transactionAmounts/transactionPricePerShare/value/text()"

    def __init__(self, *args, **kwargs):
        # self.start_urls = [_ for _ in kwargs.pop('start_urls').split(',')]
        self.start_urls = kwargs.pop('start_urls')
        self.rules = (
            Rule(LinkExtractor(restrict_text = '.*form4.*'), callback = 'parse_form4'),
        )
        super(Form4Spider, self).__init__(*args, **kwargs)

    def parse_form4(self, response):
        """parses the form4 xml and returns each transaction for acquired common Stocks"""

        # with open(f"sampleForm4_{response.url}.xml", 'w') as fhandle:
        #     fhandle.write(response.text)

        form4 = Form4TransactionItem()
        form4['company'] = response.xpath(self.company_xpath).get()
        form4['issuerTradingSymbol'] = response.xpath(self.trading_sym_xpath).get()
        form4['reportDate'] = response.xpath(self.report_date_xpath).get()
        form4['ownerId'] = response.xpath(self.owner_id_xpath).get()
        form4['ownerName'] = response.xpath(self.owner_name_xpath).get()
        
        for transaction in response.xpath(self.transactions_xpath):
            securityTitle = transaction.xpath(self.security_title_xpath).get()
            form4['securityTitle'] = securityTitle
            form4['transactionDate'] = transaction.xpath(self.transaction_date_xpath).get()
            transactionAcquiredDisposedCode = transaction.xpath(self.transaction_code_xpath).get()

            if 'common stock' in securityTitle.lower() and transactionAcquiredDisposedCode == "A":
                shares_traded = transaction.xpath(self.shares_traded_xpath).get()
                price_per_share = transaction.xpath(self.share_price_xpath).get()
                form4['sharesTraded'] = shares_traded
                form4['pricePerShare'] = price_per_share if price_per_share else 0
                yield form4
        time.sleep(0.2)