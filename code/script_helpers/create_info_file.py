import os


def create_info_file(file: str, timestamp, mode, start_time, end_time, config_dict):

    info_text = get_info_text_by_mode(mode, timestamp, start_time, end_time, config_dict)
    with open(file, "w") as fp:
        fp.write(info_text)


def get_info_text_by_mode(mode, timestamp, start_time, end_time, config_dict):

    newline = "\n"

    pollutants = config_dict["pollutants"]
    strategy = config_dict["strategy"]
    load_input_data_function = config_dict["load_input_data_function"]
    load_unified_data_function = config_dict["load_unified_data_function"]
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
        f"unified data output folder: {config_dict.get('output_folder_for_unified_data')}\n"
        f"use nh3 tier 2 ef: {use_nh3_tier2_ef}\n"
        f"links to use: {links_to_use}\n"
        f"n traffic data rows used: {use_n_traffic_data_rows}\n"
        f"\n"
        f"mode: {mode}\n"
        f"strategy: {strategy}\n"
        f"load_input_data_function: {load_input_data_function}\n"
        f"load_unified_data_function: {load_unified_data_function}\n"
        f"validation_function: {validation_function}\n"
        f"\n"
    )
    if mode == 'unified_data':
        info_text = (
            f"{general_info_text}"
            f"files given:\n"
            f"{newline.join([os.path.abspath(location) for file, location in config_dict.items() if file.startswith('unified')])}\n"
        )
    elif mode == 'input_data':
        info_text = (
            f"{general_info_text}"
            f"input_data files given:"
            f"{newline.join([os.path.abspath(location) for file, location in config_dict.items() if file.startswith('input')])}\n"
            f"\n"
            f"unified_data files constructed during the model run:\n"
            f"{newline.join([os.path.abspath(location) for file, location in config_dict.items() if file.startswith('unified')])}\n"
        )
    else:
        raise RuntimeError(f"mode {mode} is not recognized. Please use 'unified_data' or 'input_data'.")

    return info_text
