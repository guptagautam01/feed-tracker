import asyncio
from feed_tracker import FeedTracker
from openai_tracker import OpenAIFeedTracker


async def main():
    feeds: list[FeedTracker] = [
        OpenAIFeedTracker(poll_interval=60),
    ]
    clear_backlog = False  # Set to True to skip old entries on startup
    tasks = [asyncio.create_task(feed.start(clear_backlog)) for feed in feeds]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
