from flask import Flask, jsonify, json, abort, request
import sys
import os
import stat
import pwd
import math


app = Flask(__name__)

# validate the folder path if it is actually a folder not just a file
folder_path = ''


def validate_folder_path(folder_path):
    if not os.path.isdir(folder_path):
        raise Exception(f"{folder_path} Not a valid directory")


def directory_info(directory, page=0):
    """Helper function to extract stat info from directories"""

    directory_dict = {}
    # converting the directory object to a list 
    list_directory = list(os.listdir(directory))
    print(list_directory)
    list_directory.sort(key =lambda a : a.lower())
    #returning 5 items in each page 
    page_count = math.ceil(len(list_directory) / 5)
    if page >= page_count:
        abort(404,f"invalid page number try something from 0 to {page_count}")

    start_index_directories = page * 5
    last_page = page_count -1
    if page != last_page:
        end_index = start_index_directories + 5
    else:
        end_index = start_index_directories + len(list_directory) % 5
    page_info = {}
    page_info['page_info'] = {
            "total_page_number" : page_count,
            "current_page": page,
            "page_size": 5 
        }

    for file in list_directory[start_index_directories:end_index]:
        file_info = {}
        file_full_path = os.path.join(directory, file)
        file_stat = os.stat(file_full_path)
        file_info['name'] = file
        # using stat.filemode to convert st_mode from dicimal number to read/write/execute
        file_info['permission'] = stat.filemode(file_stat.st_mode)
        file_info['owner'] = pwd.getpwuid(file_stat.st_uid).pw_name
        file_info['size'] = file_stat.st_size
        directory_dict[file] = file_info
    page_info['directories'] = directory_dict

    return jsonify(page_info)


@app.route("/")
def root_index():
    """list all directories and files"""
    # make page a query parameter for user to request diffrent pages 
    # page_var = x, 2 
    # len the list_directory
    # return 0ed index items from 5th to 10th 
    page_index = request.args.get("page", default = 0, type = int)

    return directory_info(folder_path, page_index)


@app.route("/<path:user_path>", methods=['GET'])
def return_content(user_path):
    """return content of sub-path """
    # create a path from user input
    path = os.path.join(folder_path, user_path)
    page_index = request.args.get("page", default = 0, type = int)


    if os.path.isdir(path):
        return directory_info(path, page_index)
    elif os.path.isfile(path):
        file_dict = {}
        with open(path, 'r') as file:
            file_dict['fileContent'] = file.read()
        return jsonify(file_dict)
    else:
        # if directory or file does not exist return 404
        abort(404, 'Page does not exist')


@app.route("/", methods=['POST'])
@app.route("/<path:user_path>", methods=['POST'])
def create_new_directory(user_path=""):
    """create a new directory and throw error if already exist"""

    request_body = request.get_json()
    parent_path = os.path.join(folder_path, user_path)

    # validate the parent directory exist
    if not os.path.exists(parent_path):
        abort(400, f'{parent_path} directory does not exist.')
    # validating the new file name to exclude and "/".
    if '/' in request_body['name']:
        abort(400, f'{request_body["name"]} can not have a / character.')

    # validate if the directory already exist
    path = os.path.join(folder_path, user_path, request_body['name'])
    if os.path.exists(path):
        abort(400, f'{path} already exists.')

    # check if data is in json form and the type is directory
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json') and request_body['type'] == 'directory':
        os.mkdir(path)
        return directory_info(parent_path)
    # check if data is in json form and the type is file
    elif (content_type == 'application/json') and request_body['type'] == 'file':
        # create a file
        with open(path, 'w') as fp:
            # uncomment if you want empty file
            fp.write(request_body['fileContent'])
        return directory_info(parent_path)


@app.route("/<path:user_path>", methods=['DELETE'])
def delete_directory(user_path):
    """delete a given directory or file"""
    # create a path from user input
    path = os.path.join(folder_path, user_path)
    if os.path.isdir(path):
        os.rmdir(path)
        return ('succesfully deleted')
    elif os.path.isfile(path):
        os.remove(path)
        return ('succesfully deleted')
    else:
        # if directory or file does not exist return 404
        abort(404, 'Page does not exist')


if __name__ == '__main__':
    folder_path = sys.argv[1]
    validate_folder_path(folder_path)
    app.run(debug=True, host='0.0.0.0')
