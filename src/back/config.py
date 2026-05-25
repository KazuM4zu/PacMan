import json
from typing import Tuple, Optional
from pydantic import BaseModel, ValidationError


class Config(BaseModel):
    score_file: str
    lvl_size: Tuple[int, int]
    lives: int
    nb_pacgum: int
    pt_per_pacgum: int
    pt_per_sppacgum: int
    pt_per_ghost: int
    seed: int
    lvl_max_time: int


def check_config_file(config_file):
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            data_config = json.load(f)
        valid_function = Config(**data_config)
        print("The config file is valid and loaded")
        return valid_function
    except FileNotFoundError:
        raise FileNotFoundError(f"'{config_file}' file was not found")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"'{config_file}' is not a valid JSON file")
    except ValidationError as e:
        raise ValueError(e)

    return None
