import streamlit as st
from scraper import scrape_ibdb, save_data

st.title("📄 IBDB Web Scraper")

if "stop" not in st.session_state:
    st.session_state.stop = False

if st.button("Stop"):
    st.session_state.stop = True

if st.button("Run Scraper"):
    st.session_state.stop = False
    shows = scrape_ibdb(st.session_state)
    save_data(shows)
    st.success("Scraping complete. Data saved!")
