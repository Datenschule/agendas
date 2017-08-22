# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker
from .models import Topic, db_connect, create_deals_table


class AgendasPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_deals_table(engine)
        self.Session = sessionmaker(bind=engine)

    def open_spider(self, spider):
        session = self.Session()
        topics = session.query(Topic)
        print("-----------")
        print(topics)
        print ('__')
        print(topics.count())
        print("-----------")
        if topics.count() > 0:
            [session.delete(topic) for topic in topics]
        session.commit()


    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        topic = Topic(**item)

        topic.add_or_update(session)

        try:
            session.add(topic)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
