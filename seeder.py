from models import User, Topic, Tag, Comment, TopicLikeDislike, CommentLikeDislike

# Seeder function
def seed_data():
    # Create and save a user
    user1 = User(username='falgun_sinha', email='falgun.sinha@gmail.com', password='abc$123', first_name='Falgun', last_name='Sinha', active='Y')
    user1.save()
    user2 = User(username='maya.simpson', email='maya_simpson@rediff.com', password='password123', first_name='Maya', last_name='Simpson', active='Y')
    user2.save()
    user3 = User(username='sarahadams123', email='sarah.adams123@hotmail.com', password='CDF@456', first_name='Sarah', last_name='Adams', active='Y')
    user3.save()
    user4 = User(username='alex45', email='alex.lee@hotmail.com', password='123456', first_name='Alex', last_name='Lee', active='Y')
    user4.save()

    # Create and save a topic
    topic1 = Topic(title='Future of blockchain', description='It is going to be an era of blockchain in the next decade.', user_id=user1.id)
    topic1.save()
    topic2 = Topic(title='Redis DB', description='Redis is a No SQL Database', user_id=user1.id)
    topic2.save()
    topic3 = Topic(title='Winter has begun', description='Winter has begun and it is a white heaven everywhere', user_id=user2.id)
    topic3.save()
    topic4 = Topic(title='Unveiling the Art of Data Science', description='In the realm of modern technology, data science stands as the fulcrum, balancing on the convergence of raw information and insightful revelations.', user_id=user3.id)
    topic4.save()

    # Create and save a tag
    tag1 = Tag(tagname='#bitcoin')
    tag1.save()
    tag2 = Tag(tagname='blockchain')
    tag2.save()
    tag3 = Tag(tagname='NoSQL')
    tag3.save()
    tag4 = Tag(tagname='DataScience')
    tag4.save()

    # Create and save a comment on the topic
    comment1 = Comment(content='However, bitcoin may again decline in the near future.', user_id=user1.id)
    comment1.save(topic_id=topic1.id)
    comment2 = Comment(content='Other virtual currencies are going to have a better perspective.', user_id=user2.id)
    comment2.save(topic_id=topic1.id)
    comment3 = Comment(content='Document based No SQL Databases are better.', user_id=user3.id)
    comment3.save(topic_id=topic2.id)

    # User likes/dislikes topics
    user_like1 = TopicLikeDislike(user_id=user1.id, topic_id=topic1.id, is_liked=True)
    user_like1.save()
    user_like2 = TopicLikeDislike(user_id=user2.id, topic_id=topic1.id, is_liked=True)
    user_like2.save()
    user_like3 = TopicLikeDislike(user_id=user1.id, topic_id=topic1.id, is_liked=False)
    user_like3.save()
    user_like4 = TopicLikeDislike(user_id=user3.id, topic_id=topic2.id, is_liked=True)
    user_like4.save()
    user_like5 = TopicLikeDislike(user_id=user4.id, topic_id=topic3.id, is_liked=False)
    user_like5.save()
    user_like6 = TopicLikeDislike(user_id=user4.id, topic_id=topic4.id, is_liked=True)
    user_like6.save()

    # User likes/dislikes comments
    user_comment_like1 = CommentLikeDislike(user_id=user1.id, topic_id=topic1.id, comment_id=comment1.id, is_liked=True)
    user_comment_like1.save()
    user_comment_like2 = CommentLikeDislike(user_id=user2.id, topic_id=topic1.id, comment_id=comment1.id, is_liked=True)
    user_comment_like2.save()
    user_comment_like3 = CommentLikeDislike(user_id=user1.id, topic_id=topic2.id, comment_id=comment3.id, is_liked=False)
    user_comment_like3.save()
    user_comment_like4 = CommentLikeDislike(user_id=user3.id, topic_id=topic2.id, comment_id=comment3.id, is_liked=False)
    user_comment_like4.save()
    

# Run the seeder function to populate the Redis database
def run_seeders():
    # Perform seeders
    # ...

    seed_data()
    return "Seeders executed successfully"