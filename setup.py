from setuptools import setup, find_packages


setup(
    name='twitter-shill-hunter',
    version='2.0.0',
    description='Uses NLP techniques to hunt for potential bot/shill/sock puppet accounts on X',
    maintainer='@rpigu-i',
    license='MIT',
    url='https://github.com/rpigu-i/twitter-shill-hunter',
    package_dir={'': 'src'},
    include_package_data=True,
    packages=find_packages('src'),
    entry_points={
        'console_script': [
            'twitter_shill_hunter = twitter_shill_hunter.__main__:main'
        ],
        'twitter_shill_hunter.processors': [
            'sentiment_analysis = twitter_shill_hunter.processors.sentiment_analysis:SentimentAnalysis',
            'grammar_analysis = twitter_shill_hunter.processors.grammar_analysis:GrammarAnalysis',
            'spelling_analysis = twitter_shill_hunter.processors.spelling_analysis:SpellingAnalysis',
            'geo_analysis = twitter_shill_hunter.processors.geo_analysis:GeoAnalysis'
        ]
    },
    install_requires=[
        'twitter==1.17.1',
        'nltk==2.0.5',
        'vaderSentiment',
        '3to2',
        'language-check'
    ]
)
