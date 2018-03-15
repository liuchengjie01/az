import logging.config

import yaml

from modules import adownloader
import config
from modules.entities.criteria import Criteria


def setup_logging():
    with open('logging.yaml') as f:
        logging.config.dictConfig(yaml.safe_load(f.read()))


def main():
    criteria = Criteria.init_from_dict(config.criteria)
    adownloader.run(config.input_file, config.base_url, config.key, config.number, criteria, out_dir=config.output_dir, metadata=config.metadata)


if __name__ == '__main__':
    setup_logging()
    main()
