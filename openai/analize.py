from langchain.chat_models import ChatOpenAI
from langchain.chains import create_tagging_chain
import os, requests, json

ENDPOINT_URL = 'https://f6a1-195-158-4-67.ngrok-free.app'
# We need a way to pass this securely
OPENAI_API_KEY = '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'
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

try:
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
except KeyError:
    print("OPENAI_API_KEY environment variable is not set.")


def fetch_data_from_url(url):
    try:
        print(f"Fetching data from the API endpoint: {url}...")
        req = requests.get(url)
        req.raise_for_status()
        return req.json().get('data', [])
    except requests.RequestException as e:
        print(f"Request returned error: {e}")
        return []


def fetch_posts(endpoint_url, search_id, page=1, page_size=1000):
    filter_search_id = f'search_id={search_id}'
    filter_page = f'page={page}&page_size={page_size}'
    url = endpoint_url + f'/post/list/?{filter_search_id}&{filter_page}'
    return fetch_data_from_url(url)


def fetch_comments(endpoint_url, post_id, page=1, page_size=10000):
    filter_post = f'post_id={post_id}'
    filter_page = f'page={page}&page_size={page_size}'
    url = endpoint_url + f'/comment/list/?{filter_post}&{filter_page}'
    return fetch_data_from_url(url)


def update_entry(endpoint_url, entry_type, entry_id, update_data):
    url_map = {
        "post": f'{endpoint_url}/post/put/{entry_id}',
        "comment": f'{endpoint_url}/comment/put/{entry_id}'
    }
    try:
        req = requests.put(url_map[entry_type], data=json.dumps(update_data))
        req.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to update {entry_type} ID: {entry_id}. Error: {e}")


schema = {
    "properties": {
        "language": {
            "type": "string",
            "enum": ["russian", "uzbek", "english", ],
        },
        "sentiment": {
            "type": "string",
            "enum": ["negative", "neutral", "positive", "sarcastic", "critique"],
        },
    },
    "required": ["language", "sentiment"],
}

llm = ChatOpenAI(temperature=0, model="gpt-4")
chain = create_tagging_chain(schema, llm)


def sentiment_classification(endpoint_url, search_id):
    try:
        posts = fetch_posts(endpoint_url=endpoint_url, search_id=search_id)
        print('Analyzing posts and comments')

        for post in posts:
            post_id = post.get('id', None)
            if post_id is None:
                print("Skipping post due to missing ID")
                continue

            comments = fetch_comments(endpoint_url=endpoint_url, post_id=post_id)
            post_text = post.get('text', "")
            try:
                post_analytics = chain.run(post_text)
                post_lang = post_analytics.get('language', 'unknown')
                post_sentiment = post_analytics.get('sentiment', 'unknown')

                update_entry(endpoint_url, 'post', post_id, {
                    'status': 'analyzed',
                    'tone': post_sentiment
                })
            except Exception as e:
                update_entry(endpoint_url, 'post', post_id, {
                    'status': 'failed',
                })

            for comment in comments:
                comment_id = comment.get('id', None)
                if comment_id is None:
                    print("Skipping comment due to missing ID")
                    continue

                comment_text = comment.get('text', "")
                try:
                    comment_analytics = chain.run(comment_text)
                    comment_lang = comment_analytics.get('language', 'unknown')
                    comment_sentiment = comment_analytics.get('sentiment', 'unknown')

                    update_entry(endpoint_url, 'comment', comment_id, {
                        'tone': comment_sentiment,
                        'status': 'analyzed'
                    })
                except Exception as e:
                    update_entry(endpoint_url, 'comment', comment_id, {
                        'status': 'failed'
                    })

    except Exception as e:
        print(f"An error occurred while classifying sentiment: {e}")


def test(search_id):
    sentiment_classification(ENDPOINT_URL, search_id)


if __name__ == '__main__':
    test('f71de9ae-181f-487c-a0ce-490c07e8904c')
