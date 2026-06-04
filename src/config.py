import json
from pydantic import BaseModel, ValidationError, Field
from pydantic import NonNegativeInt, PositiveInt


class LevelModel(BaseModel):
    width: int = Field(ge=10, le=46)
    height: int = Field(ge=10, le=46)
    nb_pacgum: NonNegativeInt


class Config(BaseModel):
    score_file: str
    level: list[LevelModel]
    lives: NonNegativeInt
    nb_pacgum: NonNegativeInt
    pt_per_pacgum: NonNegativeInt
    pt_per_super_pacgum: NonNegativeInt
    pt_per_ghost: NonNegativeInt
    lvl_max_time: PositiveInt
    seed: PositiveInt
    volume: int = Field(ge=0, le=100)
    cheats_enabled: bool

    def save(self, path: str = "config.json") -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.model_dump(), f, ensure_ascii=False, indent=4)


def check_config_file(config_file):
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            data_config = json.load(f)
        valid_function = Config(**data_config)
        # print("The config file is valid and loaded")
        return valid_function
    except FileNotFoundError:
        raise FileNotFoundError(f"'{config_file}' file was not found")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"'{config_file}' is not a valid JSON file")
    except ValidationError as e:
        raise ValueError(e)

    return None
