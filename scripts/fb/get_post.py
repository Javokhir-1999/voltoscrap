from facebook_scraper import get_posts, _scraper

POST_IDS = ["pfbid02ZHPkvGnzyF8QhV267ZvD4cP6JuLPLZ7uCErKsVegz4dLJVhp4JwUEPNLQSq711YPl","pfbid02nwAcFcd3ebxfEgpi5nuLxUkoDrDhzHEJaNLHRH8rG99YMhCM7ArvWZt5HomcjSTNl"]

def get_detailed_post(post_id):
    import facebook_scraper as fs
    # _scraper.login("abdullajongaybullayev58@gmail.com", "10u&Nf9bVSeP")
    # print(_scraper.is_logged_in())
    # https://www.facebook.com/groups/GROUP_ID/posts/POST_ID
    MAX_COMMENTS = 1000

    gen = fs.get_posts(
        post_urls=[post_id],
        options={"comments": MAX_COMMENTS, "progress": True}
    )
    post = next(gen)
    return post

# if __name__ == '__main__':
#     print(get_detailed_post(POST_IDS))
#
