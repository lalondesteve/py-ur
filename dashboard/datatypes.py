from enum import StrEnum


class DashboardActionMessages(StrEnum):
    play = "play"
    stop = "stop"
    pause = "pause"
    # load = "load"
    power_on = "power on"
    power_off = "power off"
    brake_release = "brake release"
    shutdown = "shutdown"
    # popup = "popup"
    # close_popup = "close popup"
    set_operational_mode_manual = "set operational mode manual"
    set_operational_mode_automatic = "set operational mode automatic"
    clear_operational_mode = "clear operational mode"
    unlock_protective_stop = "unlock protective stop"
    close_safety_popup = "close safety popup"
    load_installation = "load installation"
    restart_safety = "restart safety"


class DashboardStatusMessages(StrEnum):
    robot_mode = "robotmode"
    running = "running"

    is_in_remote_control = "is in remote control"
    is_program_saved = "isProgramSaved"
    program_state = "programState"
    get_loaded_program = "get loaded program"
    safety_status = "safetystatus"
