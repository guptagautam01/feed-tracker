from bs4 import BeautifulSoup
from atom_tracker import AtomFeedTracker


class OpenAIFeedTracker(AtomFeedTracker):
    """
    Tracker for OpenAI's Atom feed.
    """

    def __init__(self, poll_interval: int = 60):
        super().__init__(
            feed_url="https://status.openai.com/feed.atom",
            name="OpenAI",
            poll_interval=poll_interval,
        )

    def _process_entry(self, entry):
        print(f"[{entry.updated}] {self.name} : {entry.title}")
        print(f"Incident Link: {entry.link}")
        # Extract the summary HTML
        summary = entry.summary_detail
        # Parse the HTML
        match summary.type:
            case "text/html":
                summary_html = summary.value
                soup = BeautifulSoup(summary_html, "html.parser")
                # Find the "Affected components" list
                affected_components = []
                ul = soup.find("ul")
                if ul:
                    for li in ul.find_all("li"):
                        # Remove the status in parentheses
                        component = li.text
                        affected_components.append(component)

                print("Affected components:", affected_components)
            case _:
                print("Unsupported summary type:", summary.type)
        print("-"*80)

        # print (soup)
