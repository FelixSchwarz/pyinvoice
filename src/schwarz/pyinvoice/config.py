
from configparser import ConfigParser
import os
from pathlib import Path
from typing import Union


__all__ = ['parse_config']

def parse_config(cfg_path: Union[os.PathLike, str]) -> dict:
    cfg_parser = ConfigParser()
    cfg_parser.read(cfg_path)
    config = dict(cfg_parser['pyinvoice'])

    path_template = Path(config['template'])
    if not path_template.is_absolute():
        cfg_dir = Path(cfg_path).parent
        path_template = (cfg_dir / path_template).absolute()
        config['template'] = str(path_template)
    return config

