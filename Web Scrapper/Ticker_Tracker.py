from Keys import reddit_UserName, reddit_Password, reddit_SecretToken, reddit_ClientID, reddit_User_Agent
from Read import stock_tickers, stock_ticker_words, stock_ticker_letters, stock_tickers_abbr
import praw
import datetime as dt
import csv
import re

#Collects the necessary info to run the reddit API
reddit = praw.Reddit(client_id = reddit_ClientID, client_secret = reddit_SecretToken, user_agent = reddit_User_Agent, username = reddit_UserName, password = reddit_Password)

def Ticker_Identification(input_list, ticker_list, ticker_words, ticker_abbr, ticker_letter):             #Finds all of the tickers listed in a list of stings that are in a predefined ticker list
    found_tickers = []
    regex = re.compile('[^a-zA-Z]')
    for i in range(0, len(input_list)):
        before = max(i-1,0)
        after = min(len(input_list)-1, i+1)
        if input_list[i].upper() in ticker_list:
            found_tickers.extend([input_list[i].upper()])
        if input_list[before].isupper() == False and input_list[after].isupper == False:
            if input_list[i] in ticker_words:
                found_tickers.extend([input_list[i]])
        if input_list[i].isalnum() == False:
            if regex.sub('', input_list[i]).upper() in ticker_abbr:
                found_tickers.extend([regex.sub('', input_list[i]).upper()])
            elif regex.sub('', input_list[i]).upper() in ticker_letter:
                found_tickers.extend([regex.sub('', input_list[i]).upper()])

    return found_tickers                                        #Return the list of found tickers

def Split_String(input_str):                                                        #Splits a string by any non-alphbetic characters and words that start with $
    split_str = re.split(r'\W+', input_str)                                         #Split by all non-alphabetic chracters
    dollar_start = [word for word in input_str.split() if word.startswith('$')]       #If a word starts with $, save it
    dollar_end = [word for word in input_str.split() if word.endswith('$')]
    parenthesis = [word for word in input_str.split() if (word.startswith('(') and word.endswith(')'))]
    split_str.extend(dollar_start)                                                    #Add it to the other string
    split_str.extend(dollar_end)
    split_str.extend(parenthesis)
    return list(set(split_str))                                                               #Return the final string


#Collects the data
post_tickers_scores = []
post_tickers_list = []
comment_tickers_scores = []
comment_tickers_list = []
for post in reddit.subreddit("wallstreetbets").top(time_filter = "day", limit = None):
    print("Analyzing New Post - Est Time = ", (post.num_comments/100))
    #Add the words from the post title and post body to the word lists
    post_title = Split_String(post.title)
    post_body = Split_String(post.selftext)
    
    post_tickers = Ticker_Identification(post_title, stock_tickers, stock_ticker_words, stock_tickers_abbr, stock_ticker_letters)
    post_tickers.extend(Ticker_Identification(post_body, stock_tickers, stock_ticker_words, stock_tickers_abbr, stock_ticker_letters))
    post_tickers_scores.append([list(set(post_tickers)), post.score])
    post_tickers_list.extend(post_tickers)
    
    #Derive the comment data
    post.comments.replace_more(limit=0)
    for comment in post.comments.list():
        comment_body = Split_String(comment.body)
        comment_tickers = Ticker_Identification(comment_body, stock_tickers, stock_ticker_words, stock_tickers_abbr, stock_ticker_letters)
        comment_tickers_scores.append([list(set(comment_tickers)), comment.score])
        comment_tickers_list.extend(comment_tickers)

post_tickers_list = list(set(post_tickers_list))
comment_tickers_list = list(set(comment_tickers_list))

print("DONE")