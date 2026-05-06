import streamlit as st
import stock_module_v2
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

st.set_page_config(page_title="專業台股分析系統", layout="wide")
st.title("⚡ 專業股市分析系統 (整合穩定版)")

with st.sidebar:
    st.header("數據查詢")
    stock_id = st.text_input("請輸入台股代碼", value="2330")
    analyze_btn = st.button("點擊開始分析")

if analyze_btn:
    with st.spinner('正在分析中...'):
        df = stock_module_v2.get_processed_data(stock_id)
        
        if df is not None:
            # 設定初始視野為最近 60 天，但保留完整資料供拖曳
            last_date = df.index[-1]
            start_view = last_date - datetime.timedelta(days=60)
            
            # 建立五層獨立圖表
            fig = make_subplots(
                rows=5, cols=1, 
                shared_xaxes=True, 
                vertical_spacing=0.03, 
                subplot_titles=('K線與均線', '成交量', '法人買賣', 'KD指標', 'MACD'),
                row_heights=[0.4, 0.12, 0.12, 0.12, 0.24]
            )

            # 1. K線圖
            fig.add_trace(go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close'], name='K線',
                increasing_line_color='red', decreasing_line_color='green'
            ), row=1, col=1)

            # 2. 成交量 (修正為長條圖)
            v_colors = ['red' if df['Close'].iloc[i] >= df['Open'].iloc[i] else 'green' for i in range(len(df))]
            fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='成交量', marker_color=v_colors), row=2, col=1)

            # 3. 法人買賣
            i_colors = ['red' if x >= 0 else 'green' for x in df['Inst_Net']]
            fig.add_trace(go.Bar(x=df.index, y=df['Inst_Net'], name='法人買賣', marker_color=i_colors), row=3, col=1)

            # 4. KD 指標
            k_col = [c for c in df.columns if 'STOCHk' in c][0]
            d_col = [c for c in df.columns if 'STOCHd' in c][0]
            fig.add_trace(go.Scatter(x=df.index, y=df[k_col], name='K值', line=dict(color='orange')), row=4, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df[d_col], name='D值', line=dict(color='dodgerblue')), row=4, col=1)

            # 5. MACD
            macd_h_col = [c for c in df.columns if 'MACDh' in c][0]
            m_colors = ['red' if x >= 0 else 'green' for x in df[macd_h_col]]
            fig.add_trace(go.Bar(x=df.index, y=df[macd_h_col], name='MACD柱', marker_color=m_colors), row=5, col=1)

            # 設定佈局與拖曳功能
            fig.update_layout(
                height=1100, 
                template="plotly_dark", 
                xaxis_rangeslider_visible=True, # 開啟底部滑動條
                xaxis=dict(range=[start_view, last_date]), # 鎖定初始視野
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("❌ 找不到資料。")