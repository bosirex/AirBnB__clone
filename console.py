#!/usr/bin/python3

"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curlybraces = re.search(r"\{(.*?)\}", arg)
    _brackets = re.search(r"\[(.*?)\]", arg)
    if curlybraces is None:
        if _brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            _lexer = split(arg[:_brackets.span()[0]])
            _retl = [i.strip(",") for i in _lexer]
            _retl.append(_brackets.group())
            return _retl
    else:
        _lexer = split(arg[:curlybraces.span()[0]])
        _retl = [i.strip(",") for i in _lexer]
        _retl.append(curlybraces.group())
        return _retl


class HBNBCommand(cmd.Cmd):
    """HBNB command interpreter.
    Attributes:
        prompt: command prompt.
    """

    custom_prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "Place",
        "Amenity",
        "Review"
    }

    def empty_line(self):
        """Do nothing on receiving an empty line."""
        pass

    def default(self, arg):
        """invalid input default behavior """
        argument_dict = {
            "all": self.all,
            "show": self.show,
            "destroy": self.destroy,
            "count": self.count,
            "update": self.update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argument1 = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argument1[1])
            if match is not None:
                command = [argument1[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argument_dict.keys():
                    call = "{} {}".format(argument1[0], command[1])
                    return argument_dict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def quit(self, arg):
        """exit the program."""
        return True

    def EOF(self, arg):
        """exit the program."""
        print("")
        return True

    def create(self, arg):
        """
         Creates a new instance of BaseModel.
        """
        argument1 = parse(arg)
        if len(argument1) == 0:
            print("** class name missing **")
        elif argument1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argument1[0])().id)
            storage.save()

    def show(self, arg):
        """Prints the string representation of an instance based on the class name and id.
        """
        argument1 = parse(arg)
        object_dict = storage.all()
        if len(argument1) == 0:
            print("** class name missing **")
        elif argument1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argument1) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argument1[0], argument1[1]) not in object_dict:
            print("** no instance found **")
        else:
            print(object_dict["{}.{}".format(argument1[0], argument1[1])])

    def destroy(self, arg):
        """Deletes an instance based on the class name and id."""
        argument1 = parse(arg)
        object_dict = storage.all()
        if len(argument1) == 0:
            print("** class name missing **")
        elif argument1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argument1) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argument1[0], argument1[1]) not in object_dict.keys():
            print("** no instance found **")
        else:
            del object_dict["{}.{}".format(argument1[0], argument1[1])]
            storage.save()

    def all(self, arg):
        """Prints all string representation of all instances based or not on the class name."""
        argument1 = parse(arg)
        if len(argument1) > 0 and argument1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            object1 = []
            for obj in storage.all().values():
                if len(argument1) > 0 and argument1[0] == obj.__class__.__name__:
                    object1.append(obj.__str__())
                elif len(argument1) == 0:
                    object1.append(obj.__str__())
            print(object1)

    def count(self, arg):
        """
        Retrieves number of instances of a given class."""
        argument1 = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argument1[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def update(self, arg):
        """Update a class instance of a given id by adding or updating
            a given attribute key/value pair or dictionary. """

        argument1 = parse(arg)
        object_dict = storage.all()

        if len(argument1) == 0:
            print("** class name missing **")
            return False
        if argument1[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argument1) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argument1[0], argument1[1]) not in object_dict.keys():
            print("** no instance found **")
            return False
        if len(argument1) == 2:
            print("** attribute name missing **")
            return False
        if len(argument1) == 3 and not isinstance(eval(argument1[2]), dict):
            print("** value missing **")
            return False

        if len(argument1) == 4:
            obj = object_dict["{}.{}".format(argument1[0], argument1[1])]
            if argument1[2] in obj.__class__.__dict__.keys():
                val_type = type(obj.__class__.__dict__[argument1[2]])
                obj.__dict__[argument1[2]] = val_type(argument1[3])
            else:
                obj.__dict__[argument1[2]] = argument1[3]
        elif isinstance(eval(argument1[2]), dict):
            obj = object_dict["{}.{}".format(argument1[0], argument1[1])]
            for j, n in eval(argument1[2]).items():
                if (j in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[j]) in {str, int, float}):
                    val_type = type(obj.__class__.__dict__[j])
                    obj.__dict__[j] = val_type(n)
                else:
                    obj.__dict__[j] = n
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
