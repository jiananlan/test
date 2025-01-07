from bs4 import BeautifulSoup
import requests

# Define the URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/Python_(programming_language)"

# Send a GET request to the Wikipedia page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'lxml')

    # Extract the first paragraph from the page (example)
    first_paragraph = soup.find('p')
    print('here',first_paragraph.get_text())  
    print(response.text)# Get plain text from the paragraph
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
