import unittest
from unittest.mock import patch, MagicMock
from scripts.health_check import get_pr_details, determine_health_status, create_or_update_comment

class TestHealthCheck(unittest.TestCase):

    @patch('scripts.health_check.requests.get')
    def test_get_pr_details(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'commits': 5,
            'changed_files': 8,
            'additions': 150,
            'deletions': 50
        }
        mock_get.return_value = mock_response
        repo = 'your_username/your_repository'
        pr_number = 1
        token = 'fake_token'
        details = get_pr_details(repo, pr_number, token)
        self.assertEqual(details['commits'], 5)
        self.assertEqual(details['changed_files'], 8)

    def test_determine_health_status(self):
        status, color = determine_health_status(500, 5, 5)
        self.assertEqual(status, 'green')
        self.assertEqual(color, 'brightgreen')
        status, color = determine_health_status(600, 5, 5)
        self.assertEqual(status, 'yellow')
        self.assertEqual(color, 'yellow')
        status, color = determine_health_status(1500, 5, 5)
        self.assertEqual(status, 'red')
        self.assertEqual(color, 'red')

    @patch('scripts.health_check.requests.get')
    @patch('scripts.health_check.requests.post')
    @patch('scripts.health_check.requests.patch')
    def test_create_or_update_comment(self, mock_patch, mock_post, mock_get):
        repo = 'your_username/your_repository'
        pr_number = 1
        token = 'fake_token'
        comment_body = 'Test comment'

        # Simulate existing comment
        mock_get.return_value.json.return_value = [{'id': 1, 'body': '### PR Health Check Results'}]
        mock_patch.return_value.status_code = 200
        result = create_or_update_comment(repo, pr_number, token, comment_body)
        self.assertTrue(result)

        # Simulate no existing comment
        mock_get.return_value.json.return_value = []
        mock_post.return_value.status_code = 201
        result = create_or_update_comment(repo, pr_number, token, comment_body)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
