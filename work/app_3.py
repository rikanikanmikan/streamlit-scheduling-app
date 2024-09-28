import streamlit as st
import pandas as pd

# タイトル
st.title("シフトスケジューリングアプリ")

# サイドバー
st.sidebar.header("データのアップロード")

calender_file = st.sidebar.file_uploader("カレンダー")

staff_file = st.sidebar.file_uploader("スタッフ")

# タブ
tab1, tab2, tab3 = st.tabs(["カレンダー情報", "スタッフ情報", "シフト表作成"])

with tab1:
    if calender_file is not None:
        st.markdown("## カレンダー情報")
        df = pd.read_csv(calender_file)
        st.write(df)
    else:
        st.write('カレンダー情報をアップロードしてください')
    
with tab2:
    if staff_file is not None:
        st.markdown("## スタッフ情報")
        df = pd.read_csv(staff_file)
        st.write(df)
    else:
        st.write('スタッフ情報をアップロードしてください')

with tab3:
    st.markdown("## 最適化結果")
    st.markdown("## シフト表")
    st.markdown("## シフト数の充足確認")
    st.markdown("## スタッフの希望の確認")
    st.markdown("## 責任者の合計シフト数の充足確認")
