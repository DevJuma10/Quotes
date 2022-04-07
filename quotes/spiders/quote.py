import scrapy
from scrapy_splash import SplashRequest

class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['http://quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/js//']


    script = '''
    
        function main(splash, args)
        
            splash:set_user_agent("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36")

            assert(splash:go(args.url))
            assert(splash:wait(0.5))
                
            
            return {
                html = splash:html(),
            }
        end
    
    '''

    def start_requests(self):
        yield SplashRequest(
            url = 'https://quotes.toscrape.com/js/',
            callback = self.parse ,
            endpoint = "execute",
            args = {
                'lua_source' : self.script
            }
        ) 

    def parse(self, response):
        for quote in response.xpath("//div[contains(@class,'quote')]"):
            yield{
                "text"  : quote.xpath(".//span[1]/text()").get(),
                "author"    : quote.xpath("//span[2]/small/text()").get(),
                "tags"    : quote.xpath(".//div/a/text()").getall()
            }


        #HANDLING PAGINATION
        next_page = response.xpath("//ul/li[1]/a/@href").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url = next_page_url, callback = self.parse)
