class User:
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username
        self.follower = 0
        self.following = 0

    def follow(self,user):
        user.follower += 1
        self.following += 1

user_1 = User("001", "JamesBond")

print(user_1.follower)

# user_2 = User()
# user_2.id = "002"
# user_2.username = "Ursula"