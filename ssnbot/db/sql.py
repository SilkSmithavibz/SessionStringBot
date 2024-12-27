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

    def __init__(self, user_id: int, user_name: str):
        self.user_id = user_id
        self.user_name = user_name


def start() -> scoped_session:
    """
    Initialize the database connection and create tables if they don't exist.
    Returns:
        scoped_session: Thread-safe session maker.
    """
    engine = create_engine(
        DB_URL, client_encoding="utf8", poolclass=StaticPool
    )
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


SESSION = start()
INSERTION_LOCK = threading.RLock()


def add_user(user_id: int, user_name: str) -> None:
    """
    Add a user to the database if they don't already exist.
    Args:
        user_id (int): Telegram user ID.
        user_name (str): Telegram user name.
    """
    with INSERTION_LOCK:
        try:
            usr = SESSION.query(Broadcast).filter_by(user_id=user_id).one()
        except NoResultFound:
            usr = Broadcast(user_id=user_id, user_name=user_name)
            SESSION.add(usr)
            SESSION.commit()


def is_user(user_id: int) -> bool:
    """
    Check if a user exists in the database.
    Args:
        user_id (int): Telegram user ID.
    Returns:
        bool: True if user exists, False otherwise.
    """
    with INSERTION_LOCK:
        try:
            usr = SESSION.query(Broadcast).filter_by(user_id=user_id).one()
            return True
        except NoResultFound:
            return False


def query_msg() -> list:
    """
    Retrieve all user IDs from the database.
    Returns:
        list: List of user IDs.
    """
    with INSERTION_LOCK:
        try:
            query = SESSION.query(Broadcast.user_id).order_by(Broadcast.user_id)
            return query.all()
        except Exception as e:
            print(f"Error querying messages: {e}")
            return []


def del_user(user_id: int) -> None:
    """
    Delete a user from the database.
    Args:
        user_id (int): Telegram user ID.
    """
    with INSERTION_LOCK:
        try:
            usr = SESSION.query(Broadcast).filter_by(user_id=user_id).one()
            SESSION.delete(usr)
            SESSION.commit()
        except NoResultFound:
            pass
