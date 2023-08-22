from scripts.fb.base import Base
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from scripts.fb.get_post import get_detailed_post

import dto
from domain import models
from domain.database_models.enums import SearchStatus, AnalizeStatus, Source
from time import sleep

class Facebook(Base):
    def login(self, usr, pwd):
        try:
            self.slp()
            username_box = self.driver.find_element('id', 'email')
            username_box.send_keys(usr)

            self.slp()
            password_box = self.driver.find_element('id','pass')
            password_box.send_keys(pwd)

            self.slp()
            login_box = self.driver.find_element('name','login')
            login_box.click()
        except Exception as ex:
            return ex

    def search(self, txt: str = "test"):
        self.slp()
        search_box = self.driver.find_element(By.XPATH,"//input[@type='search']")
        search_box.send_keys(txt)

        self.slp()
        search_box.send_keys(Keys.ENTER)

    def scroll(self, search):
        browser_window_height = self.driver.get_window_size(windowHandle='current')['height']
        current_position = self.driver.execute_script('return window.pageYOffset')
        self.driver.execute_script("""
                var style = document.createElement('style');
                style.innerHTML = 'html { scroll-behavior: smooth !important; }';
                document.head.appendChild(style);
            """)

        scroll_count = 0
        page_height = self.driver.execute_script("return document.body.scrollHeight")

        while scroll_count <= search.facebook_limit:
            current_position = self.driver.execute_script('return window.pageYOffset')
            self.driver.execute_script(f"window.scrollTo({current_position}, {browser_window_height + current_position+self.scroll_range()});")

            self.slp()
            sleep(2)

            new_page_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_page_height == page_height:
                break

            page_height = new_page_height
            scroll_count += 1

    async def get_posts(self, search, channel: None):
        if channel:
            try:
                self.driver.get('https://www.facebook.com/'+channel)
            except Exception as ex:
                print(ex)
                
        posts = self.driver.find_elements(By.XPATH,"//span/a[contains(@href,'pfbid')]")
        # print(posts)
        post_links = []

        for post in posts:
            try:
                url = post.get_attribute('href')
                if 'fbid=' in url:
                    post_links.append(url.split('fbid=')[1].lstrip().split('&')[0])
                else:
                    post_links.append(url.split('posts/')[1].lstrip().split('?')[0])
            except Exception as e:
                print("Exception:",e, post.get_attribute('href'))
        
        for post_link in post_links:
            post = get_detailed_post(post_link)
            print(post)
            try:
                post_obj = await models.Post.create(
                                source=Source.FB,
                                search_id=search.id,
                                author = post['username'],
                                author_id = post['user_id'],
                                pos_source_unique_id=post['post_id'],
                                text = post['text'],
                                date = post['time'],
                                url = post['post_url'],
                                # top_three_emoji = message.reactions,
                                # shares = message.forwards,
                                status = AnalizeStatus.NEW
                            )
            except Exception as ex:
                print("get post failed post_id:", "post_link", 'err_msg:', ex)
                continue

      

        

