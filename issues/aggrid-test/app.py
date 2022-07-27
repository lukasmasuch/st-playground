from st_aggrid import AgGrid
import pandas as pd
import os

df = pd.read_csv(
    "https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv"
)
AgGrid(df)

# print(os.listdir("~/"), flush=True)
