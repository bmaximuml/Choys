# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

from flask import current_app, g

import logging


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


class HouseScrapePipeline(object):
    def process_item(self, item, spider):
        logger = logging.getLogger()
        if item.get('name') and item.get('average_rent'):
            db = get_db()
            db.execute('INSERT INTO location ('
                       '`name`, '
                       'total_properties, '
                       'average_rent, '
                       'rent_under_250, '
                       'rent_250_to_500'
                       ') VALUES (? ? ? ? ?)',
                       (
                           item['name'],
                           item['total_properties'],
                           item['average_rent'],
                           item['rent_under_250'],
                           item['rent_250_to_500']
                       ))
            db.commit()
            logger.info(f"Inserted {item['name']} into database")
        return item
