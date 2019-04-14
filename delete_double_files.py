import os
import sys
import re


def get_config_path():
    try:
        return sys.argv[2]
    except IndexError:
        return 'config'


def get_data_from_file(file_name):
    out_dict = {}
    with open(file_name, 'r') as file_data:
        for row in [_.replace('\n', '') for _ in file_data.readlines()]:
            file_hash, file_path = row.split(':')
            if file_hash not in out_dict.keys():
                out_dict.update({file_hash: [file_path]})
            else:
                out_dict.get(file_hash).append(file_path)
    return out_dict


def get_remove_scope(data_from_file_):
    return [_[0] for _ in sorted(data_from_file_.values(), reverse=True)]


def delete_file(file_name, log_file_name_):
    log_string = ('Deleting {0}'.format(file_name))
    with open(log_file_name_, 'a') as log:
        log.write('{0}\n'.format(log_string))
    print(log_string)
    try:
        os.remove(file_name)
    except NameError:
        pass


def get_config(config_path_):
    try:
        with open(config_path_, 'r') as file:
            config = ({_.split(';')[0].strip(): _.split(';')[1].replace('\n', '').strip() for _ in file.readlines()
                       if re.search(';', _)})
            return config
    except NameError:
        return None


def main(config_path_):
    config = get_config(config_path_)
    assert config is not None, 'config is None, check config'
    out_file_name = config.get('out_file_name')
    log_file_name = config.get('log_file_name')
    data_from_file = get_data_from_file(file_name=out_file_name)
    files_to_delete = get_remove_scope(data_from_file)
    for _ in files_to_delete:
        delete_file(_, log_file_name)


if __name__ == '__main__':
    config_path = get_config_path()
    main(config_path)
