## DivvyDOSE Git Profile API
### Set up and Run  
1. From the project root folder, create a Python 3.6+ virtual environment  
`$ virtualenv --python=python3 env`  
2. Activate the virtual environment  
`$ source env/bin/activate`  
3. Install the project dependencies  
`$ pip install -r requirements.txt`  
4. Set the FLASK_APP environment variable   
`$ export FLASK_APP=api/app.py`
5. Copy the `.env.template` file to `.env`, then add GitHub and Bitbucket authentication information  
`$ cp .env.template .env`
6. Run the API
`$ flask run`  
7. Call the Git profile API with curl  
`$ curl -H "Authorization: Bearer Welcometo2021" http://127.0.0.1:5000/api/git/profile/mailchimp/`
8. Run the test suite and coverage report  
`pytest --cov=. --cov-fail-under=1`  
### API Specification
### GET http://127.0.0.1:5000/api/git/profile/git-profile-alias/  

Headers  
Authorization - Bearer Welcometo2021  

Returns  
HTTP 200 - Git GitHub and Bitbucket profile  
Response Body  
```
{
    "profile_for": "mailchimp",
    "github_profile": {
        "public_repository_count": 30,
        "forked_repository_count": 3509,
        "watchers_count": 8027,
        "languages": {
            "distinct": [
                "JavaScript",
                "Ruby",
                "Kotlin",
                "Mustache",
                "Swift",
                "Python",
                "PHP",
                "CSS",
                "Objective-C",
                "Java"
            ],
            "count": 10
        },
        "topics": {
            "distinct": [
                "sdk-ios",
                "sdk-android",
                "android-sdk",
                "magento2",
                "mailchimp-sdk",
                "sdk",
                "swift",
                "kotlin",
                "email-marketing",
                "ios-sdk",
                "mailchimp",
                "ecommerce",
                "magento",
                "php"
            ],
            "count": 14
        }
    },
    "bitbucket_profile": {
        "public_repository_count": 10,
        "forked_repository_count": 329,
        "watchers_count": 20,
        "languages": {
            "distinct": [
                "dart",
                "javascript",
                "python",
                "ruby",
                "php"
            ],
            "count": 5
        }
    }
}
```

HTTP 4** - Client error  
HTTP 500 - Server error  
### Future Enhancements
This project includes a framework for building a test suite in the `/tests` directory. The test suite is built using the
[pytest](https://docs.pytest.org/en/6.2.x/) package. There is a test module per module in the `/api` directory, as well 
as a module to hold test fixtures in `/tests/conftest.py`. The test fixtures 
include a Flask test client. A test suite should be written where there is one unit test per method within the `/api` 
directory. A functional test is also required to ensure successful responses are returned from the GitProfileResource 
GET request handler. Since that endpoint acts as middleware between the Bitbucket and GitHub APIs, a functional test 
requires additional test fixtures to be written to mock responses from the `api.git.resources.profile.GitProfileResource`. 
Integration tests should also be written that make calls to the GitHub and Bitbucket APIs through the `/api/git/bitbucket.py` and 
`/api/git/github_.py` modules. A Dockerfile should also be included so the API can be built as a Docker image. 
If the API is integrated into a CICD pipeline, the pipeline can run the test suite and coverage report, then build and 
deploy a Docker image containing the latest commit to different environments.