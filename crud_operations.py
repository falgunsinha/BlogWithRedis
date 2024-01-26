from models import Topic, Tag, Comment, User, TopicLikeDislike, CommentLikeDislike

from migrations import run_migrations
from seeder import run_seeders

# Run migrations and seeders
migration_result = run_migrations()
seeder_result = run_seeders()

print("Database connected successfully")  # Output: "Migrations executed successfully"
print(seeder_result)     # Output: "Seeders executed successfully"

def create_user():
    username = input("Enter Username: ")
    email = input("Enter Email: ")
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    password = input("Enter Password: ")
    active = input("Is user active? (Y/N): ")

    new_user = User(username, email, first_name, last_name, password, active)
    new_user.save()
    print("User created successfully!")

def view_users():
    all_users = User.find_all()
    if all_users:
        for user in all_users:
            print(user.__dict__)
    else:
        print("No users found.")

def delete_user():
    user_id = input("Enter User ID to delete: ")
    user = User.find_by_id(user_id)
    if user:
        user.delete()
        print("User deleted successfully!")
    else:
        print("User not found.")

def update_user():
    user_id = input("Enter User ID to update: ")
    user = User.find_by_id(user_id)
    if user:
        new_username = input("Enter new Username: ")
        new_email = input("Enter new Email: ")
        new_first_name = input("Enter new First Name: ")
        new_last_name = input("Enter new Last Name: ")
        new_password = input("Enter new Password: ")
        new_active = input("Is user active? (Y/N): ")

        user.username = new_username
        user.email = new_email
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.password = new_password
        user.active = new_active

        user.save()
        print("User updated successfully!")
    else:
        print("User not found.")

def create_topic():
    title = input("Enter Title: ")
    description = input("Enter Description: ")
    user_id = input("Enter User ID: ")
    new_topic = Topic(title, description, user_id)
    new_topic.save()
    print("Topic created successfully!")

def view_topics():
    all_topics = Topic.find_all()
    if all_topics:
        for topic in all_topics:
            print(topic.__dict__)
    else:
        print("No topics found.")

def delete_topic():
    topic_id = input("Enter Topic ID to delete: ")
    topic = Topic.find_by_id(topic_id)
    if topic:
        topic.delete()
        print("Topic deleted successfully!")
    else:
        print("Topic not found.")

def update_topic():
    topic_id = input("Enter Topic ID to update: ")
    topic = Topic.find_by_id(topic_id)
    if topic:
        new_title = input("Enter new Title: ")
        new_description = input("Enter new Description: ")
        topic.title = new_title
        topic.description = new_description
        topic.save()
        print("Topic updated successfully!")
    else:
        print("Topic not found.")

def create_tag():
    tagname = input("Enter Tag Name: ")
    new_tag = Tag(tagname)
    new_tag.save()
    print("Tag created successfully!")

def view_tags():
    all_tags = Tag.find_all()
    if all_tags:
        for tag in all_tags:
            print(tag.__dict__)
    else:
        print("No tags found.")

def delete_tag():
    tag_id = input("Enter Tag ID to delete: ")
    tag = Tag.find_by_id(tag_id)
    if tag:
        tag.delete()
        print("Tag deleted successfully!")
    else:
        print("Tag not found.")

def update_tag():
    tag_id = input("Enter Tag ID to update: ")
    tag = Tag.find_by_id(tag_id)
    if tag:
        new_tagname = input("Enter new Tag Name: ")
        tag.tagname = new_tagname
        tag.save()
        print("Tag updated successfully!")
    else:
        print("Tag not found.")

def create_comment():
    user_id = input("Enter User ID: ")
    content = input("Enter Comment: ")
    topic_id = input("Enter Topic ID: ")
    new_comment = Comment(user_id, content)
    new_comment.save(topic_id)
    print("Comment created successfully!")

def view_comments():
    topic_id = input("Enter Topic ID to view comments: ")
    topic = Topic.find_by_id(topic_id)
    if topic:
        comments = topic.get_comments()
        if comments:
            for comment in comments:
                print(comment.__dict__)
        else:
            print("No comments found for this topic.")
    else:
        print("Topic not found.")

