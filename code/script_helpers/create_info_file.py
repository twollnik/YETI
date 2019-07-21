import os


def create_info_file(file: str, timestamp, mode, start_time, end_time, config_dict):

    newline = "\n"

    pollutants = config_dict["pollutants"]
    strategy = config_dict["strategy"]
    load_berlin_format_data_function = config_dict["load_berlin_format_data_function"]
    load_yeti_format_data_function = config_dict["load_yeti_format_data_function"]
    output_folder = config_dict["output_folder"]
    mode = config_dict["mode"]
    use_nh3_tier2_ef = config_dict.get("use_nh3_tier2_ef")
    validation_function = config_dict.get("validation_function")
    links_to_use = config_dict.get("links_to_use", [])
    use_n_traffic_data_rows = config_dict.get("use_n_traffic_data_rows")

    general_info_text = (
        f"# This file contains information about the model run that produced the files in this directory.\n"
        "\n"
        f"time of run: {timestamp}\n"
        f"duration of run: {(end_time - start_time) / 60} min\n"
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
        f"\n"
    )
    if mode == 'yeti_format':
        info_text = (
            f"{general_info_text}"
            f"files given:\n"
            f"{newline.join([os.path.abspath(location) for file, location in config_dict.items() if file.startswith('yeti_format')])}\n"
        )
    elif mode == 'berlin_format':
        info_text = (
            f"{general_info_text}"
            f"files in berlin_format given:"
            f"{newline.join([os.path.abspath(location) for file, location in config_dict.items() if file.startswith('berlin')])}\n"
            f"\n"
            f"files in yeti_format constructed during the model run:\n"
            f"{newline.join([os.path.abspath(location) for file, location in config_dict.items() if file.startswith('yeti_format')])}\n"
        )
    else:
        raise RuntimeError(f"mode {mode} is not recognized. Please use 'yeti_format' or 'berlin_format'.")

    with open(file, "w") as fp:
        fp.write(info_text)