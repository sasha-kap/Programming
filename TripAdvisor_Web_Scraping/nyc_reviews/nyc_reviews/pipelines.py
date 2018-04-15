# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from models import Reviews, db_connect, create_reviews_table

class NycReviewsPipeline(object):

    """nycreviews pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates reviews table.
        """
        engine = db_connect()
        create_reviews_table(engine)
        #bind individual session to connection
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save reviews in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        review = Reviews(**item)

        try:
            session.add(review)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
