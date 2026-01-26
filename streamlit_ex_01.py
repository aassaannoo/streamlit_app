import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title('消費者物価指数（CPI）の比較')
data = pd.read_csv('zmy2020a.csv', encoding='cp932')
df = pd.DataFrame(data)


with st.sidebar:
    kikan = st.select_slider("期間の範囲を選択してください",
                             )
