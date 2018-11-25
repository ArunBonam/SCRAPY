import scrapy
import json
from scrapy.http.request import Request
total_items=[]
class MyItem(scrapy.Item):
        url=scrapy.Field()
        title=scrapy.Field()
        content=scrapy.Field()
class GuardianSpider(scrapy.Spider):
        #counter=0
        name = 'guardian_spider'
        start_urls = ['https://www.theguardian.com/au']
        #item=MyItem()
        #self.total_items=[]
        def __init__(self):
                self.total_items=[]
                self.counter=0
        def parse(self, response):
                
                req=None
                #######======loop through different articles======#########
                for quote in response.css('div.fc-item'):
                        #items=itemTocopy.copy()
                        items={}
                        try:    
                                ######========reading title for each artice=======#######
                                if(quote.css("div.fc-item__container a.js-headline-text::text") !=[]):
                                        items['title']=quote.css("div.fc-item__container a.js-headline-text::text").extract()[0]
                                ######========get hyperlinks for each article======######
                                if(quote.css("div.fc-item__container a::attr(href)") !=[]):
                                        
                                        art_url=quote.css("div.fc-item__container a::attr(href)").extract()[0]
                                
                                        items['url'] =art_url
                               
                        except Exception as e:
                                continue
                                 
                        #########=========add items to the session=======###########
                        response.meta['items']=items
                        if 'url' in items:
                                #############get the content for each url ,calling pageParser#############
                                req= Request(items['url'], callback=self.pageParser,meta={'items':items})
                        
                        yield req
                        
                        #break
               
        def pageParser(self, response):
                
                items=response.meta['items']
                #text={}
                ######gets the content for each url passed########                
                article= response.css("div.content__article-body")
                if(article.xpath("descendant-or-self::p/text()") !=[]):
                        items['content']=article.xpath("descendant-or-self::p/text()").extract()
                        items['content']="".join(items['content'])
                #print("in second function =====>",items)
                #print("====data====",data)
                #table=[]
                #table.append(items)
                #filename='data'+str(self.counter)+'.json'
                #filename='data'+'final2'+'.csv'
                #print(filename)
                #with open(filename,'a+') as outfile:
                        #for line in outfile:
                                #print("line=====",line)
                                #table.append(json.loads(line))       
                        #data=json.load(outfile)
                #data.update(items)
                #with open('data.json', 'a') as outfile:
                        #json.dump(table, outfile)                
                #total_items.append(items)
                #print("total_items=============>",total_items)
                return items



