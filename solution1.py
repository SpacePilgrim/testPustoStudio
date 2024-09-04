# Предположив, что подключение к БД выполняется в другом месте, опишу модели и методы согласно заданию при помощи SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ARRAY
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

login_reward = 1 # Награда игроку за вход

class Player(Base):
  __tablename__ = 'players'

  id = Column(Integer, primary_key=True)
  username = Column(String(32), unique=True, nullable=False)
  points = Column(Integer, default=0)
  first_seen_time = Column(Datetime)
  last_seen_time = Column(Datetime)
  boosts = Column(ARRAY(Integer))

  def __init__(self):
    boosts = []
  
  def login(self, session):
    now = datetime.now()
    self.first_seen_time = now if not self.first_seen_time
    self.last_seen_time = now
    self.points += login_reward
    session.commit()    

class Boost(Base):
  __tablename__ = 'boost_types'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  description = Column(String(128))


def give_player_boost(session, player_id, boost_id):
  player_to_boost = session.scalar(select(Player).where(Player.id = player_id))
  if player_to_boost is not None:
    player_to_boost.boosts.append(boost_id)
    session.commit()
