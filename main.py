import matplotlib.pyplot as plt
import seaborn as sns
import requests
import pandas as pd
from bs4 import BeautifulSoup

import osci
import refactored as tiobe

# Main execution flow
if __name__ == "__main__":
    osci_url = 'https://ststaticprodosciwebz2vmu.blob.core.windows.net/data/osci-ranking/monthly/2023/12.json'
    tiobe_url = "https://www.tiobe.com/tiobe-index/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site'
    }

    try:
        #get Tiobe data (language popularity)
        soup = tiobe.fetch_tiobe_index(tiobe_url)
        if soup:
            header, rows = tiobe.extract_table_data(soup)
            tiobe_df = tiobe.create_dataframe(header, rows)
            # Perform any additional DataFrame processing here, such as grouping into "Others"
            print(tiobe_df)
        
        #get OSCI data (company stats)
        data = osci.fetch_data(osci_url, headers)
        osci_df = osci.process_data(data)
        print(osci_df)

        



    except Exception as e:
        print(f"An error occurred: {e}")