def delete_comment():
    topic_id = input("Enter Topic ID for the comment: ")
    comment_id = input("Enter Comment ID to delete: ")
    comment = Comment.find_by_id(topic_id, comment_id)
    if comment:
        comment.delete(topic_id)
        print("Comment deleted successfully!")
    else:
        print("Comment not found.")

def update_comment():
    topic_id = input("Enter Topic ID for the comment: ")
    comment_id = input("Enter Comment ID to update: ")
    comment = Comment.find_by_id(topic_id, comment_id)
    if comment:
        new_content = input("Enter new content for the comment: ")
        comment.content = new_content
        comment.save(topic_id)
        print("Comment updated successfully!")
    else:
        print("Comment not found.")

def like_dislike_topic():
    topic_id = input("Enter Topic ID to like/dislike: ")
    is_liked = input("Like or Dislike? (L/D): ").upper()
    user_id = input("Enter User ID: ")

    if is_liked == "L":
        like = TopicLikeDislike(user_id, topic_id, True)
        like.save()
    elif is_liked == "D":
        dislike = TopicLikeDislike(user_id, topic_id, False)
        dislike.save()
    else:
        print("Invalid choice.")

def view_topic_likes_dislikes():
    topic_id = input("Enter Topic ID: ")
    likes = TopicLikeDislike.get_likes(topic_id)
    dislikes = TopicLikeDislike.get_dislikes(topic_id)
    print(f"Likes for Topic ID {topic_id}: {likes}")
    print(f"Dislikes for Topic ID {topic_id}: {dislikes}")

def like_dislike_comment():
    topic_id = input("Enter Topic ID: ")
    comment_id = input("Enter Comment ID to like/dislike: ")
    is_liked = input("Like or Dislike? (L/D): ").upper()
    user_id = input("Enter User ID: ")

    if is_liked == "L":
        like = CommentLikeDislike(user_id, topic_id, comment_id, True)
        like.save()
    elif is_liked == "D":
        dislike = CommentLikeDislike(user_id, topic_id, comment_id, False)
        dislike.save()
    else:
        print("Invalid choice.")

def view_comment_likes_dislikes():
    topic_id = input("Enter Topic ID: ")
    comment_id = input("Enter Comment ID: ")
    likes = CommentLikeDislike.get_comment_likes(topic_id, comment_id)
    dislikes = CommentLikeDislike.get_comment_dislikes(topic_id, comment_id)
    print(f"Likes for Comment ID {comment_id} under Topic ID {topic_id}: {likes}")
    print(f"Dislikes for Comment ID {comment_id} under Topic ID {topic_id}: {dislikes}")

while True:
    print("\nChoose an operation:")
    print("1. Create User")
    print("2. View Users")
    print("3. Delete User")
    print("4. Update User")
    print("5. Create Topic")
    print("6. View Topics")
    print("7. Delete Topic")
    print("8. Update Topic")
    print("9. Create Tag")
    print("10. View Tags")
    print("11. Delete Tag")
    print("12. Update Tag")
    print("13. Create Comment")
    print("14. View Comments")
    print("15. Delete Comment")
    print("16. Update Comment")
    print("17. Like/Dislike a Topic")
    print("18. View Likes/Dislikes for a Topic")
    print("19. Like/Dislike a Comment")
    print("20. View Likes/Dislikes for a Comment")
    print("0. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        create_user()
    elif choice == "2":
        view_users()
    elif choice == "3":
        delete_user()
    elif choice == "4":
        update_user()
    elif choice == "5":
        create_topic()
    elif choice == "6":
        view_topics()
    elif choice == "7":
        delete_topic()
    elif choice == "8":
        update_topic()
    elif choice == "9":
        create_tag()
    elif choice == "10":
        view_tags()
    elif choice == "11":
        delete_tag()
    elif choice == "12":
        update_tag()
    elif choice == "13":
        create_comment()
    elif choice == "14":
        view_comments()
    elif choice == "15":
        delete_comment()
    elif choice == "16":
        update_comment()
    elif choice == "17":
        like_dislike_topic()
    elif choice == "18":
        view_topic_likes_dislikes()
    elif choice == "19":
        like_dislike_comment()
    elif choice == "20":
        view_comment_likes_dislikes()
    elif choice == "0":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")
