import pandas as pd
import numpy as np
import itertools

from dict_parser import DictParser
from demand_dataset import DemandDataset


if __name__ == "__main__":
    input_data = pd.read_csv("././datasets/03_all_reports_data_current_previous/all_reports_data_current_previous.csv")

    prodx_list = ["Prod1", "Prod2", "Prod3"]
    area_list = ["Europe", "Nafta", "Internet"]
    prodx_area_list = list(itertools.product(*[prodx_list, area_list]))

    dict_file = "./scripts/03_prepare_demand_datasets/configs/dict.txt"
    factors_columns_dict = DictParser(dict_file)
    
    for el in prodx_area_list:
        print(el)
        demand_dataset = DemandDataset(input_data, el[0], el[1], factors_columns_dict.dict)
        dataset_name = "././datasets/04_demand_datasets/" + el[0] + "_" + el[1] + ".csv"
        demand_dataset.dataset.to_csv(dataset_name, index = False)
        print("Dataset saved!")

