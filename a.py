import requests
from bs4 import BeautifulSoup

# Send a GET request to YouTube's homepage
url = 'https://www.youtube.com'
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Successfully fetched the YouTube homepage")
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Get all text content from the page
    text_content = soup.get_text(separator=' ', strip=True)
    
    # Print the text content
    print(text_content[:2000])  # Print the first 2000 characters of the text
else:
    print(f"Failed to fetch the YouTube homepage. Status code: {response.status_code}")
