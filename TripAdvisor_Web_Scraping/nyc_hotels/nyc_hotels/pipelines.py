# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from models import Hotels, db_connect, create_hotels_table

class NycHotelsPipeline(object):

    """nychotels pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates hotels table.
        """
        engine = db_connect()
        create_hotels_table(engine)
        #bind individual session to connection
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save hotels in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        hotel = Hotels(**item)

        try:
            session.add(hotel)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
