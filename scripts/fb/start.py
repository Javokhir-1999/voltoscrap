from scripts.fb.logic import Facebook
import dto

async def start(search: dto.SearchDTO):
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

    fc.quit()
  