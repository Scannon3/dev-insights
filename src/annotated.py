
#defines function that takes in a list of dictionaries along with a user id.. returns a list of dicitonaries
def filter_and_sort_posts(posts: list[dict], user_id: int) -> list[dict]:
    #creates a new variable filtered and is assinged the results of the new list which are just the posts where the userid matches
    filtered = [post for post in posts if post["userId"] == user_id]
    #returns the new list sorted by post title
    return sorted(filtered, key=lambda post: post["title"])