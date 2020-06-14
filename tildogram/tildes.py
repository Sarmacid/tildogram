import requests
from bs4 import BeautifulSoup
import logging


def get_topics():
    url = "https://tildes.net/?order=new&period=1h"
    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")
    """
    with open("not_empty.html") as my_file:
        soup = BeautifulSoup(my_file.read(), "html.parser")
    """

    if soup.find("div", {"class": "empty"}):
        logging.info("No topics found.")
        return None

    all_topics = soup.find_all("article")
    logging.info(f"Found {len(all_topics)} topics.")

    parsed_topics = []

    for topic in all_topics:

        title_element = topic.header.h1.a
        topic_title = title_element.contents[0]
        topic_url = title_element.get("href")

        metadata = topic.find("div", {"class": "topic-metadata"})
        group = metadata.find("span", {"class": "topic-group"}).a.contents[0]
        tags = []

        if metadata.ul:
            for tag_element in metadata.ul.find_all("li"):
                tags.append(tag_element.a.contents[0])

        content_type = metadata.find("span", {"class": "topic-content-type"}).contents[
            0
        ]

        comments_elements = topic.footer.find("div", {"class": "topic-info-comments"})
        comments_path = comments_elements.a.get("href")
        comments_amount = int(comments_elements.span.contents[0].split(" ")[0])

        time = topic.footer.time.get("datetime")

        parsed_topics.append(
            {
                "Title": topic_title,
                "Group": group,
                "Content type": content_type,
                "Tags": tags,
                "Comments path": comments_path,
                "Comments": comments_amount,
                "Time posted": time,
            }
        )

        """
        print("***")
        print(f"Title: {topic_title}")
        print(f"URL: {topic_url}")
        print(f"Group: {group}")
        print(f"Content type: {content_type}")
        print(f"Tags: {tags}")
        print(f"Comments path: {comments_path}")
        print(f"Comments: {comments_amount}")
        print(f"Time posted: {time}")
        print("***")
        """

    return parsed_topics
