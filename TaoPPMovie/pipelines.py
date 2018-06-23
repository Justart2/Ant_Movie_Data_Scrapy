# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector

class TaoppmoviePipeline(object):
    def __init__(self):
        self.conn = mysql.connector.connect(user='root',password='root',database='python_test')
        self.cursor = self.conn.cursor()

        #清理数据库
        sql = 'DELETE FROM ant_movie_info;'
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()

    def process_item(self, item, spider):

        #电影标题
        movie_name = item.get('movie_name').strip(' ')
        #电影评分
        movie_rate = item.get('movie_rate')
        if movie_rate != 0:
            movie_rate = movie_rate.strip(' ')
        #电影logo
        movie_img_url = item.get('movie_img_url')

        #导演
        movie_director = item.get('movie_director')
        if movie_director != 'none':
            movie_director = movie_director.split('：')[1].strip(' ')

        #主演
        movie_actors = item.get('movie_actors')
        if movie_actors != 'none':
            movie_actors = movie_actors.split('：')[1].strip(' ')
        #类型
        movie_type = item.get('movie_type')
        if movie_type != 'none':
            movie_type = movie_type.split('：')[1].strip(' ')
        #制片国家/地区
        movie_country = item.get('movie_country')
        if movie_country != 'none':
            movie_country = movie_country.split('：')[1].strip(' ')
        #语言
        movie_language = item.get('movie_language')
        if movie_language != 'none':
            movie_language = movie_language.split('：')[1].strip(' ')
        #片长
        movie_length = item.get('movie_length')
        if movie_length != 'none':
            movie_length = movie_length.split('：')[1].strip(' ')
        #剧情介绍
        movie_description = item.get('movie_description')
        if movie_description != 'none':
            movie_description = movie_description.split('剧情介绍：')[1].strip(' ')
        #上映时间
        movie_show_time = item.get('movie_show_time')
        if movie_show_time != 'none':
            movie_show_time = movie_show_time.split('：')[1].strip(' ')

        #version
        movie_version = '2D/3D/3D-MAX'

        #price
        movie_price = 50.0

        #movie_stage_photos
        movie_stage_photos = ''
        if movie_director!='none' and movie_actors!='none' and movie_type!='none' and movie_country!='none' and movie_language!='none' and movie_length!='none' and movie_description!='none' and movie_show_time!='none':
            insert_sql = '''
                insert into ant_movie_info 
                (m_name, m_type, m_director, m_actor, m_country, m_version, 
                m_time_length, m_description, m_release_time, m_price, m_rate, 
                m_picture,m_stage_photos) 
                values 
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            '''
            #重新插入数据
            #try:
            self.cursor.execute(insert_sql,(movie_name,movie_type,movie_director,movie_actors,movie_country,movie_version,movie_length,movie_description,movie_show_time,movie_price,movie_rate,movie_img_url,movie_stage_photos))
            self.conn.commit()
            #except:
            # self.conn.rollback()
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()

    def clear_database(self):
        sql = 'DELETE FROM ant_movie_info;'
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()

