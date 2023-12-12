import pandas as pd

data = pd.read_csv(r"./watch_recommend/data/watch.csv", encoding="utf-8")

def watch_rec():
    data_list = []
    for _, item in data.iterrows():
        data_list.append(item['0'])
    return data_list