from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import Depends,FastAPI, HTTPException, Query

app = FastAPI()

class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)
class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class HeroCreate(HeroBase):
    pass

class HeroRead(HeroBase):
    id: int

class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age:Optional[int] = None

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/heros/", response_model=HeroRead)
def create_hero(*,session: Session = Depends(get_session), hero: HeroCreate):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
    
@app.get("/heros/", response_model=list[Hero])
def read_heros(*,session: Session = Depends(get_session),offset: int = 0, limit:int = Query(default=100,le=100)):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    if not heroes:
        raise HTTPException(status_code=404, detail="No heroes found")
    return heroes

@app.get("/heros/{hero_id}", response_model=HeroRead)
def read_hero(*,session: Session = Depends(get_session),hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@app.patch("/heroes/{hero_id}", response_model=HeroRead)
def update_hero(*,session: Session = Depends(get_session),hero_id:int, hero:HeroUpdate):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404,detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    for key,value in hero_data.items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
    
@app.delete("/heroes/{hero_id}")
def delete_hero(*,session: Session = Depends(get_session),hero_id:int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}