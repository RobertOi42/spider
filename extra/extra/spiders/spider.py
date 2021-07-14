import scrapy
import json

c = 0
size = 0

class SpiderSpider(scrapy.Spider):
	
	name = 'spider'
	allowed_domains = ['extra.com.br']
	#start_im = 'https://www.extra.com.br/api/catalogo-ssr/products/?Filtro=c56_c62&PaginaAtual=%s&RegistrosPorPagina=20&Platform=1'	
	#start_tv = 'https://www.extra.com.br/api/catalogo-ssr/products/?Filtro=c1_c2&PaginaAtual=%s&RegistrosPorPagina=20&Platform=1'
	start = ['https://www.extra.com.br/api/catalogo-ssr/products/?Filtro=c13_c14_c13&PaginaAtual=%s&RegistrosPorPagina=20&Platform=1',
				'https://www.extra.com.br/api/catalogo-ssr/products/?Filtro=c1_c2&PaginaAtual=%s&RegistrosPorPagina=20&Platform=1',
				'https://www.extra.com.br/api/catalogo-ssr/products/?Filtro=c56_c62&PaginaAtual=%s&RegistrosPorPagina=20&Platform=1']
	start_urls = [start[0] % 1,start[1] % 1,start[2] % 1]
	download_delay = 1.5 
	
	custom_settings={ 'FEED_URI': "extra_%(name)s.csv",'FEED_FORMAT': 'csv'}       
		 
	def parse(self, response):		
		
		global size	
		global c	
		
		data = json.loads(response.body)
		
		if c == 0:
			t = data.get('filters',[])			
			l = t[0].get('values')
			size = l[0].get('size')		
		
		c1 = size//20
		c1 += 1	
			
		#title = response.xpath("//div[@class='styles__ProductCardWrapper-sc-1gzprri-6 styles__ResponsiveWrapper-sc-1gzprri-9 hEMyDr']/div[@class='styles__Content-sc-1gzprri-7 jubJiu']/div[@class='styles__CardInfo-sc-1gzprri-5 iIqxUk']/a[@class='styles__Title-sc-1gzprri-1 kWIhVj']/text()").extract()
		#url = response.xpath("//div[@class='styles__ProductCardWrapper-sc-1gzprri-6 styles__ResponsiveWrapper-sc-1gzprri-9 hEMyDr']/div[@class='styles__Content-sc-1gzprri-7 jubJiu']/div[@class='styles__CardInfo-sc-1gzprri-5 iIqxUk']/a/@href").extract()
		#SKU = []
		#for i in range(len(url)):	
		#	u =[int(s) for s in url[i].split("/") if s.isdigit()]
		#	SKU.append(u[0])
		
		
		for item in data.get('products',[]):
			yield {
				'title': item.get('name'),
				'id': item.get('id'),
				'url': item.get('urls')
				}
		
		if c < c1:
			next_page = c + 1
			yield scrapy.Request(self.start[0] % next_page)
			
			c += 1
	
			
		
		
		
		
		
			
