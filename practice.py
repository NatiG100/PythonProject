
    
class Person:
    name = "unknown"
    def __init__(self,name,age, friend=None):
        self.name = name
        self.age = age
        self.friend = friend
    def sayHi(self):
        print("Hi, I am ", self.name, " and I am ",self.age," years old.")
    def friendsName(self):
        if self.friend!=None:
            print(self.friend.name)
        else:
            print("I have no friend")
        



abebe = Person("Abebe", 22)
kebede = Person("Kebede", 55,abebe)


abebe.friendsName()
kebede.friendsName()

