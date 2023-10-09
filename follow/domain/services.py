from follow.models import Follow


class FollowService(object):
    def follow(self, following_id, follower_id):
        return Follow.objects.create(follower=following_id, followed=follower_id)
    
    def is_following(self, following_id, follower_id):
        return Follow.objects.filter(follower=following_id, followed=follower_id).exists()

    def unfollow(self, following_id, follower_id):
        return Follow.objects.filter(follower=following_id, followed=follower_id).delete()
