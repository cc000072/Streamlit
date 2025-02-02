import streamlit as st
import sqlite3
import pandas as pd


def main():

    st.set_page_config(
        page_title="Fund Management Page",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    with st.form("Fund List"):

        DB_FILE = "C:\\Users\\cc000\\Desktop\\Batch\\Fund_Distribution_Date\\FUND_DIVIDEND_RECORD.db"
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()


        st.header("■Fund master")
        df_fund_list = pd.read_sql("SELECT * FROM M_FUND_LIST", conn)
        df_fund_list["fund_code"] = df_fund_list["fund_code"].apply(str)
        st.dataframe(df_fund_list, width=None, height=700, hide_index=True)


        cur.close()
        conn.close()
        st.form_submit_button()

if __name__ == "__main__":

    main()
