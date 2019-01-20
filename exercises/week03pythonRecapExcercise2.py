class Student:
    def __init__(self):
        print "Student Manager 2019 by Hannu Oksman"
        while(True):
            operation = raw_input("add, delete, edit or print: ")
            self.operate(operation)

    def operate(self,operation):
        if operation == "add":
            self.students.append(raw_input("enter new student's name: "))
        elif operation == "delete":
            while(True):
                self.listStudents()
                selection = int(raw_input("delete student #: "))
                try:
                    self.students.pop(selection)
                    break
                except IndexError:
                    print "invalid index, try again"
        elif operation == "edit":
            self.listStudents()
            selection = int(raw_input("edit student #: "))
            newName = raw_input("new name of the student: ")
            try:
                self.students[selection] = newName
                print "the new name is" , newName
            except IndexError:
                print "invalid index"
        elif operation == "print":
            for s in self.students:
                print s

    def listStudents(self):
        ind = 0
        for s in self.students:
            print ind,s
            ind += 1

    students = []

try:
    s = Student()
except KeyboardInterrupt:
    print "exiting"

''' example output
Student Manager 2019 by Hannu Oksman
add, delete, edit or print: add
enter new student's name: hannu
add, delete, edit or print: add
enter new student's name: add
add, delete, edit or print: add
enter new student's name: delete
add, delete, edit or print: add
enter new student's name: edit
add, delete, edit or print: add
enter new student's name: print
add, delete, edit or print: print
hannu
add
delete
edit
print
add, delete, edit or print: delete
0 hannu
1 add
2 delete
3 edit
4 print
delete student #: 2
add, delete, edit or print: edit
0 hannu
1 add
2 edit
3 print
edit student #: 2
new name of the student: manager
the new name is manager
add, delete, edit or print: print
hannu
add
manager
print
add, delete, edit or print: 
exiting
>>> 
'''
