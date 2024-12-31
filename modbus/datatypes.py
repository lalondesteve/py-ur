from enum import IntEnum
from typing import Protocol


class Action(IntEnum):
    READ = 3
    WRITE = 6


class StatusRegister(IntEnum):
    robotMode = 258
    isPowerOnRobot = 260
    isSecurityStopped = 261
    isEmergencyStopped = 262
    isTeachButtonPressed = 263
    isPowerButtonPressed = 264
    isSafetySignalSuchThatWeShouldStop = 265
    safetyMode = 266


register_dict = {f"register_{i}": i for i in range(128, 255)}

GeneralPurposeRegister = IntEnum("GeneralPurposeRegister", register_dict)  # pyright: ignore


class Register(Protocol):
    name: str
    value: int
