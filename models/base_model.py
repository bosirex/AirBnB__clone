#!/usr/bin/python3
"""Defines the BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime

class BaseModel:
    """HBnB project BaseModel Class ."""

    def __init__(self, *args, **kwargs):
        """new BaseModel Initialization.

        Args:
            *args (any): not used.
            **kwargs (dict): attributes' Key/values .
        """
        to_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for j, m in kwargs.items():
                if j == "created_at" or j == "updated_at":
                    self.__dict__[j] = datetime.strptime(m, to_format)
                else:
                    self.__dict__[j] = m
        else:
            models.storage.new(self)

    def save(self):
        """updated_at is updated with the current datetime and the instance saved."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of __dict__ of the instance."""
        r_dict = self.__dict__.copy()
        r_dict["created_at"] = self.created_at.isoformat()
        r_dict["updated_at"] = self.updated_at.isoformat()
        r_dict["__class__"] = self.__class__.__name__
        return r_dict

    def __str__(self):
        """ should print: [<class name>] (<self.id>) <self.__dict__>."""
        cl_name = self.__class__.__name__
        return "[{}] ({}) {}".format(cl_name, self.id, self.__dict__)
