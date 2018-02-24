# -*- coding: utf-8 -*-

import time
from datetime import datetime

from sqlalchemy import Table, Column, String, Integer, DateTime, FLOAT, MetaData, Sequence, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from base.simulator import Simulator
from modules.tank import Tank

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/simulator')

metadata = MetaData()
point_history = Table('point_history', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('timestamp', DateTime),
                      Column('name', String(20)),
                      Column('value', FLOAT))

settings = Table('settings', metadata,
                 Column('name', String(20), primary_key=True),
                 Column('value', FLOAT))
metadata.create_all(engine)

# 创建对象的基类:
Base = declarative_base()

# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

session = DBSession()

# 定义User对象:
class Point(Base):
    __tablename__ = 'point_history'

    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    timestamp = Column(DateTime)
    name = Column(String(20))
    value = Column(FLOAT)

class Settings(Base):
    __tablename__ = 'settings'

    name = Column(String(20), primary_key=True)
    value = Column(FLOAT)


def save(timestamp, values):

    for k in values:
        p = Point(timestamp=datetime.fromtimestamp(timestamp), name=k, value=values[k])
        session.add(p)

    session.commit()

    return


def get_settings():
    values = {}
    settings = session.query(Settings).all()
    for i in range(len(settings)):
        name = settings[i].name
        value = settings[i].value
        values[name] = value

    return values

def load_topo():
    sim = Simulator()
    tank1 = Tank('Tank1')
    #tank2 = Tank('Tank2')

    sim.add(tank1)
    #sim.add(tank2)

    #sim.connect(tank1, tank2)

    return sim

def main():
    interval = 1

    sim = load_topo()
    settings = get_settings()

    sim.set_values(settings)

    # python3
    curr = datetime.now().timestamp()
    save(curr, sim.dump_values())

    print(sim.dump_values())

    prev = curr
    while True:
        time.sleep(0.1)
        curr = datetime.now().timestamp()

        if curr - prev >= interval:
            settings = get_settings()
            sim.set_values(settings)
            sim.step(interval)
            save(curr, sim.dump_values())
            prev = curr

    return 0


if __name__ == "__main__":
    main()
