import re
import time
import os
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import schedule
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def scrape_ibdb():
    driver = webdriver.Chrome()
    driver.get("https://www.ibdb.com/shows")

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "xt-iblock-inner"))
    )

    soup = BeautifulSoup(driver.page_source, "html.parser")
    blocks = soup.select(".xt-iblock-inner")
    all_shows = []

    driver.set_page_load_timeout(15)

    for i, block in enumerate(blocks):
        if len(all_shows) >= 40:
            break
        try:
            relative_link = block.select_one("a")["href"]
            detail_url = f"https://www.ibdb.com{relative_link}"
            style = block.select_one("span")["style"]
            image_url = re.search(r"url\((.*?)\)", style).group(1)

            driver.get(detail_url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            detail_soup = BeautifulSoup(driver.page_source, "html.parser")

            title_element = detail_soup.select_one("h3.title-label")
            title = title_element.text.strip() if title_element else "N/A"

            type_elements = detail_soup.select(".col.s12.txt-paddings.tag-block-compact i")
            show_types = [elem.text.strip() for elem in type_elements]
            show_types = list(dict.fromkeys(show_types))  # remove duplicates

            date_blocks = detail_soup.select(".xt-main-title")
            opening_date = date_blocks[0].text.strip() if len(date_blocks) > 0 else "N/A"
            closing_date = date_blocks[1].text.strip() if len(date_blocks) > 1 else "N/A"

            performances = "N/A"
            performance_blocks = detail_soup.select("div.col.s7.m6.l7.txt-paddings.vertical-divider")
            for block_perf in performance_blocks:
                label = block_perf.select_one("div.xt-lable")
                if label and "Performances" in label.text:
                    value = block_perf.select_one("div.xt-main-title")
                    performances = value.text.strip() if value else "N/A"
                    break

            show_data = {
                "Title": title,
                "Image URL": image_url,
                "Detail Link": detail_url,
                "Opening Date": opening_date,
                "Closing Date": closing_date,
                "Type(s)": ", ".join(show_types),
                "Performances": performances
            }
            all_shows.append(show_data)
            print(f"[{len(all_shows)}] ✅ Collected: {title}")

            time.sleep(1)

        except Exception as e:
            print(f"[{i+1}] ❌ Error: {e}")
            continue

    driver.quit()
    return all_shows


def save_data(df_or_list, base_dir="data",
              sender_email=None, sender_password=None, recipient_email=None):
    os.makedirs(base_dir, exist_ok=True)

    if isinstance(df_or_list, list):
        df = pd.DataFrame(df_or_list)
    else:
        df = df_or_list

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_name = f"{base_dir}/ibdb_shows_{timestamp}.csv"
    master_path = f"{base_dir}/ibdb_master.csv"

    if os.path.exists(master_path):
        master_df = pd.read_csv(master_path)
        combined = pd.concat([master_df, df]).drop_duplicates(subset=["Title", "Opening Date"])
        # Detect new shows:
        new_shows_df = combined.merge(master_df, how='outer', indicator=True)
        new_shows_df = new_shows_df[new_shows_df['_merge'] == 'left_only']
        new_shows = new_shows_df.drop(columns=['_merge']).to_dict('records')
    else:
        combined = df
        new_shows = df.to_dict('records')

    combined.to_csv(master_path, index=False)
    df.to_csv(snapshot_name, index=False)
    print(f"✅ Data saved to:\n - {master_path}\n - {snapshot_name}")

    # Send email if new shows found & email info provided
    if new_shows and sender_email and sender_password and recipient_email:
        send_email(new_shows, sender_email, sender_password, recipient_email)

    print("Scrape done!\n")
