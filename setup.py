from setuptools import setup, find_packages


setup(
    name='twitter-shill-hunter',
    version='0.0.1',
    description='Uses NLP techniques to hunt for potential bot/shill/sock puppet accounts on Twitter',
    maintainer='@patamechanix',
    license='MIT',
    url='https://github.com/patamechanix/pata-password-cracker',
    package_dir={'': 'src'},
    include_package_data=True,
    packages=find_packages('src'),
    entry_points={
        'console_script': [
            'twitter_shill_hunter = twitter_shill.__main__:main'
        ]
    },
    install_requires=[
        'twitter==1.17.1',
        'nltk==2.0.5'
    ]
)
