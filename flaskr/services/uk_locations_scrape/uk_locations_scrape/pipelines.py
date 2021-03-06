# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from logging import getLogger
from datetime import datetime
from scrapy.exceptions import DropItem

from Choys.flaskr.model import db, Location, RentalData


class ChoysPipeline(object):
    def process_item(self, item, spider):
        logger = getLogger()
        if item.get('name') and item.get('average_rent'):
            if Location.query.filter_by(name=item.get('name')).first() is None:
                # If location doesn't already exist in db
                location = Location(name=item['name'])
                db.session.add(location)
                db.session.commit()
            rental_data = RentalData(
                total_properties=item['total_properties'],
                average_rent=item['average_rent'],
                rent_under_250=item['rent_under_250'],
                rent_250_to_500=item['rent_250_to_500'],
                datetime=datetime.utcnow(),
                location_name=item['name']
            )
            db.session.add(rental_data)
            db.session.commit()
            logger.info(f"Inserted {item['name']} into database")
        else:
            raise DropItem("No location_name or average_rent")
        return item
