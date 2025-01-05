import sqlalchemy
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)


class RobotConfigModel(BaseModel):
    __tablename__ = "robot_config"
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    ip = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
