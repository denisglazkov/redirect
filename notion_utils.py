import os
import requests
import datetime

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB_ID = os.getenv("NOTION_DB_ID")  # "Subscribers" DB
NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def insert_notion_row(source, count, when=None):
    """
    Insert a new row into the Notion 'Subscribers' database.
    Properties: Name, Source, time, Count
    """
    if when is None:
        when = datetime.datetime.now(datetime.timezone.utc)

    payload = {
        "parent": {"database_id": NOTION_DB_ID},
        "properties": {
            "Name": {
                "title": [
                    {"text": {"content": f"Data for {source}"}}
                ]
            },
            "Source": {
                "rich_text": [
                    {"text": {"content": source}}
                ]
            },
            "time": {
                "date": {
                    "start": when.isoformat()
                }
            },
            "Count": {
                "number": count
            }
        }
    }

    url = "https://api.notion.com/v1/pages"
    resp = requests.post(url, headers=NOTION_HEADERS, json=payload)
    resp.raise_for_status()
    return resp.json()


def get_last_two_entries_for_source(source):
    """
    Query Notion for the last 2 rows for a given 'Source', sorted by 'time' DESC.
    Return a list of page objects.
    """
    query_url = f"https://api.notion.com/v1/databases/{NOTION_DB_ID}/query"
    payload = {
        "filter": {
            "property": "Source",
            "rich_text": {"equals": source}
        },
        "sorts": [
            {
                "property": "time",
                "direction": "descending"
            }
        ],
        "page_size": 2
    }
    resp = requests.post(query_url, headers=NOTION_HEADERS, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data.get("results", [])


def extract_count_from_page(page):
    """Return the integer from the 'Count' property."""
    props = page["properties"]
    return props["Count"]["number"]