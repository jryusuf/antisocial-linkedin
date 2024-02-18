from sqlmodel import SQLModel
from datetime import date
from pydantic import create_model
from antisocial_backend import Model

event_model_design = create_model(
    "Event",
    __base__=SQLModel,
    name=(str, ...),
    location=(str, ...),
    organizer=(str, ...),
    date=(date,...)
)

events = Model(event_model_design,"events")
