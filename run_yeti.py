from typing import Any, Dict, Tuple

import argparse
import logging
import yaml

from code.Model import Model


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file", "-c",
                        help="The config.yaml file you want to use fo this model run. Default is './config.yaml'.",
                        dest="config_file",
                        default="./config.yaml",
                        type=str)
    parser.add_argument("--quiet", "-q",
                        help="Set this flag to print less info messages.",
                        dest="quiet",
                        action="store_true")

    config_file, quiet = parse_args(parser)
    config_dict = parse_config(config_file)
    set_logging_level(quiet)

    Model().run(config_dict, config_file)


def parse_args(parser: argparse.ArgumentParser) -> Tuple[str, bool]:

    args = parser.parse_args()
    config_file = args.config_file
    quiet = args.quiet
    return config_file, quiet


def set_logging_level(quiet: bool):

    if quiet is True:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')


def parse_config(config_file: str) -> Dict[str, Any]:

    with open(config_file, "r") as fp:
        config_dict = yaml.safe_load(fp)
    return config_dict


if __name__ == '__main__':
    main()
