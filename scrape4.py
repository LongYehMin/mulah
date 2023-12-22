from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime, timedelta
import json

def get_news_sentiment(category, start_date):
    theverge_url = 'https://www.theverge.com/archives/'
    stop_collecting = False

    # Collecting daily news headlines for the chosen stocks on Business Insider
    news = {}
    all_data = []  # Collect data from all pages
    page_number = 1

    while not stop_collecting:
        url = f'{theverge_url}{category}/{start_date.year}/{page_number}'
        req = Request(url=url, headers={'User-Agent': 'my-app'})
        response = urlopen(req)

        soup = BeautifulSoup(response, 'html.parser')
        
        articles = soup.find_all('div', class_='c-entry-box--compact__body')

        if articles:
            for article in articles:
              
                date_time_str = article.find('div', class_='c-byline')['data-cdata']
                date_time_json = json.loads(date_time_str)
                date_time = datetime.utcfromtimestamp(int(date_time_json['timestamp']))
                
                headline = article.find('h2', class_='c-entry-box--compact__title').find('a')['data-chorus-optimize-field']
                link = article.find('h2', class_='c-entry-box--compact__title').find('a')['href']

                # Check if date is greater than or equal to start_date
                if date_time < start_date:
                    # If date is earlier than start_date, set the flag to stop collecting
                    stop_collecting = True
                    break
                                
                all_data.append([date_time, headline, link])
                print(date_time, headline, link)

            # Increment page number for the next iteration
            page_number += 1

            # Pause for a short time to avoid overwhelming the server
            time.sleep(1)

        else:
            print(f"No news table found for {category} on page {page_number}")
            break

    # Create the 'df' DataFrame
    df = pd.DataFrame(all_data, columns=['date_val', 'headline', 'link'])

    # Remove duplicate headlines
    df = df.drop_duplicates(subset=['headline'])

    return df

category = 'tech'
start_date = datetime(2022, 1, 1)
news_df = get_news_sentiment(category, start_date)
print(news_df)
