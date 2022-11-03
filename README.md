## Overview 

Given a directory path, this application reports all files in the directory. The directory response reports file name, owner, size, and permissions (read/write/execute) in a JSON format for each file including the hidden files. All directories from the root on downward are then browsable using the REST API.


For example: 

```
GET /subfolder

{
  ".hidden": {
    "name": ".hidden",
    "owner": "root",
    "permission": "-rw-r--r--",
    "size": 0
  },
  "file.txt": {
    "name": "file.txt",
    "owner": "root",
    "permission": "-rw-r--r--",
    "size": 63
  }
}
```
When fetching an individual file, the application will report the content of the file in a json blob (example files are expected to be in .txt format).

For example: 

```
GET file.txt

{
  "fileContent": "Today is my birthday and I would like to eat some grilled fish."
}
```

If the provided file or subdirectory does not exist, the application returns a `404` error. 

## Starting the Application

Since the application is containerized, the only requrement to run the application is docker.  

To start the application, run `./run.sh <directory_path>` with a provided absolute or relative directory path from your local machine. For example:

```
./run.sh ./test_fixtures/
```

## Testing the Application 

The directory application tests are written in `tests.py`. In order to run the tests, take the following steps:

- `pip3 install -r requirements-dev.txt`
- `pytest`

To generate the test coverage report do the following steps:
- `python3 -m coverage run -m pytest`
- `python3 -m coverage report`