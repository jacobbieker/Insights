import yaml
import os


def import_yaml_files(base_dir, list_of_file_names):
    '''
    Imports yaml files from a base directory
    :param base_dir:
    :param list_of_file_names:
    :return:
    '''
    output_list = []
    for element in list_of_file_names:
        with open(os.path.join(base_dir, list_of_file_names), 'r') as ymlfile:
            yaml_output = yaml.safe_load(ymlfile)
            output_list.append(yaml_output)
    return output_list
