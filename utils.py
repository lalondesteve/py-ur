import yaml


def get_ursim_ip():
    try:
        with open("config.yaml", "r") as f:
            conf = yaml.safe_load(f)
    except Exception:
        return "100.82.150.95"
    return conf["ursim_ip"]
