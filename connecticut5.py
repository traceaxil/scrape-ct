import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

# Define the base URL and range of IDs
base_url = "https://services.statescape.com/LegislatorInfo/Legislator.aspx?id="
id_range = range(17001, 18000)

# Initialize an empty list to store the data
data = []

# Iterate through the range of IDs
for i in id_range:
    url = base_url + str(i)
    response = requests.get(url)
    
    # Check if the page exists
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract name
        name_element = soup.find('span', class_='statelabel')
        name = name_element.text.strip() if name_element else None
        
        # Extract email
        email_element = soup.find('a', href=re.compile(r'^mailto:'))
        email = email_element['href'].replace('mailto:', '') if email_element else None
        
        # Extract additional info
        additional_info = {}
        labels = soup.find_all('span', class_='boldlabel')
        for label_element in labels:
            label_text = label_element.text.strip()
            next_element = label_element.find_next('span')
            if next_element:
                value = next_element.text.strip()
                if label_text == "Current Term Expires:":
                    additional_info['Current Term Expires'] = value
                elif label_text == "Home Page:":
                    home_page_element = label_element.find_next('a')
                    if home_page_element and 'href' in home_page_element.attrs:
                        additional_info['Home Page'] = home_page_element['href']
        
        # Append the extracted data to the list
        data.append({'Name': name, 'Email': email, **additional_info})

# Create a pandas DataFrame from the data
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel('legislator_info_file1h.xlsx', index=False)
