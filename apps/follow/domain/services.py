from apps.follow.models import Follow


class FollowService(object):
    def follow(self, following_id, follower_id):
        return Follow.objects.create(follower=following_id, followed=follower_id)

    def is_following(self, following_id, follower_id):
        return Follow.objects.filter(
            follower=following_id, followed=follower_id
        ).exists()

    def unfollow(self, following_id, follower_id):
        return Follow.objects.filter(
            follower=following_id, followed=follower_id
        ).delete()

    def get_following_count(self, following_id):
        """フォローしている人の数を返す"""
        return Follow.objects.filter(follower=following_id).count()

    def get_follower_count(self, follower_id):
        """フォローされている人の数を返す"""
        return Follow.objects.filter(followed=follower_id).count()
