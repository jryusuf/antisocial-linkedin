from antisocial_backend.models.User import UserBase, UserCreate, UserRead, UserUpdate, DemoClass

class Person(DemoClass):

    def __init__(self, name:str, surname:str):
        self.super = super().__init__(name,surname)
    

