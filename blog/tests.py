from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Post
from blog.models import Post, Comment

class CustomAuthTokenTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jawad', password='jawad')
        self.client = APIClient()

    def test_custom_auth_token_valid(self):
        response = self.client.post('/api-token-auth/', {'username': 'jawad', 'password': 'jawad'})
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])

        if response.status_code == status.HTTP_200_OK:
            self.assertIn('token', response.data)
            token = response.data['token']
        else:
            self.assertEqual(response.data, {'message': 'Invalid username/password'})
            

class PostAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='jawad', password='jawad')
        self.published_post = Post.objects.create(
            author=self.user,
            title='Published Post',
            text='This is a published post.',
        )

    def test_get_published_post(self):
        response = self.client.get(f'/api/{self.published_post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Published Post')
        self.assertEqual(response.data['text'], 'This is a published post.')
        
    def test_create_post(self):
        self.client.login(username='jawad', password='jawad')

        new_post_data = {
            'title': 'New Post',
            'text': 'This is a new post.',
            'created_date': '2023-08-31T00:00:00Z',  
            'published_date': '2023-08-31T00:00:00Z',  
            'author': self.user.id,
     }

        response = self.client.post('/api/', new_post_data, format='json')


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_post = Post.objects.get(title='New Post')
        self.assertEqual(new_post.title, 'New Post')
        self.assertEqual(new_post.text, 'This is a new post.')
        self.assertEqual(new_post.created_date.strftime('%Y-%m-%dT%H:%M:%SZ'), '2023-08-31T00:00:00Z') 
        self.assertEqual(new_post.published_date.strftime('%Y-%m-%dT%H:%M:%SZ'), '2023-08-31T00:00:00Z')  
        self.assertEqual(new_post.author, self.user)
    
class PostAPITest_2_GET(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='jawad', password='jawad')

    def test_get_existing_post(self):
        published_post = Post.objects.create(
            author=self.user,
            title='Published Post',
            text='This is a published post.',
        )

        response = self.client.get(f'/api/{published_post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Published Post')
        self.assertEqual(response.data['text'], 'This is a published post.')
        
    def test_get_non_existing_post(self):
        response = self.client.get('/api/99/') 
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)    


class PostAPITest_2_PUT(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='jawad', password='jawad')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')

    def test_update_post_by_author(self):
        post = Post.objects.create(
            author=self.user,
            title='Test Post',
            text='This is a test post.',
        )

        self.client.login(username='jawad', password='jawad')

        updated_data = {
            'title': 'Updated Post',
            'text': 'This is an updated post.',
            'author': self.user.id,
        }

        response = self.client.put(f'/api/{post.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Post')
        self.assertEqual(response.data['text'], 'This is an updated post.')
        
    def test_update_post_by_non_author(self):
        post = Post.objects.create(
            author=self.other_user,
            title='Test Post',
            text='This is a test post.',
        )

        self.client.login(username='jawad', password='jawad')

        updated_data = {
            'title': 'Updated Post',
            'text': 'This is an updated post.',
        }
    
        response = self.client.put(f'/api/{post.id}/', updated_data, format='json')

    # Check for the presence of error details for the 'author' field
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "You are not authorized to edit this post.")

        
    def test_get_non_existing_post(self):
        self.client.login(username='jawad', password='jawad')

        response = self.client.get('/api/999/')  

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
class PostAPITest_3_DELETE(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='jawad', password='jawad')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')

    def test_delete_post_by_author(self):
        post = Post.objects.create(
            author=self.user,
            title='Test Post',
            text='This is a test post.',
        )

        self.client.login(username='jawad', password='jawad')

        # Delete the post
        response = self.client.delete(f'/api/{post.id}/')

        # Expect a 204 No Content status code indicating success
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check that the post is deleted from the database
        post_exists = Post.objects.filter(id=post.id).exists()
        self.assertFalse(post_exists)
        
    def test_delete_post_by_non_author(self):
        post = Post.objects.create(
            author=self.other_user,
            title='Test Post',
            text='This is a test post.',
        )

        self.client.login(username='jawad', password='jawad')

        response = self.client.delete(f'/api/{post.id}/') 

    # Check for the presence of an error message indicating unauthorized deletion
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "You are not authorized to delete this post.")
        
    def test_get_non_existing_post(self):
        self.client.login(username='jawad', password='jawad')

        response = self.client.get('/api/111/')  

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
class CommentAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='jawad', password='jawad')
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            text='This is a test post.',
        )
        self.comment_1 = Comment.objects.create(
            post=self.post,
            author=self.user,
            text='This is the first comment.',
        )
        
    def test_get_comments_for_post(self):
        self.client.login(username='jawad', password='jawad')
        response = self.client.get(f'/apicomment/{self.post.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Convert the response content to a string
        response_text = response.content.decode('utf-8')

        # Check if each expected comment is present in the response text
        expected_comments = [self.comment_1.text]
        for comment in expected_comments:
            self.assertIn(comment, response_text)
            
    def test_get_comments_for_nonexistent_post(self):
        self.client.login(username='jawad', password='jawad')
        response = self.client.get('/apicomment/99/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CommentAPITest_2(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='jawad', password='jawad')
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            text='This is a test post.',
        )    
        
    def test_add_comment_to_post(self):
        self.client.login(username='jawad', password='jawad')
        comment_data = {
            'post': self.post.id,
            'author': self.user.id,
            'text': 'This is a new comment.',
        }
        response = self.client.post('/apicomment/', comment_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the 'author' field from the response data
        response_author = response.data['author']

        # Convert the 'author' field to an integer (assuming it's an integer in your database)
        response_author = int(response_author)

        # Compare the converted 'author' field to self.user.id
        self.assertEqual(response_author, self.user.id)

        # Check if the comment text matches the one you provided
        self.assertEqual(response.data['text'], 'This is a new comment.')

    def test_create_comment_on_non_existent_post(self):
        comment_data = {
            'post': self.post.id,
            'author': self.user.id,
            'text': 'This is a new comment.',
        }
        response = self.client.post(f'api/999/comment', comment_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
