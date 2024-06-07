import matplotlib.pyplot as plt
import seaborn as sns
import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_tiobe_index(url):
    """Fetches TIOBE Index webpage content and returns BeautifulSoup object."""
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        response.raise_for_status()

def extract_table_data(soup):
    """Extract table header and rows from the BeautifulSoup object."""
    table = soup.find('table', {'class': 'table'})
    header = [th.text.strip() for th in table.find_all('th')] 
    print("Table Header:")
    print(header)
    rows = []
    for tr in table.find_all('tr')[1:]:  # Skip the header row
        cells = [td.text.strip() for td in tr.find_all('td')]
        del cells[3]  # Delete the 4th column
        rows.append(cells)
    return header, rows


def parse_table(soup):
    """Parses the TIOBE Index table from the BeautifulSoup object."""
    table = soup.find('table', {'class': 'table'})
    header = [th.text.strip() for th in table.find_all('th')][:-1]  # Adjust to match actual columns
    rows = [[td.text.strip() for td in tr.find_all('td')][:len(header)] for tr in table.find_all('tr')[1:]]
    return header, rows

def create_dataframe(header, rows):
    """Create and return a cleaned DataFrame."""
    df = pd.DataFrame(rows, columns=header)
    # Clean and preprocess the DataFrame as needed
    df['Ratings'] = df['Ratings'].str.replace('%', '').astype(float)
    print(df['Ratings'][0])
    
   # Add the 'Grouped Language' column here
    df['Grouped Language'] = df.apply(lambda x: x['Programming Language'] if x['Ratings'] >= 3 else 'Others', axis=1)
    change_column_name = 'Change'
    return df

def export_to_csv (df):
    df.to_csv('tiobe_index.csv', index=False)

def plot_donut_chart(df):
    """Plot a donut chart from the DataFrame."""
    grouped_df = df.groupby('Grouped Language')['Ratings'].sum().reset_index()
    change_column_name = 'Change'
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = sns.color_palette('pastel')[0:len(grouped_df)]
    wedges, texts, autotexts = ax.pie(grouped_df['Ratings'], labels=grouped_df['Grouped Language'], colors=colors, autopct='%1.1f%%', startangle=140, pctdistance=0.85)
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)
    plt.title('Ratings Distribution Including "Others": March 2024')
    plt.show()
# Main execution starts here
url = "https://www.tiobe.com/tiobe-index/"
soup = fetch_tiobe_index(url)

if soup:
    header, rows = extract_table_data(soup)
    df = create_dataframe(header, rows)
    export_to_csv(df)
    # Perform any additional DataFrame processing here, such as grouping into "Others"
    # plot_donut_chart(df)  
