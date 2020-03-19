import datetime
import os
import sqlite3

class TenMinScrapyPipeline(object):
    _db = None

    @classmethod

    def get_database(cls):
        cls._db = sqlite3.connect(
            os.path.join(os.getcwd(), 'ten_min_scrapy.db'))

        # テーブル作成
        cursor = cls._db.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS post(\
                id INTEGER PRIMARY KEY AUTOINCREMENT,\
                url TEXT UNIQUE NOT NULL,\
                title TEXT NOT NULL,\
                date DATE NOT NULL\
            );')

        return cls._db

    def process_item(self, item, spider):
        # Pipeline二データが渡される時に実行される。itemにspider殻渡されたitemがセットされる。
        self.save_post(item)
        return item

    def save_post(self, item):
        # itemをデータベースに保存
        if self.find_post(item['url']):
            # 既に同じURLのデータが存在する場合はスキップ
            return

        db = self.get_database()
        db.execute(
            'INSERT INTO post (title, url, date) VALUES (?, ?, ?)',  (
                item['title'],
                item['url'],
                datetime.datetime.strptime(item['date'], '%B %d, %Y')
            )
        )
        db.commit()

    def find_post(self, url):
        db = self.get_database()
        cursor = db.execute(
            'SELECT * FROM post WHERE url=?',
            (url,)
        )
        return cursor.fetchone()