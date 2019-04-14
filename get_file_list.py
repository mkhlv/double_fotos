# coding=utf-8

import re
import os
import fnmatch
import hashlib
import sys


def get_config_path():
    try:
        return sys.argv[2]
    except IndexError:
        return 'config'


def get_file_hash(file_name):
    with open(file_name, 'rb') as file:
        readfile = file.read()
        return hashlib.md5(readfile).hexdigest()


def check_names(work_folder, file_list_, file_type_):
    out_names = []
    file_names = [os.path.join(work_folder, file) for file in file_list_]
    up_pattern_list = fnmatch.filter(file_names, '*.{0}'.format(file_type_.upper()))
    lw_pattern_list = fnmatch.filter(file_names, '*.{0}'.format(file_type_.lower()))
    out_names.extend(up_pattern_list)
    out_names.extend(lw_pattern_list)
    return out_names


def get_folder_doubles(work_folder_, file_list_, log_file_name_):
    out = {}
    log_string = ('Checking folder "{0:60}" total files: {1}'.format(work_folder_, len(file_list_)))
    with open(log_file_name_, 'a') as log:
        log.write('{0}\n'.format(log_string))
    print(log_string)
    hash_dict = {}
    for file in file_list_:
        file_hash = get_file_hash(file)
        if hash_dict.get(file_hash) is None:
            hash_dict[file_hash] = [file]
        else:
            hash_dict.get(file_hash).append(file)
    for key in hash_dict.keys():
        value = hash_dict.get(key)
        if len(value) > 1:
            out.update({key: value})
    return out


def write_doubles(file_list_, out_file_name_):
    with open(out_file_name_, 'a') as file_out:
        file_out.writelines([key+':{0}\n'.format(value) for key in file_list_.keys() for value in file_list_.get(key)])


def folder_check(work_folder, file_list_, file_type_, out_file_name_, log_file_name_):
    file_list_ = check_names(work_folder, file_list_, file_type_)
    file_doubles = get_folder_doubles(work_folder, file_list_, log_file_name_)
    write_doubles(file_doubles, out_file_name_)


def delete_old_file(file_name):
    try:
        os.remove(file_name)
    except FileNotFoundError:
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
    work_folder = config.get('work_folder')
    file_type = config.get('file_type')
    delete_old_file(out_file_name)
    delete_old_file(log_file_name)
    for _ in os.walk(work_folder, topdown=True, onerror=None, followlinks=False):
        folder, sub_folders, file_list = _
        if len(file_list) > 0:
            folder_check(folder, file_list, file_type, out_file_name, log_file_name)


if __name__ == '__main__':
    config_path = get_config_path()
    main(config_path)
