from django.urls import reverse
from clubs.models import UserPost


def reverse_with_next(url_name,next_url):
      url=reverse(url_name)
      url += f"?next={next_url}"
      return url

def create_posts(author, from_count, to_count, club):
    """Create unique numbered posts for testing purposes."""
    for count in range(from_count, to_count):
        text = f'Post__{count}'
        post = UserPost(author=author, text=text, club=club)
        post.save()


class LogInTester:
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()
