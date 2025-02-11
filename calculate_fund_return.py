import streamlit as st
import sqlite3
import pandas as pd
import datetime as dt
import numpy as np
import sys
import math


def main():

    st.set_page_config(
        page_title="Daily Fund NAV",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )


    with st.form("Fund return"):

        DB_FILE = "C:\\Users\\cc000\\Desktop\\Batch\\Fund_Distribution_Date\\FUND_DIVIDEND_RECORD.db"
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()


        df_fund_master_sold = pd.read_sql("SELECT fund_name, fund_code, base_nav, base_amt, sell_nav, total_unit FROM M_FUND_LIST WHERE hold = 0", conn)
        df_fund_master_hold = pd.read_sql("SELECT fund_name, fund_code, base_nav, base_amt, total_unit FROM M_FUND_LIST WHERE hold = 1", conn)
        df_fund_dividend = pd.read_sql("SELECT fund_name, fund_code, SUM(dividend_amount) FROM T_DIVIDEND_RECORD GROUP BY fund_code", conn)


        df_fund_nav = pd.read_sql("SELECT fund_name, fund_code, date, fund_nav FROM T_FUND_NAV WHERE date = 20241011 ORDER BY date DESC", conn)
        df_fund_total_return_hold_tmp = pd.merge(df_fund_master_hold, df_fund_nav, on="fund_code", how="inner")
        df_fund_total_return_hold_tmp = pd.merge(df_fund_total_return_hold_tmp, df_fund_dividend, on="fund_code", how="inner")


        int_current_value = (df_fund_total_return_hold_tmp["fund_nav"] * df_fund_total_return_hold_tmp["total_unit"]) / 10000
        int_current_value = round(int_current_value)
        df_fund_total_return_hold_tmp["SUM(dividend_amount)"] = df_fund_total_return_hold_tmp["SUM(dividend_amount)"].astype("int64")
        int_total_dividend = df_fund_total_return_hold_tmp["SUM(dividend_amount)"]
        int_total_return =  int_current_value + int_total_dividend - df_fund_total_return_hold_tmp["base_amt"]
        int_total_return_ratio = (int_total_return / df_fund_total_return_hold_tmp["base_amt"]) * 100


        df_fund_total_return_hold_tmp["total_return"] = int_total_return_ratio
        df_fund_total_return_hold_tmp["hold"] = "保有中"
        df_fund_total_return_hold_tmp = df_fund_total_return_hold_tmp[["fund_name", "fund_code", "total_return", "hold"]]


        df_fund_total_return_sold_tmp = pd.merge(df_fund_master_sold, df_fund_dividend, on=["fund_name", "fund_code"], how="inner")
        int_sold_value = (df_fund_total_return_sold_tmp["sell_nav"] * df_fund_total_return_sold_tmp["total_unit"]) / 10000
        int_sold_value = round(int_sold_value)


        df_fund_total_return_sold_tmp["SUM(dividend_amount)"] = df_fund_total_return_sold_tmp["SUM(dividend_amount)"].astype("int64")
        int_total_dividend_sold = df_fund_total_return_sold_tmp["SUM(dividend_amount)"]
        int_total_return_sold =  int_total_dividend_sold + int_sold_value - df_fund_total_return_sold_tmp["base_amt"]
        int_total_return_sold_ratio = (int_total_return_sold / df_fund_total_return_sold_tmp["base_amt"]) * 100
        df_fund_total_return_sold_tmp["total_return"] = int_total_return_sold_ratio


        df_fund_total_return_sold_tmp["hold"] = "売却済"
        df_fund_total_return_sold_tmp = df_fund_total_return_sold_tmp[["fund_name", "fund_code", "total_return", "hold"]]
        df_fund_total_return = pd.concat([df_fund_total_return_hold_tmp, df_fund_total_return_sold_tmp], axis=0)


        st.header("■Fund total return")
        st.dataframe(df_fund_total_return, width=1000, height=None, hide_index=True)
        st.form_submit_button()

if __name__ == "__main__":

    main()