from abc import ABC, abstractmethod
import asyncio
import aiohttp
import feedparser

from feed_tracker import FeedTracker


class AtomFeedTracker (FeedTracker):
    """
    Base class to track any Atom/RSS feed asynchronously.
    Can be subclassed for OpenAI Atom Feed etc.
    """

    def __init__(self, feed_url: str, name: str, poll_interval: int = 60):
        self.feed_url = feed_url
        self.name = name
        self.poll_interval = poll_interval
        self.seen_ids = set()

        self.timeout = aiohttp.ClientTimeout(total=10)

    async def _fetch_feed(self, session) -> str:
        async with session.get(self.feed_url) as resp:
            resp.raise_for_status()
            return await resp.text()

    def _parse_feed(self, feed_text: str):
        return feedparser.parse(feed_text)

    @abstractmethod
    def _process_entry(self, entry):
        pass

    async def _poll_once(self, session, process_entries=True):
        """Fetch the feed once and process new items."""
        try:
            raw = await self._fetch_feed(session)
            feed = self._parse_feed(raw)

            for entry in feed.entries:
                if entry.id not in self.seen_ids:
                    self.seen_ids.add(entry.id)
                    if process_entries:
                        self._process_entry(entry)

        except Exception as e:
            print(f"Error in {self.name}: {e}")

    async def start(self, clear_backlog: bool = True):
        """Continuously poll the feed."""
        print(f"Started tracker: {self.name} ({self.feed_url})")

        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            if clear_backlog:
                await self._poll_once(session, process_entries=False)  # Initial poll without processing to clear backlog
            while True:
                await self._poll_once(session)
                await asyncio.sleep(self.poll_interval)
