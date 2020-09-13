import pandas as pd
import numpy as np

from area_enum import Area
from prod_enum import Prod


class DemandDataset:
    def __init__(self, input_data, prod, area, factors_columns_dict):
        self.input_data = input_data
        self.prod = prod
        self.area = area
        self.factors_columns_dict = factors_columns_dict
        self.dataset = self._create_dataset()
        self.prefix = '_p'


    def _create_dataset(self):
        dataset = pd.DataFrame()

        values = [self.area, self.prod, (self.area, self.prod), "All"]

        for key, val in self.factors_columns_dict.items():
            subkey = None

            for v in values:
                if v in val:
                    subkey = v
            
            if subkey is None:
                continue
            if key.lower()[:-2] in ['marketshares','numorders']:
                method_name = "_get_" + key.lower()[:-2]
                self.prefix = key.lower()[-2:]
            else:
                method_name = "_get_" + key.lower()
            dataset[key] = getattr(self, method_name)(val[subkey])

        return dataset


    def _get_column(self, col_name, type = float):
        col = self.input_data.loc[:,col_name].values
        col_replaced = np.where((col == "None") | (col == " "), 0, col)
        return col_replaced.astype(type)

    
    def _get_team(self, key):
        return self._get_column(key, str)


    def _get_history(self, key):
        return self._get_column(key, int)


    def _get_cycle(self, key):
        return self._get_column(key, int)


    def _get_diradv(self, key):
        return self._get_column(key)
    

    def _get_corpadv(self, key):
        dict_all = {0:{}, 1:{}, 2:{}, 3:{}}
        history_dict = {0:[], 1:[], 2:[], 3:[]}
        l = []

        col = self._get_column(key)
        self.input_data[key] = col

        for _, row in self.input_data.iterrows():
            scen = row["Scenario"]
            team = row["Team_c"]
            stage = row["Stage_c"]
            cykl_now = row['Cycle_c']
            value = row[key]

            #bierzemy bez bierzacej CorpAdv
            if team == 'Historia':
                CorpAdv = history_dict[scen].copy()
                history_dict[scen].append(value)

            else:  
                if cykl_now == 5:
                    if team not in dict_all[scen].keys():
                        dict_all[scen][team] = {stage:history_dict[scen].copy()}
                    else:
                        dict_all[scen][team][stage] = history_dict[scen].copy()
                CorpAdv = dict_all[scen][team][stage].copy()
                dict_all[scen][team][stage].append(value)
                
            if not CorpAdv :
                sum_corp = 0
            else:
                sum_corp = np.sum([var*(0.6**(cykl_now-(idx+1))) for idx, var in enumerate(CorpAdv)])
            l.append(sum_corp)

        return l


    def _get_commission(self, key):
        return self._get_column(key)


    def _get_agentsdistr(self, key):
        return self._get_column(key, int)


    def _get_support(self, key):
        return self._get_column(key)


    def _get_failedvisits(self, key):
        return 100 - self._get_column(key) / 10


    def _get_training(self, key):
        prev = self._get_column(key[0])
        curr = self._get_column(key[1])
        return np.round_((2/3) * prev + curr)

    def _get_managbudget(self, key):
        prev = self._get_column(key[0])
        curr = self._get_column(key[1])
        return prev + (2/3) * curr


    def _get_webdev(self, key):
        return self._get_column(key)


    def _get_backlogorders(self, key):
        ordered = self._get_column(key[0], int)
        sold = self._get_column(key[1], int)
        val = ordered - sold
        return np.where(val < 0, 0, val)


    def _get_randd(self, key):
        return self._get_column(key)


    def _get_price(self, key):
        return self._get_column(key)


    def _get_assemblytime(self, key):
        return self._get_column(key)


    def _get_col_base_num(self, start_col_name):
        start_col_num = int(start_col_name.partition("_")[0])
        return start_col_num + Area[self.area].value + 3 * Prod[self.prod].value
    

    def _get_marketshares(self, key):
        team_nums = self._get_column(key[0], int)

        start_col_name = key[1]
        col_base_num = self._get_col_base_num(start_col_name)
        values = []

        for team_num in enumerate(team_nums):
            if team_num[1] == 0:
                values.append(0)
            else:
                col_num = col_base_num + 10 * (team_num[1] - 1)
                col_name = str(col_num) + self.prefix
                col = self._get_column(col_name)
                val = col[team_num[0]]
                values.append(val)
        
        return values


    def _get_all_teams_x_columns_list(self, key, step):
        sufix = key[-2:]
        start_col_num = self._get_col_base_num(key)
        end_col_num = start_col_num + 8 * step
        return [str(x) + sufix for x in range(start_col_num, end_col_num, step)]


    def _get_all_teams_prices_columns_list(self, key):
        return self._get_all_teams_x_columns_list(key, 20)


    def _get_all_teams_market_shares_columns_list(self, key):
        return self._get_all_teams_x_columns_list(key, 10)


    def _get_meanprice(self, key):
        all_teams_prices_cols_list = self._get_all_teams_prices_columns_list(key[0])
        all_teams_market_shares_cols_list = self._get_all_teams_market_shares_columns_list(key[1])
        
        values = []

        for i in range(self.input_data.shape[0]):
            prices = self.input_data.loc[i, all_teams_prices_cols_list]
            number_of_teams = len([p for p in prices if p != 0])
            market_shares = self.input_data.loc[i, all_teams_market_shares_cols_list].values
            market_shares = [0 if y == "None" or y == " " else float(y) for y in market_shares]
            
            if not np.any(market_shares):
                mean_price = np.sum(prices) / number_of_teams
            else:
                mean_price = np.sum(prices * market_shares) / np.sum(market_shares)
                
            values.append(mean_price)

        return values


    def _get_numorders(self, key):
        return self._get_column(key, int)
        
    def _get_numsales_p(self, key):
        return self._get_column(key, int)
