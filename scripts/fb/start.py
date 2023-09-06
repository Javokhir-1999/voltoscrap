from scripts.fb.logic import Facebook
import dto
from domain import models

async def start(search: dto.SearchDTO):
    search_obj = await models.Search.get(id=search.id)
    try:
        fc = Facebook()
        fc.login('abdullajongaybullayev58@gmail.com', '10u&Nf9bVSeP')
        if search.facebook_channels:
            try:
                for channel_username in search.facebook_channels.split(','):
                    fc.redirect_to_channel(channel_username)
                    for text in search.words.split(','):
                        fc.channel_search(text)
                        fc.scroll(search)
                        await fc.get_posts(search)
                        fc.go_back()
            except Exception as ex:
                print(ex)

        else:
            for text in search.words.split(','):
                fc.global_search(text)
                fc.scroll(search)
                await fc.get_posts(search)

        if search.fb_posts:
            try:
                for post_url in search.fb_posts.split(','):
                    fc.redirect_to_url(post_url)
                    await fc.get_posts(search)

            except Exception as ex:
                print(ex)

        else:
            for text in search.words.split(','):
                fc.global_search(text)
                fc.scroll(search)
                await fc.get_posts(search)


        fc.quit()
    except Exception:
        pass
    await search_obj.recalc_counts()