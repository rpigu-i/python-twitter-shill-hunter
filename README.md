### Twitter Shill Hunter


Uses NLP techniques to hunt for potential bot/shill/sock puppet accounts on Twitter.


## Sentiment Analysis

The application is currently using the Vader package to generate
sentiment analysis values for input search terms.
Also returned is an average (mean) compound value for each search term.
This is displayed on the screen to the user, but will in the future
be output as a file for futher statistical analysis if desired.

## Config file format

A config file takes the following format:

```


config:
    access_token: '<twitter access token>'
    access_secret: '<twitter access secret>
    consumer_key: '<twitter consumer key>'
    consumer_secret: '<twitter consumer secret>'
    target: <twitter username>
    search_terms:
        - Hurricane
        - Irma
    dialect: UK


```

The first four values can be found in your Twitter developer account:

https://apps.twitter.com

The `target` value should be a twitter username or ID.

Following this is a list of search terms listed under the 
`search_terms` key.

The final value is `dialect` (Note: this value is required but not 
currently used in the pre-release version).
Based upon the dialect input, tweets will be searched to see if 
they deviate from target dialect. 

For example if the target account is suppose to be using UK English
but uses US spellings and grammer, this will be flagged.


## Running the application.

Clone the source code from git and install via pip.

```
pip install -e python-twitter-shill-hunter
```

Then run

```
python -m twitter_shill_hunter twitter.yaml
```

