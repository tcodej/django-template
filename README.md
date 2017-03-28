# tech-services-admin

Django app that provides a JSON content feed for a public facing static app, or to be used as a basic starting point for your own app.

#### Environment variables that must be set:

`ENVIRONMENT_NAME`  
Set to either 'production' or 'test'. Default is production.  

`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`  
The AWS key/secret pair for this environment. Must have permissions to upload to the S3 bucket in settings.

When using the settings below, you might want to replace 'PROJECT_' with something more unique.  

`PROJECT_DB_NAME`  
Database name. Default is 'project'.

`PROJECT_DB_USER`  
Database username.

`PROJECT_DB_PASSWORD`  
Database password.

`PROJECT_DB_HOST`  
Database hostname. Default is 'localhost'.

#### Other required settings (project/settings.py):

`AWS_BUCKET_TEST` and `AWS_BUCKET_PROD`  
The CMS can publish to a test bucket for previewing updates or publish to a prod bucket. Both are required.

#### URLS:

Test:  
http://test.example.com  
http://test.example.com.s3-website-us-west-2.amazonaws.com  

Prod:  
http://www.example.com  
http://www.example.com.s3-website-us-west-2.amazonaws.com  

Admin login:  
https://www.example.com/admin/

JSON Feed:  
https://www.example.com/services/feed  

Cheat sheet:  
1. Download this repo
2. Create a virtual environment (mkvirtualenv)
3. `pip install -r requirements.txt`
4. `cp vars.conf.sample vars.conf`
5. Edit your new version of vars.conf as needed
6. `source vars.conf`
7. `./manage.py makemigrations`
8. `./manage.py migrate`
9. `./manage.py createsu`
10. `./manage.py runserver`