import requests
from bs4 import BeautifulSoup
import pandas as pd

# Fetch the webpage content
url = "https://www.tiobe.com/tiobe-index/"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing the data
    table = soup.find('table', {'class': 'table'})

    # Extract the table header
    header = [th.text.strip() for th in table.find_all('th')]
    print("Table Header:")
    print(header)

    # Extract the table rows
    rows = []
    for tr in table.find_all('tr')[1:]:  # Skip the header row
        cells = [td.text.strip() for td in tr.find_all('td')]
        del cells[3]  # Delete the 4th column
        rows.append(cells)

    # Print the table data
    print("\nTable Data:")
    for row in rows:
        print(row)
    
    # Create a pandas DataFrame from the table data
    df = pd.DataFrame(rows, columns=header)

    # Export the DataFrame to a CSV file
    df.to_csv('tiobe_index.csv', index=False)
else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")

print (df)
