import scrapy
from TaoPPMovie.items import TaoppmovieItem
class TaoPPMovieShowListSpider(scrapy.Spider):
	name = 'taopp_movie_show_list'
	start_urls = [
		'https://dianying.taobao.com/showList.htm'
	]

	def parse(self,response):

		movie_show_list_xpaths = response.xpath('//div[@class="tab-content"]')

		for movie_show_spath in movie_show_list_xpaths.xpath('div[@class="tab-movie-list"]'):
		#for movie_show_spath in movie_show_list_xpaths.xpath('div[1]'):

			for movie in movie_show_spath.xpath('div[@class="movie-card-wrap"]'):
				movie_detail_url = movie.xpath('a[1]/@href').extract()[0]
				movie_name = movie.xpath("a[1]/div[@class='movie-card-name']/span[@class='bt-l']/text()").extract()[0]

				#print(movie_detail_url,movie_name)
		
				yield scrapy.Request(movie_detail_url, callback=self.parseMovieDetailComplete)
	
	'''
	def parseMovieDetail(self,response):
		movieItem = TaoppmovieItem()
		movie_info = response.xpath('//div[@class="detail-cont"]/div[@class="center-wrap"]')
		#电影标题
		movie_name = movie_info.xpath('h3/text()').extract()[0]
		#print(movie_name)
		movieItem['movie_name'] = movie_name
		#电影评分
		if(len(movie_info.xpath('h3/em/text()')) == 1):
			movie_rate = movie_info.xpath('h3/em/text()').extract()[0]
		else:
			movie_rate = ''
		#print(movie_rate)
		movieItem['movie_rate'] = movie_rate
		#电影logo
		movie_img_url = movie_info.xpath('div[@class="cont-pic"]/img/@src').extract()[0]
		#print(movie_img_url)
		movieItem['movie_img_url'] = movie_img_url

		#if(len(movie_info.xpath('ul[@class="cont-info"]/li[1]/text()').extract()[0]) == 0):
		#导演
		movie_director = movie_info.xpath('ul[@class="cont-info"]/li[1]/text()').extract()[0]
		#print(movie_director)
		movieItem['movie_director'] = movie_director
		#主演
		movie_actors = movie_info.xpath('ul[@class="cont-info"]/li[2]/text()').extract()[0]
		#print(movie_actors)
		movieItem['movie_actors'] = movie_actors
		#类型
		movie_type = movie_info.xpath('ul[@class="cont-info"]/li[3]/text()').extract()[0]
		#print(movie_type)
		movieItem['movie_type'] = movie_type
		#制片国家/地区
		movie_country = movie_info.xpath('ul[@class="cont-info"]/li[4]/text()').extract()[0]
		#print(movie_country)
		movieItem['movie_country'] = movie_country
		#语言
		movie_language = movie_info.xpath('ul[@class="cont-info"]/li[5]/text()').extract()[0]
		#print(movie_language)
		movieItem['movie_language'] = movie_language
		#片长
		movie_length = movie_info.xpath('ul[@class="cont-info"]/li[6]/text()').extract()[0]
		#print(movie_length)
		movieItem['movie_length'] = movie_length
		#剧情介绍
		movie_description = movie_info.xpath('ul[@class="cont-info"]/li[7]/text()').extract()[0]
		#print(movie_description)
		movieItem['movie_description'] = movie_description
		#上映时间
		if(len(movie_info.xpath('div[@class="cont-time"]/text()')) == 1):
			movie_show_time = movie_info.xpath('div[@class="cont-time"]/text()').extract()[0]
		else:
			movie_show_time = ''
		#print(movie_show_time)
		movieItem['movie_show_time'] = movie_show_time

		return movieItem
	'''
	def parseMovieDetailComplete(self,response):
		movieItem = TaoppmovieItem()
		#初始化Item数据格式
		self.initItem(movieItem)

		movie_info = response.xpath('//div[@class="detail-cont"]/div[@class="center-wrap"]')
		#电影标题
		movie_name = movie_info.xpath('h3/text()').extract()[0]
		#print(movie_name)
		movieItem['movie_name'] = movie_name
		#电影评分
		movie_rate = 0;
		if(len(movie_info.xpath('h3/em/text()')) == 1):
			movie_rate = movie_info.xpath('h3/em/text()').extract()[0]
		#print(movie_rate)
		movieItem['movie_rate'] = movie_rate
		#电影logo
		movie_img_url = movie_info.xpath('div[@class="cont-pic"]/img/@src').extract()[0]
		#print(movie_img_url)
		movieItem['movie_img_url'] = movie_img_url

		#上映时间
		movie_show_time = movie_info.xpath('div[@class="cont-time"]/text()').extract()[0]
		movieItem['movie_show_time'] = movie_show_time

		#不同格式区分
		movie_other_infos = movie_info.xpath('ul[@class="cont-info"]/li')
		for movie_other_info in movie_other_infos:
			movie_other = movie_other_info.xpath('text()').extract()[0]
			#print (movie_other)

			#导演
			if movie_other.find('导演：') != -1:
				#print (movie_other)
				movieItem['movie_director'] = movie_other

  			#主演
			if movie_other.find('主演：') != -1:
				#print (movie_other)
				movieItem['movie_actors'] = movie_other

			#制片国家/地区
			if movie_other.find('制片国家/地区：') != -1:
				#print (movie_other)
				movieItem['movie_country'] = movie_other

			#片长
			if movie_other.find('片长：') != -1:
				#print (movie_other)
				movieItem['movie_length'] = movie_other

			#语言
			if movie_other.find('语言：') != -1:
				#print (movie_other)
				movieItem['movie_language'] = movie_other

			#剧情介绍
			if movie_other.find('剧情介绍：') != -1:
				#print (movie_other)
				movieItem['movie_description'] = movie_other

			#上映时间
			if movie_other.find('上映时间：') != -1:
				#print (movie_other)
				movieItem['movie_show_time'] = movie_other

			#类型
			if movie_other.find('类型：') != -1:
				#print (movie_other)
				movieItem['movie_type'] = movie_other

		return movieItem

	def initItem(self,movieItem):

		#电影标题
		movieItem['movie_name'] = 'none'

		#电影评分
		movieItem['movie_rate'] = 0

		#电影logo
		movieItem['movie_img_url'] = 'none'

		#导演
		movieItem['movie_director'] = 'none'

  		#主演
		movieItem['movie_actors'] = 'none'

		#制片国家/地区
		movieItem['movie_country'] = 'none'

		#片长
		movieItem['movie_length'] = 'none'

		#语言
		movieItem['movie_language'] = 'none'

		#剧情介绍
		movieItem['movie_description'] = 'none'

		#上映时间
		movieItem['movie_show_time'] = 'none'

		#类型
		movieItem['movie_type'] = 'none'

