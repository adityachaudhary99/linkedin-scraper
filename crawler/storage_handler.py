import json

class StorageHandler:
    def __init__(self, profile_file="profiles_new.json", posts_file="posts_new.json"):
        self.profile_file = profile_file
        self.posts_file = posts_file

    def save_profiles(self, profiles):
        with open(self.profile_file, "w") as f:
            json.dump(profiles, f)

    def save_posts(self, posts):
        with open(self.posts_file, "w") as f:
            json.dump(posts, f)
