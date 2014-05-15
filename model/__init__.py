
# coding:utf-8

#import redis as _redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db = create_engine("sqlite:///database.db")
Base = declarative_base()
Session = sessionmaker(bind=db)

session = Session()

@classmethod
def new(cls, *args, **kwargs):
    i = cls(*args, **kwargs)
    cls.after_new(i, kwargs)
    session.add(i)
    ret = cls.data_commit(i)
    cls.new_done(i, kwargs)
    return ret

@classmethod
def after_new(cls, i, kwargs):
    pass

@classmethod
def new_done(cls, i, kwargs):
    pass

@classmethod
def data_commit(cls, i=None):
    try:
        session.commit()
        return i
    except:
        session.rollback()

@classmethod
def save(cls, id, **kwargs):
    i = cls.get_by_id(id)
    if i:
        for k,v in kwargs.items():
            setattr(i, k, v)
        session.add(i)
        return cls.data_commit(i)

@classmethod
def get_by_id(cls, id):
    if 'id' in cls.__table__.columns:
        return session.query(cls).filter_by(id=id).first()

@classmethod
def get_by_id_list(cls, id_list):
    if 'id' in cls.__table__.columns:
        return session.query(cls).filter(cls.id.in_(map(int, id_list)))

@classmethod
def count_all(cls):
    return session.query(cls).count()

Base.new = new
Base.save = save
Base.get_by_id = get_by_id
Base.get_by_id_list = get_by_id_list
Base.after_new = after_new
Base.new_done = new_done
Base.data_commit = data_commit
Base.count_all = count_all


#redis = _redis.Redis(host='localhost', port=6379, db=0)
