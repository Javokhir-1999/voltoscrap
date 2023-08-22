from scripts.fb.logic import Facebook
import dto
# text_list = [
#         "Shavkat Umurzakov",
#         "Shavkat Umurzoqov",
#         "Sh. Umurzakov",
#         "Sh. Umurzoqov",
#         "Sh.Umurzakov",
#         "Sh.Umurzoqov",
#         "Ш. Умурзоқов",
#         "Ш. Умурзаков",
#         "Шавкат Умурзаков",
#         "Шавкат Умурзоқов",
#         "Shavkat Bo'ronovich Umurzoqov",
#         "Shavkat Buranovich Umurzakov",
#         "Shavkat Bo'ronovich",
#         "Shavkat Umurzoqov",
#         "Shavkat Buranovich",
#         "Shavkat Umurzakov",
#         "Bo'ronovich Umurzoqov",
#         "Buranovich Umurzakov",
#         "Шавкат Буранович Умурзаков",
#         "Шавкат Бўронович Умурзоқов",
#         "Шавкат Буранович",
#         "Шавкат Умурзаков",
#         "Шавкат Бўронович",
#         "Шавкат Умурзоқов",
#         "Буранович Умурзаков",
#         "Бўронович Умурзоқов",
#         "Toshkent Shahar Hokimligi",
#         "Toshkent Shaxar Hokimligi",
#         "Toshkent Shaxar Xokimligi",
#         "TOSHKENT SHAHAR HOKIMIYATI",
#         "Тошкент шаҳар ҳокимлиги",
#         "Тошкент шахар ҳокимлиги",
#         "Тошкент шахар хокимлиги",
#         "ТОШКЕНТ ШАҲАР ҲОКИМИЯТИ"
#     ]

async def start(search: dto.SearchDTO):
    fc = Facebook()
    # fc.login('sarvarhayatov5@gmail.com', 'Sarvar1995')
    fc.login('abdullajongaybullayev58@gmail.com', '10u&Nf9bVSeP')

    try:
        for channel_username in search.facebook_channels.split(','):
            fc.redirect_to_channel(channel_username)
            for text in search.words.split(','):
                fc.channel_search(text)
                fc.scroll(search)
                await fc.get_posts(search)
           
    except Exception as ex:
        for text in search.words.split(','):
            fc.global_search(text)
            fc.scroll(search)
            await fc.get_posts(search)

    fc.quit()
  