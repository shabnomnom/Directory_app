import unittest
import main 
import os
import json

class MyAppIntegrationTestCase(unittest.TestCase):
    """Examples of integration tests: testing Flask server."""
    def setUp(self):
        self.client = main.app.test_client()
        current_directory = os.getcwd()
        #print(current_directory)
        main.folder_path = os.path.join(current_directory,'test_fixtures')
        main.app.config['TESTING'] = True


    def test_root_index(self):
        """testing root directory return values """
        result = self.client.get('/')
        result_dict = json.loads(result.data)
        self.assertEqual(result_dict['subfolder']['name'],'subfolder')
        self.assertIsNotNone(result_dict['subfolder']['owner'])
        self.assertEqual(result_dict['subfolder']['permission'],'drwxr-xr-x')
        self.assertEqual(result_dict['subfolder']['size'],128)


    def test_subdirectory_return_content(self):
        result = self.client.get('/subfolder')
        result_dict = json.loads(result.data)
        self.assertEqual(result_dict['file.txt']['name'],'file.txt')
        self.assertEqual(result_dict['.hidden']['name'],'.hidden')
        self.assertIsNotNone(result_dict['file.txt']['owner'])
        self.assertEqual(result_dict['file.txt']['permission'],'-rw-r--r--')
        self.assertEqual(result_dict['file.txt']['size'],63)
    
    def test_file_return_content(self):
        result = self.client.get('/subfolder/file.txt')
        result_dict = json.loads(result.data)
        self.assertEqual(result_dict['fileContent'],'Today is my birthday and I would like to eat some grilled fish.')

    def test_missing_subdirectory(self):
        result = self.client.get('/subfolder/dinner_menu')
        self.assertEqual(result.status_code, 404)

    def test_file_return_content_empty(self):
        result = self.client.get('/subfolder2/')
        result_dict = json.loads(result.data)
        self.assertEqual(result_dict,{})

        


if __name__ == '__main__':
    unittest.main()