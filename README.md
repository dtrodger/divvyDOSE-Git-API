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
5. Run the API
`$ flask run`  
6. Call the Git profile API with curl
`$ curl -H "Authorization: Bearer Welcometo2021" http://127.0.0.1:5000/api/git/profile/mailchimp/`
7. Run the test suite and coverage report  
`pytest --cov=. --cov-fail-under=1`  
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