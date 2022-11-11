# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Stacker(Base):
    """
    The Database model for the Stacker table.
    """
    __tablename__ = 'threads'

    id = Column(Integer, primary_key=True)
    thread_id = Column(Integer)
    title = Column(String)
    sats = Column(Integer)
    comments = Column(Integer)
    create_at = Column(DateTime)

    def __init__(self, thread_id, title, sats, comments, create_at):
        self.thread_id = thread_id
        self.title = title
        self.sats = sats
        self.comments = comments
        self.create_at = create_at


class SqliteDatabase(object):
    def __init__(self, db_name):
        self.engine = create_engine(db_name, echo=False)
        # create tables
        Base.metadata.create_all(self.engine)

        # create a Session
        session_made = sessionmaker(bind=self.engine)
        self.session = session_made()

    def add_thread(self, thread_id: int, title: str, sats: int, comments: int):
        """
        Add a thread to the database.
        :param thread_id: The thread id to add.
        :param title: The thread title to add.
        :param sats: The thread sats to add.
        :param comments: The thread comments to add.
        """
        thread_db = self.get_thread(thread_id)
        if thread_db:
            return
        thread = Stacker(thread_id, title, sats, comments, datetime.datetime.now())
        self.session.add(thread)
        self.session.commit()

    def get_thread(self, thread_id: int) -> Stacker:
        """
        Get a thread from the database.
        :param thread_id: The thread id to get.
        """
        # for thread in self.session.query(Stacker).filter(Stacker.title == 'Hello World'):
        #     print(thread.thread_id, thread.title, thread.sats, thread.comments, thread.create_at)
        thread = self.session.query(Stacker).filter_by(thread_id=thread_id).first()
        return thread

    def del_thread(self, thread_id: int):
        """
        Delete a thread from the database.
        :param thread_id: The thread id to delete.
        """
        thread = self.get_thread(thread_id)
        if not thread:
            return
        self.session.delete(thread)
        self.session.commit()
