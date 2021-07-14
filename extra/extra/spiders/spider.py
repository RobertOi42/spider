import scrapy
import json

c = 0
size = 0

class SpiderSpider(scrapy.Spider):
	
	name = 'spider'
	allowed_domains = ['extra.com.br']
	#urls para filtrar produtos a serem achados. Mudar manualmente para cada pois não consegui rodar todos em apenas uma compilação
	#start = 'https://www.extra.com.br/api/catalogo-ssr/products/?Filtro=c13_c14_c13&PaginaAtual=%s&RegistrosPorPagina=20&Platform=1'
	#start = 'https://www.extra.com.br/api/catalogo-ssr/products/?Filtro=c1_c2&PaginaAtual=%s&RegistrosPorPagina=20&Platform=1'
	start = 'https://www.extra.com.br/api/catalogo-ssr/products/?Filtro=c56_c62&PaginaAtual=%s&RegistrosPorPagina=20&Platform=1'
	start_urls = [start % 1]
	download_delay = 1.5 
	
	custom_settings={ 'FEED_URI': "extra_%(name)s.csv",'FEED_FORMAT': 'csv'}       
		 
	def parse(self, response):		
		
		global size	
		global c	
		
		data = json.loads(response.body)
		
		#número de produtos encontrado dividido pelo número mostrado por página, 20 neste caso
		if c == 0:
			t = data.get('filters',[])			
			l = t[0].get('values')
			size = l[0].get('size')		
		
		c1 = size//20
		c1 += 1	
			
		
		for item in data.get('products',[]):
			yield {
				'title': item.get('name'),
				'id': item.get('id'),
				'url': item.get('urls')
				}
		
		#passa para a próxima página do site
		if c < c1:
			next_page = c + 1
			yield scrapy.Request(self.start % next_page)
			
			c += 1
	
		#dentro das categorias do site haviam erros, e por isso alguns produtos aparecem na lista sendo
		#que não são do tipo dos produtos procurados	
			
		
		
		
		
		
			
