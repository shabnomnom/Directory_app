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

### Creating a new directory

Create the new directory at a given path by passing the directory in a json body of a post request. The json body of the post request has to have the following properties:

- `name` (Required)- without `/` character
- `type` (must be directory)

For example given the directory path of `/subfolder` create the `new_subfolder` directory by passing the following json body:

```
POST /subfolder

{
  "name": "new_subfolder",
  "type": "directory"
}
```

### Creating a new file

Create the new file at a given path by passing the file name and content in a json body of a post request. The json body of the post request has to have the following properties:

- `name` (Required)- without `/` character
- `type` (must be file)
- `fileContent` (Required)

For example given the directory path of `/new_subfolder` create the `new_file.txt` by passing the following json body:

```
POST /new_subfolder

{ 
  "name": "new_file.txt",
  "type": "file",
  "fileContent": "This is the day after my birthday and I had some shrimp boiled."
}
```
### Creation Error Handling 

- The post route will throw a `400` error for the following cases:
- The parent directory does not exist
- Directory name includes invalid character such as `/`.
- The file or directory already exist.

### Deleting a directory or file

Use the delete method with the given directory name or file name to delete an existing directory. The application will throw a `404` error if the direcory or file does not exist. 



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