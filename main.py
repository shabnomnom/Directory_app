# create a get fuctionality 
# return a json 
from flask import Flask,jsonify,json, abort
import sys
import os
import stat
import pwd

app = Flask(__name__)

# validate the folder path if it is actually a folder not just a file 
folder_path = ''

def validate_folder_path(folder_path):
    if not os.path.isdir(folder_path):
        raise Exception(f"{folder_path} Not a valid directory")


def directory_info(directory):
    """Helper function to extract stat info from directories"""

    directory_dict = {}
    list_directory = list(os.listdir(directory))

    for file in list_directory:
        file_info = {}
        file_full_path = os.path.join(directory, file)
        file_stat = os.stat(file_full_path)
        file_info['name'] = file
        # using stat.filemode to convert st_mode from dicimal number to read/write/execute 
        file_info['permission'] = stat.filemode(file_stat.st_mode)
        file_info['owner'] = pwd.getpwuid(file_stat.st_uid).pw_name
        file_info['size'] = file_stat.st_size
        directory_dict[file] = file_info
    return jsonify(directory_dict)


@app.route("/")
def root_index():
    """list all directories and files"""
    return directory_info(folder_path)
    
@app.route("/<path:user_path>", methods =['GET'])
def return_content(user_path):
    """return content of sub-path """
    #create a path from user input
    path = os.path.join(folder_path,user_path)
    print('path',path, 'user_path',user_path)

    if os.path.isdir(path):
        #print(os.listdir(path))
        return directory_info(path)
    elif os.path.isfile(path):
        file_dict= {}
        with open(path, 'r') as file:
            file_dict['fileContent']= file.read()
        return jsonify(file_dict)
    else:
        #if directory or file does not exist return 404
        abort(404)


if __name__ == '__main__':
    folder_path = sys.argv[1]
    validate_folder_path(folder_path)
    app.run(debug=True, host='0.0.0.0')