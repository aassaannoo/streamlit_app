import streamlit as st
import pandas as pd
import plotly.express as px


st.title('消費者物価指数（CPI）の推移')

data = pd.read_csv("zmy2020a.csv", header=None, encoding="cp932")
colnames = data.iloc[0].tolist()
colnames[0] = "年月"
maindata = data.iloc[6:].copy()
maindata.columns = colnames
maindata["年月"] = pd.to_datetime(maindata["年月"].astype(str), format="%Y%m")

# サイドバー
with st.sidebar:
    st.header("分析設定")
    
    # 期間選択
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



# 折れ線グラフ
st.write(f"### {start_date.strftime('%Y-%m')} から {end_date.strftime('%Y-%m')} の推移")
fig = px.line(df_show, x=df_show.index, y=df_show.columns)

    
fig.update_layout(
    legend_title_text='',
    template="plotly_dark", 
    paper_bgcolor="#1e1e1e",
    plot_bgcolor="#1e1e1e",
    font_color="white",
    hovermode="x unified",
        legend=dict(
        font=dict(color="white"))

)    

st.plotly_chart(fig, use_container_width=True)

#棒グラフ
st.write("最新月の品目別比較（棒グラフ）")

latest_data = df_show.iloc[-1]
    
fig_bar = px.bar(
        x=latest_data.index, 
        y=latest_data.values,
        labels={'x': '品目', 'y': '指数'} 
    )
    
fig_bar.update_layout(
    template="plotly_dark",
    paper_bgcolor="#1e1e1e",  
    plot_bgcolor="#1e1e1e",    
    font_color="white" ,
    showlegend=False # 棒グラフは色が1色なので凡例は不要
)

fig_bar.update_traces(marker_color='skyblue') 
st.plotly_chart(fig_bar, use_container_width=True)



# 最新データの表
st.write("最新データの状況")
if not df_show.empty:
    cols = st.columns(len(category)) 
    last_row = df_show.iloc[-1]      
    prev_row = df_show.iloc[-2]      
    
    for i, col_name in enumerate(category):
        val = last_row[col_name]
        diff = val - prev_row[col_name]
        with cols[i]:
            st.metric(label=col_name, value=f"{val:.1f}", delta=f"{diff:.1f}")

st.write("---")




# データダウンロード（授業未使用UI部品③）
st.download_button(
    label="CSVデータをダウンロード",
    data=df_show.to_csv().encode('utf-8'),
    file_name='cpi_data.csv',
    mime='text/csv',
)