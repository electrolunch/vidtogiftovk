import json
from typing import Dict
from urllib.parse import quote
import requests
import os
class InstagramParser:
    def __init__(self, url_or_shortcode):
        self.INSTAGRAM_APP_ID = "936619743392459"  # this is the public app id for instagram.com
        self.url_or_shortcode = url_or_shortcode
        self.shortcode = self.get_shortcode()
        self.cache_file = f"{self.shortcode}_cache.json"

    def get_shortcode(self):
        if "http" in self.url_or_shortcode:
            if "/p/" in self.url_or_shortcode:
                return self.url_or_shortcode.split("/p/")[-1].split("/")[0]
            elif "/reel/" in self.url_or_shortcode:
                return self.url_or_shortcode.split("/reel/")[-1].split("/")[0]
        else:
            return self.url_or_shortcode

    def get_variables(self):
        return {
            "shortcode": self.shortcode,
            "child_comment_count": 20,
            "fetch_comment_count": 100,
            "parent_comment_count": 24,
            "has_threaded_comments": True,
        }

    def load_post(self):
        url = "https://www.instagram.com/graphql/query/?query_hash=b3055c01b4b222b8a47dc12b090e4e64&variables="
        result = requests.get(
            url=url + quote(json.dumps(self.get_variables())),
            headers={"x-ig-app-id": self.INSTAGRAM_APP_ID},
        )
        data = json.loads(result.content)
        with open(self.cache_file, 'w') as f:
            json.dump(data, f)
        return data

    def get_post(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        else:
            return self.load_post()

    def clear_cache(self):
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)


class InstagramPostInfo:
    def __init__(self, parser):
        self.parser = parser
        self.data = self.parser.get_post()
        self.post = self.data['data']['shortcode_media']

    def get_value(self, path, default=None):
        keys = path.split('.')
        value = self.post
        for key in keys:
            if isinstance(value, list):
                value = [v.get(key, default) if v else default for v in value]
            else:
                value = value.get(key, default) if value else default
        return value

    @property
    def description(self):
        captions = self.get_value('edge_media_to_caption.edges')
        if captions and isinstance(captions, list) and len(captions) > 0:
            return captions[0].get('node', {}).get('text')
        return None

    @property
    def id(self):
        return self.get_value('id')

    @property
    def shortcode(self):
        return self.get_value('shortcode')

    @property
    def dimensions(self):
        return self.get_value('dimensions')
    
    @property
    def video_url(self):
        return self.get_value('video_url')
    
    @property
    def is_video(self):
        return self.get_value('is_video')
    
    @property
    def comments_count(self):
        return self.get_value('edge_media_to_parent_comment.count')
    
    @property
    def comments(self):
        return self.get_value('edge_media_to_parent_comment.edges')
    

    def get_comments(self, num_comments):
        comments = self.comments
        if comments:
            comments = comments[:num_comments]
            return [{'id': comment.get('node').get('id'), 'text': comment.get('node').get('text')} for comment in comments]
        return []

    # Add other properties here

class VideoPostLoader:
    def __init__(self, post_info):
        self.post_info = post_info

    def download_video(self, directory):
        if not self.post_info.is_video:
            print("The post is not a video.")
            return

        video_url = self.post_info.video_url
        if video_url:
            response = requests.get(video_url)
            filename = os.path.join(directory, f"{self.post_info.shortcode}.mp4")
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Video downloaded to {filename}")
        else:
            print("No video URL found.")

    def extract_description(self):
        return self.post_info.description

    def extract_comments(self, n):
        return self.post_info.get_comments(n)
    

#%%

# %%
