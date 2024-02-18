from sqlmodel import SQLModel
from datetime import date
from pydantic import create_model
from antisocial_backend import Model

roadmap_model_design = create_model(
        "Note",
        __base__=SQLModel,
        name=(str, ...),
        description=(str, ...),
        start_date=(date, ...)
    )

roadmaps = Model(roadmap_model_design,"roadmaps")
