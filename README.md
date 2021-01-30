<p align="center">
    <a href="https://github.com/lalitpagaria/reddit-rss-reader/blob/master/LICENSE">
        <img alt="License" src="https://img.shields.io/github/license/lalitpagaria/reddit-rss-reader?color=blue">
    </a>
    <a href="https://pypi.org/project/reddit-rss-reader">
        <img src="https://img.shields.io/pypi/pyversions/reddit-rss-reader" alt="PyPI - Python Version" />
    </a>
    <a href="https://pypi.org/project/reddit-rss-reader/">
        <img alt="Release" src="https://img.shields.io/pypi/v/app-store-reviews-reader">
    </a>
    <a href="https://pepy.tech/project/reddit-rss-reader">
        <img src="https://pepy.tech/badge/reddit-rss-reader/month" alt="Downloads" />
    </a>
    <a href="https://github.com/lalitpagaria/reddit-rss-reader/commits/master">
        <img alt="Last commit" src="https://img.shields.io/github/last-commit/lalitpagaria/reddit-rss-reader">
    </a>
</p>

# Reddit RSS Reader
This is wrapper around publicly/privately available Reddit RSS feeds. It can be used to fetch content from front page, subreddit, all comments of subreddit, all comments of a certain post, comments of certain reddit user, search pages and many more. For more details about what type of RSS feed is provided by Reddit refer these links: [link1](https://www.reddit.com/r/pathogendavid/comments/tv8m9/pathogendavids_guide_to_rss_and_reddit/) and [link2](https://www.reddit.com/wiki/rss).

*Note: These feeds are rate limited hence can only be used for testing purpose. For serious scrapping register your bot at [apps](https://www.reddit.com/prefs/apps/) to get client details and use it with [Praw](https://github.com/praw-dev/praw).


## Installation

Install via PyPi:
```shell
pip install reddit-rss-reader
```
Install from master branch (if you want to try the latest features):
```shell
git clone https://github.com/lalitpagaria/reddit-rss-reader
cd reddit-rss-reader
pip install --editable .
```

# How to use
`RedditRSSReader` require feed url, hence refer [link](https://www.reddit.com/wiki/rss) to generate. For example to fetch all comments on subreddit `r/wallstreetbets` -
```shell
https://www.reddit.com/r/wallstreetbets/comments/.rss?sort=new
```

Now you can run the following [example](https://github.com/lalitpagaria/reddit-rss-reader/tree/master/example) -
```python
import pprint
from datetime import datetime, timedelta

import pytz as pytz

from reddit_rss_reader.reader import RedditRSSReader


reader = RedditRSSReader(
    url="https://www.reddit.com/r/wallstreetbets/comments/.rss?sort=new"
)

# To consider comments entered in past 5 days only
since_time = datetime.utcnow().astimezone(pytz.utc) + timedelta(days=-5)

# fetch_content will fetch all contents if no parameters are passed.
# If `after` is passed then it will fetch contents after this date
# If `since_id` is passed then it will fetch contents after this id
reviews = reader.fetch_content(
    after=since_time
)

pp = pprint.PrettyPrinter(indent=4)
for review in reviews:
    pp.pprint(review.__dict__)
```
Reader return `RedditContent` which have following information (`extracted_text` and `image_alt_text` are extracted from Reddit content via `BeautifulSoup`) -
```python
@dataclass
class RedditContent:
    title: str
    link: int
    id: str
    content: str
    extracted_text: Optional[str]
    image_alt_text: Optional[str]
    updated: datetime
    author_uri: str
    author_name: str
    category: str
```
The output is given with UTF-8 charsets, if you are scraping non-english reddits then set the environment to use UTF -
```shell
export LANG=en_US.UTF-8
export PYTHONIOENCODING=utf-8
```
