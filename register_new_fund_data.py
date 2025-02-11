import streamlit as st
import sqlite3
import pandas as pd
import datetime
import re


def main():

    st.set_page_config(
        page_title="Fund data registration",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )


    with st.form("New fund data registration"):

        DB_FILE = "C:\\Users\\cc000\\Desktop\\Batch\\Fund_Distribution_Date\\FUND_DIVIDEND_RECORD.db"
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()

        st.header("■New fund registration")
        new_buy, sold = st.tabs(["New fund registration", "Sold fund registration"])

        with new_buy:

            str_investment_category = st.selectbox("Investment category : ",("Domestic", "International"),)

            if str_investment_category == "International":

                str_investment_region = st.selectbox("Investment region : ", ("North America", "South America", "Asia (include AUS, Middle east)", "Europe", "Africa"), )

            elif str_investment_category == "Domestic":

                str_investment_region = "Japan"


            str_investment_asset = st.selectbox("Asset type : ",("Equity", "Bond", "REIT", "Commodity", "Multi-Asset"),)
            str_fund_name = st.text_area("Fund name", height=100, max_chars=50)
            str_distributor = st.selectbox("Distributor : ", ("SBI証券", "マネックス証券"), )
            int_dividend_number = st.number_input("Number of dividends", min_value=0, max_value=12)

            dt_start_date = datetime.date(1900, 1, 1)
            dt_end_date = datetime.date(2100, 12, 31)
            dt_today_date = datetime.date.today()
            dt_enter_date = st.date_input("Buy date", dt_today_date, min_value=dt_start_date, max_value=dt_end_date)
            int_base_amount = st.number_input("Base amount : ", min_value=0, step=1)
            int_total_unit = st.number_input("Total unit : ", min_value=0, step=1)
            int_base_nav = st.number_input("Base nav : ", min_value=0, step=1)


            if st.form_submit_button() == True:

                st.write(st.session_state)
                st.write(str_investment_category, str_investment_region, str_investment_asset, str_distributor, int_dividend_number, dt_enter_date, int_base_amount)

        with sold:

            df_fund_code = pd.read_sql("SELECT fund_code, fund_name FROM M_FUND_LIST WHERE hold = 1", conn)
            lst_fund_info_tmp = df_fund_code.values.tolist()
            lst_fund_info = []

            for int_index in range(0, len(lst_fund_info_tmp)):

                str_fund_code = str(lst_fund_info_tmp[int_index][0])
                str_fund_name = lst_fund_info_tmp[int_index][1]
                lst_fund_info.append(str_fund_code + " : " + str_fund_name)

            str_fund_info = st.radio("Select fund to update info : ", lst_fund_info, key="sold_fund")
            str_fund_code = re.findall(r'[0-9]+', str_fund_info)[0]
            print(str_fund_code, type(str_fund_code))

            if st.session_state:

                df_sold_fund_info = pd.read_sql("SELECT fund_code, fund_name FROM M_FUND_LIST WHERE fund_code = " + str_fund_code, conn)
                st.dataframe(df_sold_fund_info, width=None, height=None, hide_index=True)

        cur.close()
        conn.close()

if __name__ == "__main__":

    main()