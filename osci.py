import matplotlib.pyplot as plt
import seaborn as sns
import requests
import pandas as pd
import ast

def fetch_data(url, headers):
    """Fetch JSON data from a specified URL and return as a dictionary."""
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # This will raise an exception for HTTP errors
    return response.json()

def process_data(data):
    """Process the JSON data and return a pandas DataFrame."""
    if 'data' in data and isinstance(data['data'], list):
        df = pd.DataFrame(data['data'])
        return df
    else:
        raise ValueError("JSON structure doesn't match expected format.")
    
def plot_industry_active(df, economist_palette):
    """Plot total active contributors by industry."""
    plt.figure(figsize=(12, 8))
    industry_contributors = df.groupby('industry')['activeContributors'].sum()
    industry_contributors.sort_values(inplace=True)
    sns.barplot(x=industry_contributors.values, y=industry_contributors.index, palette = economist_palette)
    plt.title('Total Active Contributors by Industry')
    plt.xlabel('Total Active Contributors')
    plt.ylabel('Industry')
    plt.show()

def plot_license_distribution(df, economist_palette):
    """Plot the distribution of licenses."""
   
    # agregate the licenses dictionaries
    licenses_summary = {}
    for element in df["licenses"].sum():
        licenses_summary[element["name"]]  = licenses_summary.get(element["name"],0) + element["amount"]
    
   # Group less significant licenses into 'Others'
    licenses_grouped = {'other':  1e5}
    threshold =licenses_grouped['other']
    for name, count in licenses_summary.items():
        if count < threshold:
            licenses_grouped['other'] += count
        else:
            licenses_grouped[name] = count
    
    print(licenses_grouped)


    print(licenses_grouped)
    plt.figure(figsize=(12, 8))
    plt.bar(licenses_grouped.keys(), licenses_grouped.values(), color=economist_palette)
  
    plt.title('License Distribution')
    plt.xlabel('License')
    plt.ylabel('Amount')
    plt.gca().set_facecolor('#F4F5F7')
    plt.grid(color='white', linestyle='--', linewidth=0.5)
    plt.show()

def hbar_active_companies(df,economist_palette):
    """Plot the top 10 companies by active contributors."""
    plt.figure(figsize=(12, 8))
    top_companies = df.sort_values('activeContributors', ascending=False).head(10)
    sns.barplot(x='activeContributors', y='company', data=top_companies, palette=economist_palette[:len(top_companies)])
    plt.title('Top 10 Companies by Active Contributors')
    plt.xlabel('Active Contributors')
    plt.ylabel('Company')
    plt.show()

# Main execution flow
if __name__ == "__main__":
    url = 'https://ststaticprodosciwebz2vmu.blob.core.windows.net/data/osci-ranking/monthly/2023/12.json'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site'
    }

    try:
        data = fetch_data(url, headers)
        df = process_data(data)
        print(df)

        # Define the color palette
        economist_palette = ['#E3120B', '#5B9BD5', '#A5A5A5', '#ED7D31','#203864','#FFD966' ,'#70AD47','#DEEBF7','#7030A0','#36454F']

        # print(df["licenses"].sum())
        print("toto0")
        # Plot visualizations
        plot_industry_active(df,economist_palette)
        plot_license_distribution(df, economist_palette)  
        hbar_active_companies(df, economist_palette)
    except Exception as e:
        print(f"An error occurred: {e}")


# Extract the 'languages' column
languages_data = df['languages']

print(languages_data)