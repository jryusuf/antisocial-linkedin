from antisocial_backend.dependencies.dependencies import Session,get_session
from fastapi import Depends
from antisocial_backend.dependencies.model import Model
from sqlmodel import select


class Crud():
    def __init__(self,model:Model):
        self.model = model

    def create(session:Session , data, model = Model):
        db_data = model.Table.model_validate(data)
        session.add(db_data)
        session.commit()
        session.refresh(db_data)
        return db_data
    
    def reads(self):
        return self.session.exec(select(self.model.Table)).all()

    def read(self, id:int):
        return self.session.get(self.model.Table, id)

    def delete(self, id:int)->bool:
        """ db_data = self.session.get(self.model.Table, id)
        if not db_data:
            return False
        self.session.delete(db_data)
        self.session.commit() """
        return True

    def update(self, id:int, data):
        """ db_data = self.session.get(Model.Table,id)
        if not db_data:
            return None
        data = data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(db_data, key, value)
        self.session.add(db_data)
        self.session.commit()
        self.session.refresh(db_data)
        return db_data  """
        pass   