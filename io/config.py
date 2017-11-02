import yaml
import os


def import_yaml_files(base_dir):
    with open(os.path.join("..", "constants.yaml"), 'r') as ymlfile:
        constants = yaml.load(ymlfile)
    return constants