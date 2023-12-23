from flask import Flask, render_template
from scrape4 import (
    get_news

) 
import pandas as pd

app = Flask(__name__)

# Assuming you have a DataFrame 'df' with your data
df = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']})

# Convert the DataFrame to HTML
html_table = df.to_html()

# Define a route to display the HTML content
@app.route('/')
def news():
    headlines_df = get_news('tech')
    headlines_df = headlines_df.sort_values(by='date_time', ascending=False)
    headlines = headlines_df.to_dict(orient='records')
    return render_template('news.html', headlines=headlines)

if __name__ == '__main__':
    app.run(debug=True)
