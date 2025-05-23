import pytest
from rest_framework.test import APIClient
from blog.models import BlogPost

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def blog_posts():
    return [
        BlogPost.objects.create(title="Post 1", content="Content 1", published_date="2025-05-23T10:00:00Z"),
        BlogPost.objects.create(title="Post 2", content="Content 2", published_date="2025-05-23T11:00:00Z"),
    ]

@pytest.mark.django_db
def test_blogpost_list_endpoint(api_client, blog_posts):
    response = api_client.get('/api/blogposts/')
    assert response.status_code == 200
    assert len(response.data) == len(blog_posts)
    for i, post in enumerate(blog_posts):
        assert response.data[i]['title'] == post.title
        assert response.data[i]['content'] == post.content
        assert response.data[i]['published_date'] == post.published_date.isoformat()

class BlogPostTestCase(TestCase):
    def setUp(self):
        self.blog_post = BlogPost.objects.create(
            title="Test Blog",
            content="This is a test blog post.",
            published_date=datetime.now()
        )

    def test_blog_post_creation(self):
        self.assertEqual(self.blog_post.title, "Test Blog")
        self.assertEqual(self.blog_post.content, "This is a test blog post.")
        self.assertIsNotNone(self.blog_post.published_date)

    def test_blog_post_retrieval(self):
        retrieved_post = BlogPost.objects.get(title="Test Blog")
        self.assertEqual(retrieved_post, self.blog_post)

# Create your tests here.
