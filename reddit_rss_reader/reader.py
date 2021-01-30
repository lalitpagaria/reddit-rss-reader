import logging
from dataclasses import dataclass
from datetime import datetime
from time import mktime
from typing import List, Optional

import feedparser
import requests
from bs4 import BeautifulSoup
from feedparser import FeedParserDict

RATE_LIMIT_STR = 'you appear to be a bot and we\'ve seen too many requests'

logger = logging.getLogger(__name__)


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


@dataclass
class RedditRSSReader:
    # For proper url
    # Refer https://www.reddit.com/r/pathogendavid/comments/tv8m9/pathogendavids_guide_to_rss_and_reddit/
    url: str
    user_agent: Optional[str] = None

    def fetch_content(self, after: Optional[datetime] = None, since_id: Optional[int] = None) -> List[RedditContent]:
        contents: List[RedditContent] = []
        feed = self.fetch_feed(feed_url=self.url, user_agent=self.user_agent)

        # Check if rate limited
        if self.is_rate_limited(feed):
            logger.warning("Request is rate limited, hence wait for some time before running again")
            raise RuntimeError("Request is rate limited, hence wait for some time before running again")

        for entry in feed.entries:
            if after is not None and after.timetuple() > entry.updated_parsed:
                break

            if since_id is not None and since_id == entry.id:
                break

            try:
                soup = BeautifulSoup(entry.summary, "html.parser")

                image_alt_texts = [x['alt'] for x in soup.find_all('img', alt=True)]
                image_alt_texts = image_alt_texts if image_alt_texts else []

                contents.append(
                    RedditContent(
                        link=entry.link,
                        id=entry.id,
                        title=entry.title,
                        content=entry.summary,
                        extracted_text=soup.get_text(),
                        image_alt_text=". ".join(image_alt_texts),
                        updated=datetime.fromtimestamp(mktime(entry.updated_parsed)),
                        author_name=entry.author_detail.name,
                        author_uri=str(entry.author_detail.href),
                        category=entry.category
                    )
                )
            except Exception:
                logger.error(f'Error parsing Entry={entry}')

        return contents

    @staticmethod
    def is_rate_limited(feed: FeedParserDict):
        if feed and "feed" in feed and "summary" in feed.feed:
            text = ''.join(BeautifulSoup(feed.feed.summary, "html.parser").findAll(text=True))
            if RATE_LIMIT_STR in text:
                return True

        return False

    @staticmethod
    def fetch_feed(feed_url: str, user_agent: Optional[str]) -> FeedParserDict:
        if user_agent:
            feedparser.USER_AGENT = user_agent

        # On MacOS https do not work, hence using workaround
        # Refer https://github.com/uvacw/inca/issues/162
        is_https = "https://" in feed_url[:len("https://")]
        if is_https:
            feed_content = requests.get(feed_url)
            feed = feedparser.parse(feed_content.text)
        else:
            feed = feedparser.parse(feed_url)

        return feed
