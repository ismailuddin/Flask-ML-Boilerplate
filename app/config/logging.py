import logging
import logging.config
import yaml

with open("./app/config/logging.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
