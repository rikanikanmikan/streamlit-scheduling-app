import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import pulp
import matplotlib.pyplot as plt
import japanize_matplotlib
from src.ShiftScheduler import ShiftScheduler

# タイトル
st.title("シフトスケジューリングアプリ")

# サイドバー
st.sidebar.header("データのアップロード")

#calender_file = st.sidebar.file_uploader("カレンダー")
#staff_file = st.sidebar.file_uploader("スタッフ")

calender_file = "data/calendar.csv"
staff_file = "data/staff.csv"

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
            # 各スタッフの合計シフト数をstreamlitのbar chartで表示
            shift_sum = shift_sch.sch_df.sum(axis=1)
            st.bar_chart(shift_sum)           

            st.markdown("## スタッフの希望の確認")
            shift_staff = shift_sch.sch_df.sum(axis=0)
            st.bar_chart(shift_staff)           
    
            st.markdown("## 責任者の合計シフト数の充足確認")
            # shift_scheduleに対してstaff_dataをマージして責任者の合計シフト数を計算
            shift_schedule_with_staff_data = pd.merge(
                shift_sch.sch_df,
                staff_df,
                left_index=True,
                right_on="スタッフID",
            )
            # 責任者フラグが1の行のみqueryで抽出
            shift_chief_only = shift_schedule_with_staff_data.query("責任者フラグ == 1")
            # 不要な列はdropで削除する
            shift_chief_only = shift_chief_only.drop(
                columns=[
                    "スタッフID",
                    "責任者フラグ",
                    "希望最小出勤日数",
                    "希望最大出勤日数",
                ]
            )
            shift_chief_sum = shift_chief_only.sum(axis=0)
            st.bar_chart(shift_chief_sum)
            # DataFrameをCSV形式に変換

