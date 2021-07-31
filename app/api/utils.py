def lod_to_dict(lod):
    new_dict = dict()
    for item in lod:
        new_dict[item['id']] = {key: value for key, value in item.items() if key != 'id'}
    return new_dict


def dict_to_lod(_dict):
    lod = list()
    for key in _dict.keys():
        actual_dict = {'id': key}
        actual_dict.update(_dict[key])
        lod.append(actual_dict)
    return lod
