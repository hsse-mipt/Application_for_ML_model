from sqlite3 import connect
from pandas import DataFrame, read_sql


def read_data_from_db():
    all_news = read_sql('SELECT * FROM different_news_news LIMIT 256', connect('db.sqlite3'))
    return all_news


def write_data_to_db(data: DataFrame):
    data.to_sql(name='different_news_news',
                con=connect('db.sqlite3'),
                index=False,
                if_exists='append')
