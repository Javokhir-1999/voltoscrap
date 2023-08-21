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

async def get_posts(search: dto.SearchDTO):
    fc = Facebook()
    # fc.login('sarvarhayatov5@gmail.com', 'Sarvar1995')
    fc.login('abdullajongaybullayev58@gmail.com', '10u&Nf9bVSeP')
    for text in search.words.split(','):
        fc.search(text)
        fc.scroll(search)
        await fc.get_posts(search)

    fc.quit()
  
    # import json
    # data = {'posts': ['фыв', 'sd'] }
    # json_object = json.dumps(data, indent=4, ensure_ascii=False).encode('utf8')
    # with open("data"+".json", "w") as outfile:
    #     outfile.write(str(json_object.decode()))