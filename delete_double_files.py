import os


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


def delete_file(file_name):
    print('Deleting {0}'.format(file_name))
    try:
        os.remove(file_name)
    except FileNotFoundError:
        pass


data_from_file = get_data_from_file(file_name='out.txt')
files_to_delete = get_remove_scope(data_from_file)
list(map(delete_file, files_to_delete))
