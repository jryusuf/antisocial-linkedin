from sqlmodel import SQLModel
from datetime import datetime
from pydantic import create_model
from antisocial_backend import Model

note_model_design = create_model(
        "Note",
        __base__=SQLModel,
        name=(str, ...),
        description=(str, ...),
        start_date=(datetime, ...)
    )

notes = Model(note_model_design,"notes")
