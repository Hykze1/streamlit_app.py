import streamlit as st
from scraper import scrape_ibdb, save_data

st.set_page_config(page_title="IBDB Scraper", layout="wide")
st.title("📄 IBDB Web Scraper")

# Optional stop flag
if "stop" not in st.session_state:
    st.session_state.stop = False

if st.button("Stop"):
    st.session_state.stop = True

if st.button("Run Scraper"):
    st.session_state.stop = False
    shows = scrape_ibdb(st.session_state)
    save_data(shows)
    st.success(f"Scraped {len(shows)} shows!")
    st.dataframe(shows)
