import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.rcParams['font.family'] = 'MS Gothic'

st.title('消費者物価指数（CPI）の推移比較')

data = pd.read_csv("zmy2020a.csv", header=None, encoding="cp932")
colnames = data.iloc[0].tolist()
colnames[0] = "年月"
maindata = data.iloc[6:].copy()
maindata.columns = colnames
maindata["年月"] = pd.to_datetime(maindata["年月"].astype(str), format="%Y%m")

# サイドバー
with st.sidebar:
    st.header("分析設定")
    
    # 期間選択（授業未使用UI部品①）
    dates = maindata["年月"].sort_values().unique()
    start_date, end_date = st.select_slider(
        "分析期間を選択",
        options=dates,
        value=(dates[-24], dates[-1]),
        format_func=lambda x: x.strftime("%Y-%m")
    )
    
    # 品目選択
    category = st.multiselect(
        "品目を選択",
        options=colnames[1:],
        default=["総合", "食料"]
    )
   
# データ処理
mask = (maindata["年月"] >= start_date) & (maindata["年月"] <= end_date)
df_show = maindata.loc[mask, ["年月"] + category].copy()
df_show.set_index("年月", inplace=True)
df_show = df_show.apply(pd.to_numeric, errors="coerce")

 
# sideberグラフメモリ設定
with st.sidebar:
    st.write("------------")
    st.write("グラフのメモリ設定")
    
    default_min = df_show.min().min() - 5
    default_max = df_show.max().max() + 5
    
    ymin = st.sidebar.number_input('最小値', value=default_min)
    ymax = st.sidebar.number_input('最大値', value=default_max)


# メイン画面表示
st.write(f"### {start_date.strftime('%Y-%m')} から {end_date.strftime('%Y-%m')} の推移")

# グラフ描画
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_show)

ax.set_ylim(ymin, ymax)


ax.grid(True)
ax.legend(df_show.columns)
st.pyplot(fig)

# データダウンロード（授業未使用UI部品③）
st.download_button(
    label="CSVデータをダウンロード",
    data=df_show.to_csv().encode('utf-8'),
    file_name='cpi_data.csv',
    mime='text/csv',
)