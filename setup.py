from setuptools import setup, find_packages


setup(
    name='twitter-shill-hunter',
    version='2.0.0',
    description='Uses NLP techniques to hunt for potential bot/shill/sock puppet accounts on X',
    author='@rpigu-i',
    author_email='rpigu.i@example.com',
    license='MIT',
    url='https://github.com/rpigu-i/twitter-shill-hunter',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
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
        'nltk==3.6.6',
        'vaderSentiment',
        '3to2',
        'language-check'
    ]
)
