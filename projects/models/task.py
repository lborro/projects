# -*- coding: utf-8 -*-
"""Task model."""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, JSON, String, Text
from sqlalchemy.sql import expression

from projects.database import Base
from projects.jupyter import read_parameters
from projects.utils import to_camel_case

DEFAULT_IMAGE = 'platiagro/platiagro-notebook-image:0.2.0'
DEFAULT_COMMANDS = ['sh', '-c']
DEFAULT_ARGUMENTS = ['''papermill $notebookPath output.ipynb -b $parameters;
                        status=$?;
                        bash save-dataset.sh;
                        bash save-figure.sh;
                        bash make-cells-read-only.sh
                        bash upload-to-jupyter.sh $experimentId $operatorId Experiment.ipynb;
                        exit $status''']


class Task(Base):
    __tablename__ = "tasks"
    uuid = Column(String(255), primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    image = Column(String(255), nullable=False, default=DEFAULT_IMAGE)
    commands = Column(JSON, nullable=False, default=DEFAULT_COMMANDS)
    arguments = Column(JSON, nullable=False, default=DEFAULT_ARGUMENTS)
    tags = Column(JSON, nullable=False, default=[])
    experiment_notebook_path = Column(String(255))
    deployment_notebook_path = Column(String(255), nullable=True)
    is_default = Column(Boolean, nullable=False, server_default=expression.false())
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.name}>"

    def as_dict(self):
        d = {to_camel_case(c.name): getattr(self, c.name) for c in self.__table__.columns}
        d["parameters"] = read_parameters(self.experiment_notebook_path)
        return d
