def drop_keys_starting_with(starting_chars, dict):
    return {key: value for key, value in dict.items() if not key.startswith(starting_chars)}


def remove_prefix_from_keys(prefix, dict):
    for key, value in list(dict.items()):
        if key.startswith(prefix):
            del dict[key]
            dict[key[len(prefix):]] = value
    return dict


def add_prefix_to_keys(prefix, paths_to_cold_yeti_format_data):

    return {f"{prefix}_{key}": value for key, value in list(paths_to_cold_yeti_format_data.items())}