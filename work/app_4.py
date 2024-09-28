import streamlit as st
import pandas as pd
import os
import pulp
from ShiftScheduler import ShiftScheduler

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
        calendar_df = pd.read_csv(calender_file)
        st.write(calendar_df)
    else:
        st.write('カレンダー情報をアップロードしてください')
    
with tab2:
    if staff_file is not None:
        st.markdown("## スタッフ情報")
        staff_df = pd.read_csv(staff_file)
        st.write(staff_df)
    else:
        st.write('スタッフ情報をアップロードしてください')

with tab3:
    if calender_file is None:
        st.write('カレンダー情報をアップロードしてください')
    if staff_file is None:
        st.write('スタッフ情報をアップロードしてください')
    if calender_file is not None and staff_file is not None:
        if st.button('最適化実行'):
            st.markdown("## 最適化結果")
            shift_sch = ShiftScheduler()
            shift_sch.set_data(staff_df, calendar_df)
            shift_sch.build_model()
            shift_sch.solve()

            st.write("実行ステータス:", pulp.LpStatus[shift_sch.status])
            st.write("最適値:", pulp.value(shift_sch.model.objective))

            st.markdown("## シフト表")
            st.write(shift_sch.sch_df)
    
    st.markdown("## シフト数の充足確認")
    st.markdown("## スタッフの希望の確認")
    st.markdown("## 責任者の合計シフト数の充足確認")
