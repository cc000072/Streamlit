import streamlit as st
import sqlite3
import pandas as pd
import datetime

def main():

    st.set_page_config(
        page_title="Fund Dividend Page",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )


    with st.form("Fund dividend"):

        DB_FILE = "C:\\Users\\cc000\\Desktop\\Batch\\Fund_Distribution_Date\\FUND_DIVIDEND_RECORD.db"
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()


        dt_today_date = datetime.date.today()
        str_today_date = dt_today_date.strftime("%Y/%#m/%#d")
        st.header("■Fund dividend")


        df_total_dividend = pd.read_sql("SELECT SUM(dividend_amount) AS 'total dividend (JPY)' FROM T_DIVIDEND_RECORD", conn)
        lst_total_dividend = df_total_dividend.values.tolist()
        int_total_dividend = int(lst_total_dividend[0][0])
        st.subheader("Total dividend : " + str(int_total_dividend) + " in JPY by fund as of : " + str_today_date)
        df_fund_dividend = pd.read_sql("SELECT fund_code, fund_name, SUM(dividend_amount) AS 'total dividend by fund (in JPY)' FROM T_DIVIDEND_RECORD GROUP BY fund_code", conn)
        df_fund_dividend["fund_code"] = df_fund_dividend["fund_code"].apply(str)
        st.dataframe(df_fund_dividend, width=None, height=None, hide_index=True)


        df_fund_dividend_date = pd.read_sql("SELECT year, month, day FROM T_DIVIDEND_RECORD", conn)
        df_fund_dividend_date = df_fund_dividend_date.reset_index()
        df_year = df_fund_dividend_date["year"]
        df_month = df_fund_dividend_date["month"]
        lst_year = list(set(df_year.values.tolist()))
        lst_month = list(set(df_month.values.tolist()))
        lst_month.sort(reverse=False)
        st.subheader("Please select year and month")
        st.selectbox("From year", lst_year, key="year_from")
        st.selectbox("From month", lst_month, key="month_from")
        st.selectbox("To year", lst_year, key="year_to")
        st.selectbox("To month",lst_month, key="month_to")


        if st.form_submit_button(label="Show bar graph"):

            option_year_month_from = st.session_state["year_from"] + st.session_state["month_from"]
            option_year_month_to = st.session_state["year_to"] + st.session_state["month_to"]
            df_fund_dividend_per_month = pd.read_sql("SELECT fund_code, fund_name, SUM(dividend_amount) AS 'total dividend by fund (in JPY)', year_month FROM T_DIVIDEND_RECORD WHERE year_month BETWEEN " + option_year_month_from + " AND " + option_year_month_to + " GROUP BY year_month", conn)


            if df_fund_dividend_per_month.empty == True:

                st.warning("No dividend record found")

            elif df_fund_dividend_per_month.empty == False:

                df_fund_dividend_per_month["fund_code"] = df_fund_dividend_per_month["fund_code"].apply(str)
                df_chart_data = pd.DataFrame({"year/month":df_fund_dividend_per_month["year_month"],
                                              "total dividend in JPY":df_fund_dividend_per_month["total dividend by fund (in JPY)"]})
                st.subheader("Total dividend by month from " + option_year_month_from + " to " + option_year_month_to)
                st.subheader("Total dividend is " + str(int(df_fund_dividend_per_month["total dividend by fund (in JPY)"].sum())) + " in JPY")
                st.bar_chart(df_chart_data, x="year/month", y="total dividend in JPY")

        cur.close()
        conn.close()


if __name__ == "__main__":

    main()