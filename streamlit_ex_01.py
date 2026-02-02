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
    with st.expander("消費者物価指数（CPI）の用語解説"):
        st.markdown("""
    消費者物価指数は、全国の世帯が購入する家計に係る財及びサービスの価格等を総合した物価の変動を時系列的に測定するものです。  
    すなわち家計の消費構造を一定のものに固定し、これに要する費用が物価の変動によって、どう変化するかを指数値で示したもので、毎月作成しています。  
    指数計算に採用している各品目のウエイトは総務省統計局実施の家計調査の結果等に基づいています。  
    品目の価格は総務省統計局実施の小売物価統計調査によって調査された小売価格を用いています。  
    参照：統計局ホームページhttps://www.stat.go.jp/data/cpi/index.html
    """)
   
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
st.write("---")

#棒グラフ
st.write("**最新月の品目別比較（棒グラフ）**")

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
    showlegend=False 
)

fig_bar.update_traces(marker_color='skyblue') 
st.plotly_chart(fig_bar, use_container_width=True)



# 最新データの表
st.write("**最新データの状況（先月との比較）**")
st.caption("※矢印は**先月との比較**です。プラスは値上がり、マイナスは値下がりを表します。")

if not df_show.empty:
    cols = st.columns(len(category)) 
    last_row = df_show.iloc[-1]      
    prev_row = df_show.iloc[-2]      
    
    for i, col_name in enumerate(category):
        val = last_row[col_name]
        diff = val - prev_row[col_name]
        with cols[i]:
            st.metric(label=col_name, value=f"{val:.1f}", delta=f"{diff:.1f}",delta_color="inverse")



#リンクボタン
st.write("---")
st.write("※使用データの出典")
st.link_button("e-Stat (政府統計の総合窓口) を見る", "https://www.e-stat.go.jp/stat-search/files?page=1&layout=dataset&toukei=00200573&tstat=000001150147&cycle=0&year=20230&month=12040605&tclass1=000001150151&tclass2=000001150152&tclass3=000001150153&tclass4=000001150156&stat_infid=000032103934")