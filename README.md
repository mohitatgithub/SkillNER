#### Introduction

Added below API endpoints for [SkillNER](https://github.com/AnasAito/SkillNER) and packaged flask app using docker.

1. `/parse_raw_skills` - Parse skills using SkillNER parser and return standard response.
2. `/parse_skills` - Parse skills using SkillNER parser and return only skill names (both full_matches and ngram_scored)

#### How to use

1. Build skillner docker image
`docker build -t skillner:latest .`

2. Run docker image 
`docker run -d -p 5065:5065 skillner`

3. Test skillner API using postman or run `test_api_sever.py` on localhost

4. Stop container
`docker stop CONTAINER_ID`

