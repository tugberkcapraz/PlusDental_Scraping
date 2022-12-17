import requests
from bs4 import BeautifulSoup
import pandas as pd
#import numpy as np
import argparse
import json
import time
import numpy as np

reviews = []

def trustpilot_scraper(PATH: str, page_number: int, lang: str):
    """

    :param PATH: str - Trustpilot link of the company.
    :param page_number: For iteration purposes. Helps navigating through pages
    :param lang: Language filter for the comments
    :return: A dataframe consisting of Comment, comment title, rating, location of the user, user name, date of the
    comment and language of the comment.
    """

    #Lists
    body = []
    heading = []
    rating = []
    location = []
    author = []
    date = []

    #Website Load
    page = "{a}?languages={b}&page=".format(a = PATH, b =lang)
    url = "{x}{y}&stars=1&stars=2&stars=3&stars=4&stars=5".format(x = page, y = page_number)
    print(url)
    req = requests.get(url)
    time.sleep(2)
    soup = BeautifulSoup(req.text, 'html.parser')

    #initial reviews
    reviews_raw = soup.find("script", id = "__NEXT_DATA__").string
    reviews_raw = json.loads(reviews_raw)
    rev = reviews_raw["props"]["pageProps"]["reviews"]

    #get reviews into df
    for i in range(len(rev)):
        instance = rev[i]
        body_ = instance["text"]
        heading_ = instance["title"]
        rating_ = instance["rating"]
        location_ = instance["consumer"]["countryCode"]
        author_ = instance["consumer"]["displayName"]
        date_ = pd.to_datetime(instance["dates"]["publishedDate"]).strftime("%Y-%m-%d")

        #append to the list
        body.append(body_)
        heading.append(heading_)
        rating.append(rating_)
        location.append(location_)
        author.append(author_)
        date.append(date_)
        df = {
            'date' : date,
            'author' : author,
            'text' : body,
            'title' : heading,
            'stars' : rating,
            'location' : location,
            'url': url,
            'language' : lang
        }

        rev_df = pd.DataFrame(df)
        rev_df.sort_values(by = "date", axis = 0, inplace = True, ignore_index = True)
        rev_df.drop_duplicates(subset=["text"],keep= 'first', inplace= True)
        rev_df.reset_index(drop = True, inplace = True)

    return rev_df


def main():
    """

    :return:
    """
    arg_parser = argparse.ArgumentParser()

    # Define Arguments
    # Varname
    arg_parser.add_argument(
        "-l",
        "--language",
        required=True,
        type=str,
        help = "Pass here the two digit abbreviation of the language that you wish to filter. Provide it in quotes. "
               "Example: python Scraper.py -l 'en' -p 4"

    )
    # Dataframe
    arg_parser.add_argument(
        "-p",
        "--page",
        required=True,
        type=int,
        help = "Pass here the maximum page numbers that you wish to scrape. If you wish to scrape n pages, then provide"
               "n+1. Example: python Scraper.py -l 'en' -p 4"

    )


    args = arg_parser.parse_args()

    # Place the arguments
    lang = args.language
    page = args.page

    #Set number of pages to scrape
    page_up = page
    pages = np.arange(2, page_up, 1)
    web = "plusdental"

    # Initiate empty data frame
    review_df = pd.DataFrame()

    #Loop over reviews
    for page in pages:
        review = trustpilot_scraper("https://www.trustpilot.com/review/"+web+".de", page, lang)
        # append the empty data frame
        review_df = review_df.append(review, ignore_index=True)

    # save it under data folder
    review_df.to_csv("../data/pd_rev_{}.csv".format(lang))

if __name__ == "__main__":
    main()