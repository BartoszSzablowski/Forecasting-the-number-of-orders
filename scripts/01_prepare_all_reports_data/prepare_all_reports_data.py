import pandas as pd
import numpy as np
import glob


def prepare_data_frame(reports_list, sheet):
    data = pd.DataFrame()
    reports_names_components = []

    print("Number of reports: ", len(reports_list))
    print()
    for report in reports_list:
        print("Loading report ", report)
        W =  pd.read_excel(report, sheet_name = sheet, skip_blank_lines = False, header = None)
        data = data.append(W[[0]].T)
        reports_names_components.append(report.split("/")[-1].split("_"))

    year = get_reports_names_components(reports_names_components, 0)
    stage = get_reports_names_components(reports_names_components, 1)
    splitted_names_list = get_team_scenario_cycle(reports_names_components, 2)
    team = get_team(splitted_names_list)
    scenario = get_scenario(splitted_names_list)
    cycle = get_cycle(splitted_names_list)

    cols_dict = {"Year": year,
                "Stage": stage,
                "Team": team,
                "Scenario": scenario,
                "Cycle": cycle}

    data = insert_columns_from_dict(data, cols_dict)

    return data


def get_reports_names_components(reports_names_components, idx):
    return [el[idx] for el in reports_names_components]


def get_team_scenario_cycle(reports_names_components, idx):
    team_scenario_cycle = get_reports_names_components(reports_names_components, idx)
    return [el.split(".")[0] for el in team_scenario_cycle]


def get_team(splitted_names_list):
    return [el[:-3] for el in splitted_names_list]


def get_scenario(splitted_names_list):
    return [el[-2] for el in splitted_names_list]


def get_cycle(splitted_names_list):
    return [el[-1] for el in splitted_names_list]


def insert_columns_from_dict(df, cols_dict):
    for el in enumerate(cols_dict):
        key = el[1]
        df.insert(loc = el[0], column = key, value = cols_dict[key])
    return df



if __name__ == "__main__":
    reports_list = glob.glob("././datasets/01_reports/*.xlsx")
    reports_list.sort()
    sheet = "W"
    data = prepare_data_frame(reports_list, sheet)
    data.to_csv("././datasets/02_all_reports_data/all_reports_data.csv", index = False)
    print("\nTask done correctly")
