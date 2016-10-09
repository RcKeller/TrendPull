# TrendPull

TrendPull provides an interface between market and SEO researchers and google trends that allows the mass-mining, collection, and dissemination of google search trend data. It supports both ad-hoc pulls and using .csv lists of data to pull thousands of trends at once.

This is currently a work-in-progress. Mass pulling via wordlists is not 100% functional, due to google terminating connections. In addition, corrupt data can be retrieved from google with large pull requests. These are known issues being addressed.

##### Requires:
 - Python 2.7
 - pytrends (any)
 - lxml (not always on pip, .whl file included in the env directory)
 - Microsoft C++ Compiler for Python

In addition, there are a few extra local files associated with TrendPull:
 - data/data.txt
    * Contains a username/password/agent name set
 - searches/searches.csv
    * Contains a spreadsheet of search terms used in Mass Pulls
 - trends/trends.csv
    * Default save location. Will error if the directory is not included.
 - 
 
##### Functions:
1. Credential Management
    - Credentials are automatically loaded, incl. the name of the agent/request
    - Credential management allows you to manually change credentials
2. Search List Management
    - Modify the path of your trend search list used in mass pulls    
3. Save Settings
    - Modify the path of your save file
4. Search Settings
    - Modify the parameters of your search.
    - Currently only toggles between US/All countries
5. Ad-Hoc Trend Pull
    - Pulls data trends for a set of searches separated by commas.
6. Mass Trend Pull
    - Pulls data trends for a large list loaded from a file, currently a work-in-progress function.