from scripts.fb.base import Base
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from scripts.fb.get_post import get_detailed_post

import dto
from domain import models
from domain.database_models.enums import SearchStatus, AnalizeStatus, Source
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class Facebook(Base):
    def login(self, usr, pwd):
        try:
            self.slp()
            username_box = self.driver.find_element('id', 'email')
            username_box.send_keys(usr)

            self.slp()
            password_box = self.driver.find_element('id', 'pass')
            password_box.send_keys(pwd)

            self.slp()
            login_box = self.driver.find_element('name', 'login')
            login_box.click()
        except Exception as ex:
            return ex

    def redirect_to_url(self, url):
        try:
            self.driver.get(url)
        except Exception as ex:
            print(ex)
        self.slp()

    def redirect_to_channel(self, channel_username):
        try:
            self.driver.get('https://www.facebook.com/' + channel_username)
        except Exception as ex:
            print(ex)
        self.slp()

    def go_back(self):
        self.driver.back()

    def channel_search(self, txt: str = "test"):

        self.slp()
        sleep(3)
        chennel_search_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-pagelet='ProfileActions']/div/div[3]"))
        )
        chennel_search_button.click()

        self.slp()
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete')
        chennel_search_input = self.driver.find_elements(By.XPATH, "//input[@type='search' and @spellcheck='false']")[1]
        chennel_search_input.send_keys(txt)

        self.slp()
        chennel_search_input.send_keys(Keys.ENTER)

    def global_search(self, txt: str = "test"):
        self.slp()
        search_box = self.driver.find_element(By.XPATH, "//input[@type='search']")
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
            self.driver.execute_script(
                f"window.scrollTo({current_position}, {browser_window_height + current_position + self.scroll_range()});")

            self.slp()
            WebDriverWait(self.driver, 50).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete')

            new_page_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_page_height == page_height:
                break

            page_height = new_page_height
            scroll_count += 1

    async def get_posts(self, search):
        search_obj = await models.Search.get(id=search.id)
        posts = self.driver.find_elements(By.XPATH, "//span/a[contains(@href,'pfbid')]")
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
                print("Exception:", e, post.get_attribute('href'))

        for post_link in post_links:
            post = get_detailed_post(post_link)

            print(post)
            try:
                post_obj = await models.Post.create(
                    source=Source.FB,
                    search_id=search.id,
                    author=post.get('username', None),
                    author_id=post.get('user_id', None),
                    pos_source_unique_id=post.get('post_id', None),
                    text=post.get('text', None),
                    date=post.get('time', None),
                    url=post.get('post_url', None),
                    # top_three_emoji = message.reactions,
                    # shares = message.forwards,
                    status=AnalizeStatus.NEW
                )
                for comment in post.get('comments_full', []):
                    print("comment:", comment)
                    comment_obj = await models.Comment.create(
                        post=post_obj,
                        search_id=search.id,
                        post_source_id=post_obj.pos_source_unique_id,
                        source=Source.FB,
                        comment_source_unique_id=comment.get('comment_id', None),
                        author=comment.get('commenter_name', None),
                        author_id=comment.get('commenter_id', None),
                        text=comment.get('comment_text', None),
                        url=comment.get('comment_url', None),
                        date=comment.get('comment_time', None),
                        emoji=comment.get('comment_reactions', None),
                        status=AnalizeStatus.NEW
                    )
                    for repl in comment.get('replies', []):
                        print("repl:", repl)
                        repl_obj = await models.Comment.create(
                            post=post_obj,
                            search_id=search.id,
                            post_source_id=post_obj.pos_source_unique_id,
                            source=Source.FB,
                            reply_url=comment_obj.url,
                            reply_comment=comment_obj,
                            comment_source_unique_id=repl.get('comment_id', None),
                            author=repl.get('commenter_name', None),
                            author_id=repl.get('commenter_id', None),
                            text=repl.get('comment_text', None),
                            url=repl.get('comment_url', None),
                            date=repl.get('comment_time', None),
                            emoji=repl.get('comment_reactions', None),
                            status=AnalizeStatus.NEW
                        )
            except Exception as ex:
                print("get post failed post_id:", "post_link", 'err_msg:', ex)
                continue

    async def get_post_by_url(self, search, url):
        search_obj = await models.Search.get(id=search.id)
        post_id = None
        try:
            if 'fbid=' in url:
                post_id = url.split('fbid=')[1].lstrip().split('&')[0]
            else:
                post_id = url.split('posts/')[1].lstrip().split('?')[0]
        except Exception as e:
            print("Exception:", e, url)

        post = get_detailed_post(post_id)

        print(post)
        try:
            post_obj = await models.Post.create(
                source=Source.FB,
                search_id=search.id,
                author=post.get('username', None),
                author_id=post.get('user_id', None),
                pos_source_unique_id=post.get('post_id', None),
                text=post.get('text', None),
                date=post.get('time', None),
                url=post.get('post_url', None),
                # top_three_emoji = message.reactions,
                # shares = message.forwards,
                status=AnalizeStatus.NEW
            )
            for comment in post.get('comments_full', []):
                print("comment:", comment)
                comment_obj = await models.Comment.create(
                    post=post_obj,
                    search_id=search.id,
                    post_source_id=post_obj.pos_source_unique_id,
                    source=Source.FB,
                    comment_source_unique_id=comment.get('comment_id', None),
                    author=comment.get('commenter_name', None),
                    author_id=comment.get('commenter_id', None),
                    text=comment.get('comment_text', None),
                    url=comment.get('comment_url', None),
                    date=comment.get('comment_time', None),
                    emoji=comment.get('comment_reactions', None),
                    status=AnalizeStatus.NEW
                )
                for repl in comment.get('replies', []):
                    print("repl:", repl)
                    repl_obj = await models.Comment.create(
                        post=post_obj,
                        search_id=search.id,
                        post_source_id=post_obj.pos_source_unique_id,
                        source=Source.FB,
                        reply_url=comment_obj.url,
                        reply_comment=comment_obj,
                        comment_source_unique_id=repl.get('comment_id', None),
                        author=repl.get('commenter_name', None),
                        author_id=repl.get('commenter_id', None),
                        text=repl.get('comment_text', None),
                        url=repl.get('comment_url', None),
                        date=repl.get('comment_time', None),
                        emoji=repl.get('comment_reactions', None),
                        status=AnalizeStatus.NEW
                    )
        except Exception as ex:
            print("get post failed post_id:", "post_link", 'err_msg:', ex)
