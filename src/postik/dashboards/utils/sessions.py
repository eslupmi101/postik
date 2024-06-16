from logging import getLogger

from posts.models import Post
from posts.serializers import PostSerializer

logger = getLogger(__name__)


# Sessions post
def delete_post_session(card: dict, post_id: int) -> dict:
    """
    Delete post and post_id from user session.

    return: session card
    """
    try:
        card['id_selected_posts'].remove(post_id)
    except ValueError as e:
        logger.warning(
            'Post with id %s not found in session id_selected_posts. %s', post_id, e
        )

    for i in range(len(card['posts'])):
        if card['posts'][i]['id'] == post_id:
            del card['posts'][i]
            break

    return card


def add_post_session(card: dict, post: dict) -> dict:
    """Add post and post_id to user session."""
    card['posts'] += [post]
    card['id_selected_posts'].append(int(post['id']))
    return card


def update_post_session(card: dict, posts: list[Post]) -> dict:
    """Update posts in session."""
    posts = [PostSerializer(post).data for post in posts]
    posts.sort(key=lambda post: post['id'])
    posts_session = card['posts']
    posts_session.sort(key=lambda post: post['id'])

    for i in range(len(posts_session)):
        for j in range(len(posts)):
            if posts_session[i]['id'] == posts[j]['id']:
                posts_session[i] = posts[j]
                del posts[j]
                break

    return card
