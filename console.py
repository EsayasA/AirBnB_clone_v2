#!/usr/bin/python3
""" Console Module """
import sys
import cmd
from models.base_model import BaseModel
from models.__init__ import storage
from models.review import Review
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.user import User
from models.state import State

class HBNBCommand(cmd.Cmd):
    """ Command for th console"""

    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place, 'State': State,
               'City': City, 'Amenity': Amenity, 'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int, 'max_guest': int,
             'price_by_night': int, 'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Display if false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Command line for Adv.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''

        
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  
            pline = line[:]  

            
            _cls = pline[:pline.find('.')]

            
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                
                pline = pline.partition(', ')  

                
                _id = pline[0].replace('\"', '')
                
                pline = pline[2].strip()  
                if pline:
                    
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """show if it's false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Exit method"""
        exit()

    def help_quit(self):
        """ show for quit documentation  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ EOF """
        print()
        exit()

    def help_EOF(self):
        """ show help for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Emptyline method """
        pass

    def do_create(self, args):
        """ Object of class"""
        try:
            if not args:
                raise SyntaxError()
            arg_list = args.split(" ")
            kw = {}
            for arg in arg_list[1:]:
                arg_splited = arg.split("=")
                arg_splited[1] = eval(arg_splited[1])
                if type(arg_splited[1]) is str:
                    arg_splited[1] = arg_splited[1].replace("_", " ").replace('"', '\\"')
                kw[arg_splited[0]] = arg_splited[1]
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        new_instance = HBNBCommand.classes[arg_list[0]](**kw)
        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """ Information for create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Show method """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ info for show cmd """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ destroy object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ infor for destroy cmd """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ show all"""
        print_list = []

        if args:
            args = args.split(' ')[0]  
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage.all(HBNBCommand.classes[args]).items():
                print_list.append(str(v))
        else:
            for k, v in storage.all().items():
                print_list.append(str(v))
        print(print_list)

    def help_all(self):
        """ info for all cmd """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count class"""
        c = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                c += 1
        print(c)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ update method """
        c_name = c_id = att_name = att_val = kwargs = ''

        
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  
            print("** class doesn't exist **")
            return

        
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  
            print("** instance id missing **")
            return

        
        key = c_name + "." + c_id

        
        if key not in storage.all():
            print("** no instance found **")
            return

        
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  
            args = args[2]
            if args and args[0] == '\"':  
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            
            if not att_name and args[0] != ' ':
                att_name = args[0]
            
            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        
        new_dict = storage.all()[key]

        
        for i, att_name in enumerate(args):
            
            if (i % 2 == 0):
                att_val = args[i + 1]  
                if not att_name:  
                    print("** attribute name missing **")
                    return
                if not att_val:  
                    print("** value missing **")
                    return
                
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  

    def help_update(self):
        """ info for update """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
