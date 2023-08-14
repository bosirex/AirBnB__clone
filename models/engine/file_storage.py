#!/usr/bin/python3
"""FileStorage class."""

# imported modules
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """storage engine representation.

    Attributes:
        __file_path (str): file name for saving objects.
        __objects (dict): instantiated objects dictionary.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        obj_class_name = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(obj_class_name, obj.id)] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)."""
        o_dict = FileStorage.__objects
        object_dict = {obj: o_dict[obj].to_dict() for obj in o_dict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(object_dict, f)

    def reload(self):
        """deserializes the JSON file to __objects (only if the JSON file (__file_path) exists ; 
        otherwise, do nothing. If the file doesn’t exist, no exception should be raised)."""
        try:
            with open(FileStorage.__file_path) as f:
                object_dict = json.load(f)
                for o in object_dict.values():
                    clss_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(clss_name)(**o))
        except FileNotFoundError:
            raise FileNotFoundError("File not found: {}".format(FileStorage.__file_path))
