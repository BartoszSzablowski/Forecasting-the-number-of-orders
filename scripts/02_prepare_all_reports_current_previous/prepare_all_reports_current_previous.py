import pandas as pd
import numpy as np


def prepare_data_previous(data_current):
    data_previous = pd.DataFrame(columns = data_current.columns)
    n_col = data_current.shape[1]

    for index, row in data_current.iterrows():
        if row.Team == "Historia" and row.Cycle == 0:
            new_row = np.repeat("None", n_col, axis = 0)
            data_previous.loc[index] = new_row
        elif row.Cycle == 5:
            new_row = data_current.loc[(data_current["Scenario"] == row.Scenario) & (data_current["Team"] == "Historia") & (data_current["Cycle"] == 4)]
            data_previous = data_previous.append(new_row)
        else:
            new_row = data_current.loc[(data_current["Scenario"] == row.Scenario) & (data_current["Team"] == row.Team) & (data_current["Cycle"] == row.Cycle - 1) & (data_current["Stage"] == row.Stage)]
            data_previous = data_previous.append(new_row)
        
    data_previous = data_previous.reset_index(drop = True)
    data_previous = data_previous.drop(columns = ["Scenario"])
    data_previous.columns = [x + "_p" for x in data_previous.columns.values]

    return data_previous


if __name__ == "__main__":
    data_current = pd.read_csv("././datasets/02_all_reports_data/all_reports_data.csv")
    data_current = data_current.sort_values(by = ["Scenario", "Cycle", "Team"]).reset_index(drop = True)
    data_previous = prepare_data_previous(data_current)
    data_current.columns = [x + "_c" if x != "Scenario" else x for x in data_current.columns.values]
    data = pd.merge(data_current, data_previous, right_index = True, left_index = True)
    data.to_csv("././datasets/03_all_reports_data_current_previous/all_reports_data_current_previous.csv", index = False)
    print("Task done correctly")
