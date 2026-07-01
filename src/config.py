import json
from pydantic import BaseModel, ValidationError, Field
from pydantic import NonNegativeInt, PositiveInt
from typing import Any


class LevelModel(BaseModel):
    """Validate the dimensions and pac-gum count for one level definition."""

    width: int = Field(ge=10, le=46)
    height: int = Field(ge=10, le=46)
    nb_pacgum: NonNegativeInt


class Config(BaseModel):
    """Validate the full game configuration payload."""

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
        """Persist the current configuration to disk.

        Args:
            path: File path where the configuration should be written.
        """
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.model_dump(), f, ensure_ascii=False, indent=4)


def check_config_file(config_file: Any) -> Config:
    """Load and validate the game configuration from a JSON file.

    Args:
        config_file: Path or file-like object containing the configuration.

    Returns:
        A validated Config instance.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If the JSON payload is invalid.
    """
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            data_config = json.load(f)
        valid_function = Config(**data_config)
        return valid_function
    except FileNotFoundError:
        raise FileNotFoundError(f"'{config_file}' file was not found")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"'{config_file}' is not a valid JSON file",
            e.doc,
            e.pos,
        ) from e
    except ValidationError as e:
        raise ValueError(e)

    return None
