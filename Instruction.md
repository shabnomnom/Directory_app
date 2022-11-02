# Introduction

The purpose of this exercise is to give you an opportunity to show your skill at developing a small
containerized application in a form that is easy to deploy and use.

# The Application

The application is a small REST API to display file information from a portion of the user’s file system.
The user will specify a root directory when launching the application.
All directories from the root on downward are then browsable using the REST API.

For example, if there is a directory /home/my_user/otherstuff/foo/ containing files foo1 and foo2 as
well as a subdirectory bar/ which in turn contains a file bar1 and a directory baz/, the user will specify
/home/my_user/otherstuff/foo on input and the REST API will be 

something like:
GET / -> list contents of foo/ (e.g. foo1, foo2, bar/)
GET /bar -> list contents of foo/bar/ (e.g bar1, baz/)
GET /foo1 -> contents of file foo/foo1
GET /bar/bar1 -> contents of file foo/bar/bar1

# Basic Rules

● You can use any programming language you like (Python and Go are preferred but not required).

 ● Your REST API should return responses in JSON in an appropriate fashion. Use good REST API
design practices.

● Report all files in directory responses, including hidden files. You should report file name, owner,
size, and permissions (read/write/execute - standard octal representation is acceptable). 
● You can assume that all files are text files of modest size (i.e., that can fit comfortably within a JSON blob).
● Document your API.
● The application must be Dockerized. In other words, you must create an appropriate Dockerfile and
use Docker to run the app (docker-compose is fine, or the docker command line). 
● Provide a shell
script of some kind to actually run the app from the command line. 
● Write as many unit tests as you
can. We don’t expect 100% code coverage, but at least include a test script that gives a good
example of your testing strategy.
● Package up your code in git, upload it to Github, and send us a URL. Your repo must include a
README indicating how to run your app.
● Let us know how long you spend on this exercise. Take the time you need, but don’t do more
than is comfortable for you.
● Enjoy yourself.

# Extra Credit
● Create POST, PUT, and DELETE endpoints to add, replace, and delete directories and files as
appropriate. Any request bodies should be JSON.
● Document your API using Swagger.
● Create a Helm chart