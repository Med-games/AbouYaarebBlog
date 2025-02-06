import requests
from bs4 import BeautifulSoup
import csv

titles = []
contents = []
dates = []
import re

# Send a GET request to the blog site
for i in range(1,2):
    url = "https://tadwinet.net/tag/%d8%a3%d8%a8%d9%88-%d9%8a%d8%b9%d8%b1%d8%a8-%d8%a7%d9%84%d9%85%d8%b1%d8%b2%d9%88%d9%82%d9%8a/page/"+str(i)+"/"  # Replace with the actual blog site URL

    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        # Find the blog posts on the page
        blog_urls = [h2.find('a')['href'] for h2 in soup.find_all('h2', class_='post-box-title')]
        # Process the blog posts
        for url in blog_urls:
            response = requests.get(url)
            post = BeautifulSoup(response.content, "html.parser")
            # Extract relevant information from each blog post

            title = post.find("h1",class_='post-title entry-title').get_text()
            content = post.find('div', class_='entry')
            updated_content = re.sub(r'<p[^>]*>\s*<a\b[^>]*>.*', '', str(content))
            updated_content = re.sub(r'<aside.*', '', str(updated_content))
            updated_content = re.sub(r'<span class="tagcloud">\s*<a.*?</span>', '', str(updated_content))
            
            date = post.find('span', class_='tie-date').get_text()
            titles.append(title)
            contents.append(updated_content)
            dates.append(date)
        
    else:
        print("Failed to retrieve the blog site.")
# Create the root element
data = list(zip(titles, contents, dates))

# Specify the file path
csv_file_path = "./data.csv"

# Write data to CSV file
with open(csv_file_path, mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    for title, content,date in data:
        content_with_tags = f'<html>{content}</html>'
        # Parse HTML content with BeautifulSoup
        soup = BeautifulSoup(content_with_tags, 'html.parser')
        # Remove all tags except <h2>
        for tag in soup.find_all(True):
            if tag.name != 'h2' and tag.name != 'strong' and tag.name != 'p':
                tag.unwrap()
        
        # Get cleaned content
        cleaned_content = str(soup)
        print(date)
        # Write title and cleaned content to CSV
        writer.writerow([title, cleaned_content, date])

