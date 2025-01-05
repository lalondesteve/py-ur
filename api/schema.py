from pydantic import BaseModel, ConfigDict
from pydantic.networks import IPvAnyAddress
from py_ur.modbus import RegisterEnum


class RobotConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    ip: IPvAnyAddress


class RobotConfigFromDb(RobotConfig):
    id: int


class RobotConfigUpdate(BaseModel):
    name: str
    ip: IPvAnyAddress


class RobotState(BaseModel):
    name: str
    id: int
    ip: IPvAnyAddress
    online: bool
    modbus_online: bool
    modbus_state: dict[RegisterEnum, int]
    dashboard_online: bool
    dashboard_state: dict[str, str]
