#!/usr/bin/python3
"""Database storage engine"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity

classes = {
    'User': User,
    'State': State,
    'City': City,
    'Place': Place,
    'Review': Review,
    'Amenity': Amenity
}

class DBStorage:
    """Database Storage Class"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the database storage"""
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                    .format(user, pwd, host, db),
                                    pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects depending on the class"""
        objects = {}
        if cls:
            if type(cls) == str:
                cls = classes.get(cls)
            query = self.__session.query(cls)
            for obj in query:
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                objects[key] = obj
        else:
            for cls in classes.values():
                query = self.__session.query(cls)
                for obj in query:
                    key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Add object to current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit changes to database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in database and session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                     expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the session"""
        self.__session.close()

    def get(self, cls, id):
        """Retrieve one object"""
        if cls and id:
            if type(cls) == str:
                cls = classes.get(cls)
            obj = self.__session.query(cls).filter(cls.id == id).first()
            return obj
        return None

    def count(self, cls=None):
        """Count number of objects in storage"""
        if cls:
            if type(cls) == str:
                cls = classes.get(cls)
            return self.__session.query(cls).count()
        count = 0
        for cls in classes.values():
            count += self.__session.query(cls).count()
        return count
