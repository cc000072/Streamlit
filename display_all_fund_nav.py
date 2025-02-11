import streamlit as st
import sqlite3
import pandas as pd
import datetime
import numpy as np
import sys
import re

lst_fund_code_name = []


def highlight_background_color(val):

    if val > 0:

        color = "green"

    elif val < 0:

        color = "red"

    elif val == 0:

        color = "yellow"

    return 'background-color: %s' % color


def main():

    st.set_page_config(
        page_title="Daily Fund NAV",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )


    with st.form("All fund NAV"):

        DB_FILE = "C:\\Users\\cc000\\Desktop\\Batch\\Fund_Distribution_Date\\FUND_DIVIDEND_RECORD.db"
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()

        st.header("■Fund NAV")
        st.subheader("Fund daily NAV")
        dt_start_date = datetime.date(1900, 1, 1)
        dt_end_date = datetime.date(2100, 12, 31)
        dt_today_date = datetime.date.today()
        dt_enter_date = st.date_input("Enter NAV date", dt_today_date, min_value=dt_start_date, max_value=dt_end_date, key="name")
        str_nav_date = dt_enter_date.strftime("%Y%m%d")

        df_fund_nav_data_tmp = pd.read_sql(
            "SELECT fund_name, fund_nav, nav_change, profit_loss, total_balance FROM T_FUND_NAV WHERE date = " + str_nav_date + " ORDER BY fund_code",
            conn)

        if st.form_submit_button(label="Show nav data"):

            if df_fund_nav_data_tmp.empty is False:

                df_fund_nav_data_tmp = df_fund_nav_data_tmp.style.applymap(highlight_background_color, subset=["nav_change", "profit_loss"])
                st.dataframe(df_fund_nav_data_tmp, width=None, height=None, hide_index=True)

            elif df_fund_nav_data_tmp.empty is True:

                st.write("NAVデータがありません")


        st.subheader("Fund NAV line graph")
        df_fund_nav_data_tmp_a = pd.read_sql("SELECT fund_code, fund_name FROM M_FUND_LIST", conn)
        lst_fund_code_tmp = df_fund_nav_data_tmp_a["fund_code"].values.tolist()
        lst_fund_name_tmp = df_fund_nav_data_tmp_a["fund_name"].values.tolist()


        for int_index in range(0, len(lst_fund_code_tmp)):

            lst_fund_code_name.append(str(lst_fund_code_tmp[int_index]) + " : " + lst_fund_name_tmp[int_index])

        str_fund = st.selectbox("ファンド選択",lst_fund_code_name)


        if st.form_submit_button(label="Show nav graph"):

            lst_fund_info = str_fund.split(":")
            str_fund_code = lst_fund_info[0]
            str_fund_name = lst_fund_info[1]
            df_fund_nav_data_tmp = pd.read_sql("SELECT fund_code, fund_nav, date FROM T_FUND_NAV WHERE fund_code = " + str_fund_code, conn)


            if df_fund_nav_data_tmp.empty is False:

                df_fund_nav_data = pd.DataFrame({
                    "Date" : df_fund_nav_data_tmp["date"],
                    "NAV" : df_fund_nav_data_tmp["fund_nav"],
                    "Fund" : str_fund_name})
                st.line_chart(df_fund_nav_data, x="Date", y="NAV", color="Fund")

            elif df_fund_nav_data_tmp.empty is True:

                st.write("NAVデータがありません")

        cur.close()
        conn.close()

if __name__ == "__main__":

    main()