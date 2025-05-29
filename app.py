import streamlit as st
from scraper import scrape_ibdb, save_data

st.set_page_config(page_title="IBDB Scraper", layout="wide")
st.title("📄 IBDB Web Scraper")

if "stop" not in st.session_state:
    st.session_state.stop = False

col1, col2 = st.columns(2)

with col1:
    if st.button("Run Scraper"):
        st.session_state.stop = False
        shows = scrape_ibdb(st.session_state)
        save_data(shows)
        st.success(f"Scraped {len(shows)} shows!")
        st.dataframe(shows)

with col2:
    if st.button("Stop"):
        st.session_state.stop = True
        st.warning("Scraper stopped.")
