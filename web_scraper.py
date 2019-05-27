class table():
    dict = {}
    id = 0

    def __init__(self, *args):
        for key in args:
            self.__dict__[key] = ""

    def insert(self, **kwargs):
        if self.validate(kwargs):
            table_row = {}
            for key, value in kwargs.items():
                table_row[key] = value
            self.__class__.dict[self.__class__.id] = table_row
            self.__class__.id += 1;
            return True
        else:
            return False


    def validate(self, kwargs):
        if (len(self.__dict__) != len(kwargs)):
            return False
        for key, value in kwargs.items():
            if key not in self.__dict__:
                print("{} not valid column. cannot add row {}".format(key, kwargs))
                return False
        return True

    def delete(self, args):
        
    def query(self, string):
        string = string.strip()
        words = string.split()

        if words[0] != "SELECT":
            print("invalid syntax for query")
            return False
        if words[1] == "*":
            if words[-1] == "*":
                for row in self.dict.values():
                    for key, value in row.items():
                        print("{} = {}, ".format(key, value), end="")
                    print()
                return
            if words[2] != "WHERE":
                print("invalid syntax for query")
                return False
            if words[3] not in self.__dict__:
                print("{} is not a valid attribute of this table".format(words[3]))
                return False
            if type(self.dict[0][words[3]]) != type(words[5]):
                words[5] = type(self.dict[0][words[3]])(words[5])
            if words[4] != "==" and words[4] != "!=":
                print("invalid syntax for query")
                return False
            else:
                if words[4] == "==":
                    for row in self.dict.values():
                        if row[words[3]] == words[5]:
                            for key, value in row.items():
                                print("{} = {}, ".format(key, value), end="")
                            print()
                else:
                    for row in self.dict.values():
                        if row[words[3]] != words[5]:
                            for key, value in row.items():
                                print("{} = {}, ".format(key, value), end="")
                            print()
        else:

class validator
        
def main():
    while(true):
        user_input = input("\n")
        if 
        var.query(user_input)

if __name__ == '__main__':
    main()
