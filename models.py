from migrations import run_migrations
from datetime import datetime

r = run_migrations()


# User Model
class User:
    def __init__(self, username, email, first_name, last_name, password, active='Y'):
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        self.id = f"U{first_name[0].upper()}{last_name[0].upper()}{current_time}"
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.active = active
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = self.created_at

    def save(self):
        user_data = {
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password,
            "active": self.active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        r.hmset(f"user:{self.id}", user_data)

    @staticmethod
    def find_by_id(id):
        user_data = r.hgetall(f"user:{id}")
        if user_data:
            return User(
                user_data[b'username'].decode('utf-8'),
                user_data[b'email'].decode('utf-8'),
                user_data[b'first_name'].decode('utf-8'),
                user_data[b'last_name'].decode('utf-8'),
                user_data[b'password'].decode('utf-8'),
                user_data[b'active'].decode('utf-8'),
            )
        return None
    
    @staticmethod
    def find_all():
        all_user_keys = r.keys("user:*")
        all_users = []
        for key in all_user_keys:
            user_data = r.hgetall(key)
            user = User(
                user_data[b'username'].decode('utf-8'),
                user_data[b'email'].decode('utf-8'),
                user_data[b'first_name'].decode('utf-8'),
                user_data[b'last_name'].decode('utf-8'),
                user_data[b'password'].decode('utf-8'),
                user_data[b'active'].decode('utf-8'),
            )
            all_users.append(user)
        return all_users
    
    def delete_all_users():
        user_keys = r.keys("user:*")
        for key in user_keys:
            r.delete(key)
        print("All users deleted.")

# Comment Model
class Comment:
    def __init__(self, user_id, content):
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        self.id = f"CM{current_time}"
        self.user_id = user_id
        self.content = content
        self.likes = 0
        self.dislikes = 0
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = self.created_at

    def save(self, topic_id):
        comment_data = {
            "user_id": self.user_id,
            "content": self.content,
            "likes": self.likes,
            "dislikes": self.dislikes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        r.hmset(f"topic:{topic_id}:comment:{self.id}", comment_data)

    @staticmethod
    def find_by_id(topic_id, comment_id):
        comment_data = r.hgetall(f"topic:{topic_id}:comment:{comment_id}")
        if comment_data:
            return Comment(
                comment_data[b'user_id'].decode('utf-8'),
                comment_data[b'content'].decode('utf-8')
            )
        return None
    
    @staticmethod
    def find_all(topic_id):
        all_comment_keys = r.keys(f"topic:{topic_id}:comment:*")
        all_comments = []
        for key in all_comment_keys:
            comment_id = key.decode('utf-8').split(":")[-1]
            comment_data = r.hgetall(key)
            comment = Comment(
                comment_data[b'user_id'].decode('utf-8'),
                comment_data[b'content'].decode('utf-8')
            )
            comment.id = comment_id
            comment.likes = int(comment_data[b'likes'])
            comment.dislikes = int(comment_data[b'dislikes'])
            comment.created_at = comment_data[b'created_at'].decode('utf-8')
            comment.updated_at = comment_data[b'updated_at'].decode('utf-8')
            all_comments.append(comment)
        return all_comments
    
    @staticmethod
    def delete_all_comments():
        comment_keys = r.keys("topic:*:comment:*")
        for key in comment_keys:
            r.delete(key)
        print("All comments deleted.")

# Topic Model
class Topic:
    def __init__(self, title, description, user_id):
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        self.id = f"TP{current_time}"
        self.title = title
        self.description = description
        self.user_id = user_id
        self.likes = 0
        self.dislikes = 0
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = self.created_at

    def save(self):
        topic_data = {
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id,
            "likes": self.likes,
            "dislikes": self.dislikes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        r.hmset(f"topic:{self.id}", topic_data)

    @staticmethod
    def find_by_id(id):
        topic_data = r.hgetall(f"topic:{id}")
        if topic_data:
            return Topic(
                topic_data[b'title'].decode('utf-8'),
                topic_data[b'description'].decode('utf-8'),
                topic_data[b'user_id'].decode('utf-8')
            )
        return None
    
    @staticmethod
    def find_all():
        all_topic_keys = r.keys("topic:*")
        all_topics = []
        for key in all_topic_keys:
            if r.type(key) == b'hash':
                topic_data = r.hgetall(key)
                if topic_data and b'title' in topic_data and b'description' in topic_data and b'user_id' in topic_data:
                    topic = Topic(
                        topic_data[b'title'].decode('utf-8'),
                        topic_data[b'description'].decode('utf-8'),
                        topic_data[b'user_id'].decode('utf-8')
                    )
                    topic.id = key.split(":")[-1].decode('utf-8')
                    all_topics.append(topic)
        return all_topics

    def add_comment(self, user_id, content):
        comment = Comment(user_id, content)
        comment.save(self.id)

    def get_comments(self):
        comments = []
        comment_keys = r.keys(f"topic:{self.id}:comment:*")
        for key in comment_keys:
            comment_id = key.decode('utf-8').split(":")[-1]
            comment = Comment.find_by_id(self.id, comment_id)
            comments.append(comment)
        return comments
    
    def delete_all_topics():
        topic_keys = r.keys("topic:*")
        for key in topic_keys:
            r.delete(key)
        print("All topics deleted.")

# Tag Model
class Tag:
    def __init__(self, tagname):
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        self.id = f"TG{current_time}"
        self.tagname = tagname
        self.description = tagname
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = self.created_at

    def save(self):
        tag_data = {
            "tagname": self.tagname,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        r.hmset(f"tag:{self.id}", tag_data)

    @staticmethod
    def find_by_id(id):
        tag_data = r.hgetall(f"tag:{id}")
        if tag_data:
            return Tag(
                tag_data[b'tagname'].decode('utf-8')
            )
        return None
    
    @staticmethod
    def find_all():
        all_tag_keys = r.keys("tag:*")
        all_tags = []
        for key in all_tag_keys:
            tag_data = r.hgetall(key)
            tag = Tag(
                tag_data[b'tagname'].decode('utf-8')
            )
            tag.id = key.split(":")[-1]
            tag.description = tag_data[b'description'].decode('utf-8')
            tag.created_at = tag_data[b'created_at'].decode('utf-8')
            tag.updated_at = tag_data[b'updated_at'].decode('utf-8')
            all_tags.append(tag)
        return all_tags
    
    @staticmethod
    def delete_all_tags():
        tag_keys = r.keys("tag:*")
        for key in tag_keys:
            r.delete(key)
        print("All tags deleted.")

class TopicLikeDislike:
    def __init__(self, user_id, topic_id, is_liked=True):
        self.user_id = user_id
        self.topic_id = topic_id
        self.is_liked = is_liked

    def save(self):
        r.sadd(f"topic:{self.topic_id}:likes" if self.is_liked else f"topic:{self.topic_id}:dislikes", self.user_id)
        print("Topic liked!" if self.is_liked else "Topic disliked!")

    @staticmethod
    def get_likes(topic_id):
        return r.smembers(f"topic:{topic_id}:likes")

    @staticmethod
    def get_dislikes(topic_id):
        return r.smembers(f"topic:{topic_id}:dislikes")
    
    @staticmethod
    def drop_likes_dislikes_for_topics():
        topic_like_keys = r.keys("topic:*:likes")
        topic_dislike_keys = r.keys("topic:*:dislikes")
    
    # Combine all keys related to topic likes and dislikes
        all_topic_keys = topic_like_keys + topic_dislike_keys
    
    # Delete all keys related to topic likes and dislikes
        for key in all_topic_keys:
            r.delete(key)

class CommentLikeDislike:
    def __init__(self, user_id, topic_id, comment_id, is_liked=True):
        self.user_id = user_id
        self.topic_id = topic_id
        self.comment_id = comment_id
        self.is_liked = is_liked

    def save(self):
        r.sadd(f"topic:{self.topic_id}:comment:{self.comment_id}:likes" if self.is_liked else f"topic:{self.topic_id}:comment:{self.comment_id}:dislikes", self.user_id)
        print("Comment liked!" if self.is_liked else "Comment disliked!")

    @staticmethod
    def get_comment_likes(topic_id, comment_id):
        return r.smembers(f"topic:{topic_id}:comment:{comment_id}:likes")

    @staticmethod
    def get_comment_dislikes(topic_id, comment_id):
        return r.smembers(f"topic:{topic_id}:comment:{comment_id}:dislikes")
    
    @staticmethod
    def drop_likes_dislikes_for_comments():
        comment_like_keys = r.keys("comment:*:likes")
        comment_dislike_keys = r.keys("comment:*:dislikes")
    
    # Combine all keys related to comment likes and dislikes
        all_comment_keys = comment_like_keys + comment_dislike_keys
    
    # Delete all keys related to comment likes and dislikes
        for key in all_comment_keys:
            r.delete(key)


# # Example usage:

# # Create and save a user
# user1 = User('john_doe', 'john@example.com', 'John', 'Doe', 'password123', 'Y')
# user1.save()

# # Retrieve user by ID
# retrieved_user = User.find_by_id(user1.id)
# print("Retrieved User:", retrieved_user.__dict__ if retrieved_user else "User not found")

# # Create and save a topic
# topic1 = Topic('Redis Basics', 'Introduction to Redis', user1.id)
# topic1.save()

# # Retrieve topic by ID
# retrieved_topic = Topic.find_by_id(topic1.id)
# print("Retrieved Topic:", retrieved_topic.__dict__ if retrieved_topic else "Topic not found")

# # Create and save a tag
# tag1 = Tag('NoSQL')
# tag1.save()

# # Retrieve tag by ID
# retrieved_tag = Tag.find_by_id(tag1.id)
# print("Retrieved Tag:", retrieved_tag.__dict__ if retrieved_tag else "Tag not found")

# # Add comments to a topic
# topic1.add_comment(user1.id, "This is a comment.")
# topic1.add_comment(user1.id, "Another comment.")

# # Get comments for a topic
# comments = topic1.get_comments()
# for comment in comments:
#     print(comment.__dict__)
