#!/usr/bin/python3
"""Base Model Class"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()

class BaseModel:
    """BaseModel class"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize BaseModel"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in ["created_at", "updated_at"]:
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

    def __str__(self):
        """String representation"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def to_dict(self, save_fs=None):
        """Convert instance to dictionary"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].isoformat()
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].isoformat()
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if save_fs is None and "password" in new_dict:
            del new_dict["password"]
        return new_dict

    def save(self):
        """Save instance"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def delete(self):
        """Delete instance"""
        from models import storage
        storage.delete(self)
