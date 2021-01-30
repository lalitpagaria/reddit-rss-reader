import pprint
from datetime import datetime, timedelta

import pytz as pytz

from reddit_rss_reader.reader import RedditRSSReader


reader = RedditRSSReader(
    url="https://www.reddit.com/r/wallstreetbets/new/.rss?sort=new"
    # url="https://www.reddit.com/r/wallstreetbets/comments/l84ner/for_those_who_have_been_around_for_a_while_what/.rss?sort=new"
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
