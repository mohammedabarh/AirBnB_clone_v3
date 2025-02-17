#!/usr/bin/python3
"""File Storage Engine"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

classes = {
    'BaseModel': BaseModel,
    'User': User,
    'State': State,
    'City': City,
    'Place': Place,
    'Amenity': Amenity,
    'Review': Review
}

class FileStorage:
    """File Storage Class"""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns dictionary of objects"""
        if cls:
            if type(cls) == str:
                cls = classes.get(cls)
            return {k: v for k, v in self.__objects.items()
                    if isinstance(v, cls)}
        return self.__objects

    def new(self, obj):
        """Sets new obj in __objects"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to JSON file"""
        serialized = {}
        for key, obj in self.__objects.items():
            serialized[key] = obj.to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(serialized, f)

    def reload(self):
        """Deserializes JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    class_name = value['__class__']
                    obj = classes[class_name](**value)
                    self.__objects[key] = obj
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects"""
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """Call reload method"""
        self.reload()

    def get(self, cls, id):
        """Retrieve one object"""
        if cls and id:
            if type(cls) == str:
                cls = classes.get(cls)
            key = "{}.{}".format(cls.__name__, id)
            return self.__objects.get(key)
        return None

    def count(self, cls=None):
        """Count number of objects in storage"""
        if cls:
            if type(cls) == str:
                cls = classes.get(cls)
            return len([obj for obj in self.__objects.values()
                       if isinstance(obj, cls)])
        return len(self.__objects)
