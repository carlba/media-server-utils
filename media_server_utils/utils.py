import logging
from pathlib import Path

from dotenv import load_dotenv


def configure_logging(name: str) -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(name)


def load_environment():
    env_path_home = Path(Path.home()) / '.env'
    env_path_current_dir = Path('.') / '.env'
    load_dotenv(env_path_home)
    load_dotenv(env_path_current_dir)
