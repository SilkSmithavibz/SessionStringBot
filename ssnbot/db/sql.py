import asyncio
import threading
from sqlalchemy import create_engine, Column, TEXT, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.pool import StaticPool
from ssnbot import DB_URL

BASE = declarative_base()

class Broadcast(BASE):
    __tablename__ = "broadcast"
    user_id = Column(BigInteger, primary_key=True)
    user_name = Column(TEXT)

    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name

def start() -> scoped_session:
    engine = create_engine(
        DB_URL, client_encoding="utf8", poolclass=StaticPool, future=True)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False, future=True))

# Create the scoped session (thread-safe for multiple calls)
SESSION = start()
INSERTION_LOCK = threading.RLock()

# Asynchronous function to add a user to the database
async def add_user(user_id, user_name):
    loop = asyncio.get_event_loop()
    # Using the event loop to run synchronous DB calls to avoid blocking the event loop
    await loop.run_in_executor(None, _add_user_sync, user_id, user_name)

def _add_user_sync(user_id, user_name):
    with INSERTION_LOCK:
        try:
            usr = SESSION.query(Broadcast).filter_by(user_id=user_id).one()
        except NoResultFound:
            usr = Broadcast(user_id=user_id, user_name=user_name)
            SESSION.add(usr)
            SESSION.commit()

# Asynchronous function to check if a user exists
async def is_user(user_id):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, _is_user_sync, user_id)
    return result

def _is_user_sync(user_id):
    with INSERTION_LOCK:
        try:
            usr = SESSION.query(Broadcast).filter_by(user_id=user_id).one()
            return usr.user_id
        except NoResultFound:
            return False

# Asynchronous function to query all users' IDs
async def query_msg():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, _query_msg_sync)
    return result

def _query_msg_sync():
    try:
        query = SESSION.query(Broadcast.user_id).order_by(Broadcast.user_id)
        return query.all()
    finally:
        SESSION.close()

# Asynchronous function to delete a user from the database
async def del_user(user_id):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _del_user_sync, user_id)

def _del_user_sync(user_id):
    with INSERTION_LOCK:
        try:
            usr = SESSION.query(Broadcast).filter_by(user_id=user_id).one()
            SESSION.delete(usr)
            SESSION.commit()
        except NoResultFound:
            pass
