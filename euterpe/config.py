import os
import sys
from pathlib import Path
from typing import Optional
import configparser
import pydantic
from pydantic import BaseModel, Field, IPvAnyAddress, Extra

from euterpe.logger import config as logger

_config: dict = None


class ConfigBaseModel(BaseModel):
    __slots__ = ()

    class Config(object):
        extra = Extra.ignore


class StorageConfig(ConfigBaseModel):
    __slots__ = ()
    data_dir: Path
    index_file: Path
    samples_dir: Path


class ServerConfig(ConfigBaseModel):
    __slots__ = ()
    address: IPvAnyAddress
    port: int = Field(
        min=0,
        max=(1 >> 16) - 1
    )


class Config(ConfigBaseModel):
    __slots__ = ()

    storage: StorageConfig
    server: ServerConfig


def get_config(config_path: Optional[Path] = None) -> Config:
    global _config
    if _config is None:
        _init(config_path)
    return _config


_CONFIG_PATHS = []

if (_platform := sys.platform) == "linux":
    _CONFIG_ROOT = os.environ.get(
        "XDG_CONFIG_HOME",
        Path.home().joinpath(".config/")
    )
    _CONFIG_PATHS.append(os.path.join(_CONFIG_ROOT, "euterpe.conf"))

    _CONFIG_PATHS.append(Path("/etc/euterpe.conf"))

else:
    pass


def _parser_to_dict(parser: configparser.ConfigParser) -> dict:
    return dict((k, dict(v)) for k, v in parser.items() if k != "DEFAULT")


def _init(config_path: Optional[Path] = None) -> None:
    global _config
    parser = configparser.ConfigParser()
    paths = _CONFIG_PATHS
    if config_path is not None:
        paths = [config_path] + paths

    found = False
    for path in paths:
        try:
            parser.read_file(open(path, "r"))
        except FileNotFoundError:
            continue
        found = True
        try:
            _config = Config.parse_obj(_parser_to_dict(parser))
            logger.info(f"Using config \"{path}\"")
            break
        except (configparser.Error, pydantic.ValidationError) as e:
            logger.error(f"Config file at \"{path}\" contains errors: {e}")
            exit(1)
    if not found:
        logger.error(f"No config file was found. Locations checked: {paths}")
