from dataclasses import dataclass
from enum import StrEnum


class DashboardMessages(StrEnum):
    play = "play"
    stop = "stop"
    pause = "pause"
    load = "load"
    running = "running"
    robot_mode = "robotmode"
    safety_status = "safetystatus"
    power_on = "power on"
    power_off = "power off"
    breake_release = "break release"
    get_loaded_program = "get loaded program"
    shutdown = "shutdown"
    program_state = "programState"
    is_program_saved = "isProgramSaved"
    popup = "popup"
    close_popup = "close popup"
    set_operational_mode_manual = "set operational mode manual"
    set_operational_mode_automatic = "set operational mode automatic"
    clear_operational_mode = "clear operational mode"
    unlock_protective_stop = "unlock protective stop"
    close_safety_popup = "close safety popup"
    load_installation = "load installation"
    restart_safety = "restart safety"
    is_in_remote_control = "is in remote control"