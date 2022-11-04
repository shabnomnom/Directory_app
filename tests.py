import unittest
import main
import os
import json


class MyAppIntegrationTestCase(unittest.TestCase):
    """Examples of integration tests: testing Flask server."""

    def setUp(self):
        self.client = main.app.test_client()
        current_directory = os.getcwd()
        # print(current_directory)
        main.folder_path = os.path.join(current_directory, 'test_fixtures')
        main.app.config['TESTING'] = True

    def test_root_index(self):
        """testing root directory return values """
        result = self.client.get('/')
        result_dict = json.loads(result.data)
        self.assertEqual(result_dict['subfolder']['name'], 'subfolder')
        self.assertIsNotNone(result_dict['subfolder']['owner'])
        self.assertEqual(result_dict['subfolder']['permission'], 'drwxr-xr-x')
        self.assertIsNotNone(result_dict['subfolder']['size'])

    def test_subdirectory_return_content(self):
        result = self.client.get('/subfolder')
        result_dict = json.loads(result.data)
        self.assertEqual(result_dict['file.txt']['name'], 'file.txt')
        self.assertEqual(result_dict['.hidden']['name'], '.hidden')
        self.assertIsNotNone(result_dict['file.txt']['owner'])
        self.assertEqual(result_dict['file.txt']['permission'], '-rw-r--r--')
        self.assertEqual(result_dict['file.txt']['size'], 63)

    def test_file_return_content(self):
        result = self.client.get('/subfolder/file.txt')
        result_dict = json.loads(result.data)
        self.assertEqual(
            result_dict['fileContent'], 'Today is my birthday and I would like to eat some grilled fish.')

    def test_missing_subdirectory(self):
        result = self.client.get('/subfolder/dinner_menu')
        self.assertEqual(result.status_code, 404)

    # testing POST and DELETE for direcotries 
    def test_json_creation_directory(self):
        response = self.client.post('/subfolder', json={
            "name": "new_subfolder",
            "type": "directory"
        })
        result = self.client.get('/subfolder')
        result_dict = json.loads(result.data)
        self.assertEqual(result_dict['new_subfolder']['name'], 'new_subfolder')
        self.assertEqual(result_dict['new_subfolder']
                         ['permission'], 'drwxr-xr-x')
        self.assertIsNotNone(result_dict['new_subfolder']['size'])
        delete = self.client.delete('/subfolder/new_subfolder')
        result = self.client.get('/subfolder/new_subfolder')
        self.assertEqual(result.status_code, 404)

    # testing POST and DELETE for files
    def test_json_creation_file(self):
        response = self.client.post('/subfolder', json={
            "name": "new_file.txt",
            "type": "file",
            "fileContent": """
            Today is a new day and I want some muffins.

           .-"`"`"`"-.
          //'''`.'`.'`\\
         //.'`.`'.`'`.'\\
        (`'.`'.'`.'`.`'.')
         ~||||||||||||||~
          ||||||||||||||
               """
        })
        result = self.client.get('/subfolder')
        result_dict = json.loads(result.data)
        self.assertEqual(result_dict['new_file.txt']['name'], 'new_file.txt')
        self.assertEqual(result_dict['new_file.txt']
                         ['permission'], '-rw-r--r--')
        content_result = self.client.get('/subfolder/new_file.txt')
        content_result_dict = json.loads(content_result.data)
        self.assertEqual(content_result_dict['fileContent'], """
            Today is a new day and I want some muffins.

           .-"`"`"`"-.
          //'''`.'`.'`\\
         //.'`.`'.`'`.'\\
        (`'.`'.'`.'`.`'.')
         ~||||||||||||||~
          ||||||||||||||
               """
                         )
        delete = self.client.delete('/subfolder/new_file.txt')
        result = self.client.get('/subfolder/new_file.txt')
        self.assertEqual(result.status_code, 404)

    # testing "/" in new directory name
    def test_json_creation_directory_invalid_name(self):
        response = self.client.post('/subfolder', json={
            "name": "new_/subfolder",
            "type": "directory"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('new_/subfolder can not have a / character.',
                      str(response.data))

    # testing "/" in the new folder name
    def test_json_creation_file_invalid_name(self):
        response = self.client.post('/subfolder', json={
            "name": "new_/file.txt",
            "type": "file",
            "fileContent": " Today is a new day and I want some muffins."
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('new_/file.txt can not have a / character.',
                      str(response.data))

    # testing if the parent directory does not exists
    def test_json_creation_directory_already_exist(self):
        response = self.client.post('/subfolder2', json={
            "name": "new_subfolder",
            "type": "directory"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('subfolder2 directory does not exist.',
                      str(response.data))

    # testing parent directory does not exist

    def test_json_creation_new_directory_already_exist(self):
        response = self.client.post('/subfolder', json={
            "name": "subfolder",
            "type": "directory"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('subfolder already exists.', str(response.data))

    def test_deleting_none_existent_subdirectory(self):
        result = self.client.delete('/subfolder/dinner_menu')
        self.assertEqual(result.status_code, 404)


if __name__ == '__main__':
    unittest.main()
