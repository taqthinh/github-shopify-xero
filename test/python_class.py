
class Person:
    # thuoc tinh
    name_abc = 'Abc'
    staff = None

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __del__(self):
        print("Da HUY")
        del self.name, self.age, self.gender

    #phuong thuc
    def get_name1(self):
        return self.name_abc
    def get_name(self):
        return self.name
    def get_age(self):
        return self.age
    def get_gender(self):
        return self.gender

    def is_staff(self):
        return self.staff

class Staff(Person):

    staff = True

    def __del__(self):
        print("Da HUY 2")
        del self.name, self.age, self.gender

person2 = Person('Thinh', 22, 'FeMale')
print(person2.get_name())
print(person2.get_age())
print(person2.get_gender())
print(person2.get_name1())
print(person2.name_abc)
print("===============================")
person3 = Staff('Thinh123', 22123, 'Male')
print(person3.get_name())
print(person3.get_age())
print(person3.is_staff())
print(person3.get_name1())
print(person3.name_abc)
