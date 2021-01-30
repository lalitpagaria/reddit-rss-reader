import logging
from dataclasses import dataclass
from datetime import datetime
from time import mktime
from typing import List, Optional

import feedparser
import requests
from bs4 import BeautifulSoup
from feedparser import FeedParserDict

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

    def fetch_content(self, after: Optional[datetime] = None, since_id: Optional[int] = None) -> List[RedditContent]:
        contents: List[RedditContent] = []
        feed = self.fetch_feed(self.url)

        for entry in feed.entries:
            if after is not None and after.timetuple() > entry.updated_parsed:
                break

            if since_id is not None and since_id == entry.id:
                break

            try:
                soup = BeautifulSoup(entry.summary)

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
    def fetch_feed(feed_url: str) -> FeedParserDict:
        # On MacOS https do not work, hence using workaround
        # Refer https://github.com/uvacw/inca/issues/162
        is_https = "https://" in feed_url[:len("https://")]
        if is_https:
            feed_content = requests.get(feed_url)
            feed = feedparser.parse(feed_content.text)
        else:
            feed = feedparser.parse(feed_url)

        return feed
