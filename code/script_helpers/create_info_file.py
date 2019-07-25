import os


def create_info_file(output_file, timestamp, duration, config_dict, config_file, yeti_format_file_locations):

    mode = config_dict["mode"]

    general_info_text = get_general_info_text(config_dict, duration, mode, timestamp)
    file_locations_text = get_file_locations_text(config_dict, mode, yeti_format_file_locations)
    whole_config_text = get_config_file_text(config_file)

    info_text = (f"# This file contains information about the model run that produced the files in this directory.\n"
                 f"\n"
                 f"General Info:\n"
                 f"=============\n"
                 f"{general_info_text}\n"
                 f"\n"
                 f"File Locations:\n"
                 f"===============\n"
                 f"{file_locations_text}\n"
                 f"\n"
                 f"Contents of the config file used:\n"
                 f"=================================\n"
                 f"{whole_config_text}")

    with open(output_file, "w") as fp:
        fp.write(info_text)


def get_general_info_text(config_dict, duration, mode, timestamp):

    pollutants = config_dict["pollutants"]
    strategy = config_dict["strategy"]
    load_berlin_format_data_function = config_dict["load_berlin_format_data_function"]
    load_yeti_format_data_function = config_dict["load_yeti_format_data_function"]
    output_folder = config_dict["output_folder"]
    use_nh3_tier2_ef = config_dict.get("use_nh3_tier2_ef")
    validation_function = config_dict.get("validation_function")
    links_to_use = config_dict.get("links_to_use", [])
    use_n_traffic_data_rows = config_dict.get("use_n_traffic_data_rows")

    general_info_text = (
        f"time of run: {timestamp}\n"
        f"duration of run: {duration / 60} min\n"
        f"pollutants: {pollutants}\n"
        f"output folder: {output_folder}\n"
        f"yeti_format data output folder: {config_dict.get('output_folder_for_yeti_format_data')}\n"
        f"use nh3 tier 2 ef: {use_nh3_tier2_ef}\n"
        f"links to use: {links_to_use}\n"
        f"n traffic data rows used: {use_n_traffic_data_rows}\n"
        f"\n"
        f"mode: {mode}\n"
        f"strategy: {strategy}\n"
        f"load_berlin_format_data_function: {load_berlin_format_data_function}\n"
        f"load_yeti_format_data_function: {load_yeti_format_data_function}\n"
        f"validation_function: {validation_function}\n"
    )
    return general_info_text


def get_file_locations_text(config_dict, mode, yeti_format_file_locations):

    newline = "\n"  # make '\n' usable for join operations in f-Strings

    if mode == 'yeti_format':
        info_text = (
            f"files given:\n"
            f"{newline.join([os.path.abspath(location) for file, location in config_dict.items() if file.startswith('yeti_format')])}\n"
        )
    elif mode == 'berlin_format':
        info_text = (
            f"files in berlin_format given:"
            f"{newline.join([os.path.abspath(location) for file, location in config_dict.items() if file.startswith('berlin')])}\n"
            f"\n"
            f"files in yeti_format constructed during the model run:\n"
            f"{newline.join([os.path.abspath(location) for file, location in yeti_format_file_locations.items()])}\n"
        )
    else:
        raise RuntimeError(f"mode {mode} is not recognized. Please use 'yeti_format' or 'berlin_format'.")

    return info_text


def get_config_file_text(config_file):

    with open(config_file) as fp:
        config_contents = fp.read()
    config_contents = config_contents.replace("\n", "\n\t")
    config_contents = f"\t{config_contents}"
    return config_contents
