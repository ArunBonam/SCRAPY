import scrapy
import json
from scrapy.http.request import Request
total_items=[]
class MyItem(scrapy.Item):
        url=scrapy.Field()
        title=scrapy.Field()
        content=scrapy.Field()
class QuotesSpider(scrapy.Spider):
        #counter=0
        name = 'guardian_spider_test_3_w1'
        start_urls = ['https://www.theguardian.com/au']
        #item=MyItem()
        #self.total_items=[]
        def __init__(self):
                self.total_items=[]
                self.counter=0
        def parse(self, response):
                #items={}
                req=None
                #itemTocopy =response.meta['items']
                for quote in response.css('div.fc-item'):
                        #items=itemTocopy.copy()
                        items={}
                        try:
                                if(quote.css("div.fc-item__container a.js-headline-text::text") !=[]):
                                        items['title']=quote.css("div.fc-item__container a.js-headline-text::text").extract()[0]
                                if(quote.css("div.fc-item__container a::attr(href)") !=[]):
                                #print("test quote=========>",quote.css("div.fc-item__container a::attr(href)"))
                                #items['url']=quote.css("div.fc-item__container a::attr(href)").extract()[0]
                                        art_url=quote.css("div.fc-item__container a::attr(href)").extract()[0]
                                #print(art_url)
                                        items['url'] =art_url
                                #print("----")
                                #print(items)
                        except Exception as e:
                                continue
                                 
                        #print("sending : {}".format(items['url']))
                        response.meta['items']=items
                        if 'url' in items:
                                req= Request(items['url'], callback=self.pageParser,meta={'items':items})
                        #req= Request(items['url'], callback=self.pageParser,meta={'items':items})
                        #req.meta['items'] = items
                        #req.meta['items']=response.meta['items']
                        yield req
                        #yield items
                        #print("yielded  item=======>",item)
                        #print("items======>",items)
                        #break
                #return req
                #print(items)
                #print(items['url'][0])
                #extr_url=items['url'][0]
                #yield Request(extr_url, callback=self.pageParser)
        def pageParser(self, response):
                #total_items=[]
                #self.counter=self.counter+1
                #print(self.counter)
                #print("==========In second parser===================")
                items=response.meta['items']
                #text={}
                #print("in second function",items)                
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



