from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import json
import calendar

def get_news(category):
    theverge_url = 'https://www.theverge.com/archives/'

    # Define the range of years and months
    years = [2022,2023]
    months = list(range(1, 13))

    # Collecting daily news headlines for the chosen category on The Verge
    all_data = []  # Collect data from all pages

    for year in years:
        for month in months:
            last_day_of_month = calendar.monthrange(year, month)[1]

            for day in range(1, last_day_of_month + 1):
                url = f'{theverge_url}{category}/{year}/{month}/{day}'
                req = Request(url=url, headers={'User-Agent': 'my-app'})

                try:
                    response = urlopen(req)
                    soup = BeautifulSoup(response, 'html.parser')

                    articles = soup.find_all('div', class_='c-entry-box--compact__body')

                    if articles:
                        for article in articles:
                            date_time_str = article.find('div', class_='c-byline')['data-cdata']
                            date_time_json = json.loads(date_time_str)
                            date_time = datetime.utcfromtimestamp(int(date_time_json['timestamp']))

                            headline = article.find('h2', class_='c-entry-box--compact__title').find('a').text
                            link = article.find('h2', class_='c-entry-box--compact__title').find('a')['href']

                            all_data.append([date_time, headline, link])
                            print(date_time, headline, link)
                    else:
                        print(f"No news table found for {category} on {year}-{month}-{day}")

                    # Pause for a short time to avoid overwhelming the server
                    time.sleep(1)

                except HTTPError as e:
                    print(f"Error for {category} on {year}-{month}-{day}: {e}")

                # Pause before moving to the next day
                time.sleep(1)

    # Create the 'df' DataFrame outside the loop
    df = pd.DataFrame(all_data, columns=['date_time', 'headline', 'link'])

    # Remove duplicate headlines
    df = df.drop_duplicates(subset=['headline'])

    # Sort the DataFrame by 'date_val' in descending order
    df = df.sort_values(by='date_time', ascending=False)

    all_data.append(df)

    return df