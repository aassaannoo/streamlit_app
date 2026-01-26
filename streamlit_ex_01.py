import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title('消費者物価指数（CPI）の比較')

data = pd.read_csv("zmy2020a.csv", header=None, encoding="cp932")

meta = data.iloc[:6]
maindata = data.iloc[6:].copy()

colnames = data.iloc[0].tolist()
colnames[0] = "年月" 

maindata.columns = colnames

maindata["年月"] = maindata["年月"].astype(str)
maindata["年月"] = pd.to_datetime(maindata["年月"], format="%Y%m")



with st.sidebar:
    kikan = st.select_slider(
        "期間を選択してください",
        options=maindata["年月"].sort_values().unique()
    )

category = st.multiselect(
    "品目を選択してください",
    options=colnames[1:],
    default=["総合"]
)

#df_selected = maindata[maindata["年月"] == kikan]

st.write("選択した年月:", kikan.strftime("%Y-%m"))
st.write(maindata[maindata["年月"] + category])
