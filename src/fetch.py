import requests

def fetch_posts(limit: int) -> list[dict]:
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    data = response.json()[:limit]
    return data
    
def print_posts(posts: list[dict]) -> None:
    for post in posts:
        print(post["title"])

def main() -> None:
    posts = fetch_posts(5)
    print_posts(posts)

if __name__ == "__main__":
    main()
