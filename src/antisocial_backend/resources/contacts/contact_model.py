from sqlmodel import SQLModel
from datetime import date
from pydantic import create_model
from antisocial_backend import Model

contact_model_design = create_model(
        "Note",
        __base__=SQLModel,
        name=(str, ...),
        email=(str, ...),
        phone=(str, ...)
    )

contacts = Model(contact_model_design,"contacts")
