import yaml


def get_ursim_ip():
    try:
        with open("config.yaml", "r") as f:
            conf = yaml.safe_load(f)
    except Exception:
        return "127.0.0.1"
    return conf["ursim_ip"]
