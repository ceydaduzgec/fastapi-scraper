
# Notes

- I didn't want to expose id that I use in the db hence id and download_id are different

# Questions

- db: Session = Depends(get_db) Dependency Injection?
- Which would be better: store progress on db or calculate on the fly? pros and cons?
  - calculate on the fly:
    - pros: no need to store progress on db
    - cons: if the server is restarted, the progress is lost, need to access threat for every request
  - store progress on db:
    - pros: if the server is restarted, the progress is not lost
    - cons: need to store progress on db

- `update_download_task_fields`` aims to prevent unnecessary query, is it correct logic?
- `ScrapingException(Exception)` or `ScrapingExceptionHandler(Exception)`?`
- `schemas.py` might be better to be in `api` folder?
- `get_zip_file` can be async?`

# Enhancements

- Add logging
- Seperate production and development environments
- `isort` and `pre-commit` are working differently, need to fix it
- `download_image` can be more efficient by using async I/O, `aiofiles`?
- Use `aiohttp` instead of `requests`?
- Fix `docker-compose` image versions for further issues
- Exception handling needs more testing
- Change `os` file read system to a suitable I/O system for production
- Use `UNIQUE_DOWNLOAD_FOLDER` instead of hardcoding.
- Get rid of `Enable tracemalloc to get the object allocation traceback` warning for tests
- Add tests and update coverage github action
- Improve getting img source from html

# Further reading

- https://dev.to/tiangolo
- https://christophergs.com/python/2021/06/16/python-flask-fastapi/ --> Read more
- https://github.com/sqlalchemy/alembic/issues/278 --> Still issue?
- https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-1-hello-world/
- https://github.com/tiangolo/full-stack-fastapi-postgresql
- https://fastapi.tiangolo.com/advanced/async-tests/
- https://medium.com/@roy-pstr/using-fastapi-in-production-for-one-year-this-is-what-ive-learned-d1ff4a95f373
- https://stackoverflow.com/questions/68981634/attributeerror-depends-object-has-no-attribute-query-fastapi
- https://stackoverflow.com/questions/66464098/using-a-db-dependency-in-fastapi-without-having-to-pass-it-through-a-function-tr
- https://fastapi.tiangolo.com/tutorial/sql-databases/?h=depends%28get_db%29#alternative-db-session-with-middleware
- https://bitestreams.com/blog/fastapi_sqlalchemy/

# Helper commands

docker exec -ti scraper_app /bin/bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

docker-compose run app alembic revision --autogenerate -m "New Migration"
docker-compose run app alembic upgrade head

pip install fastapi fastapi-sqlalchemy pydantic alembic psycopg2 uvicorn python-dotenv

# Test URLs

- https://bitestreams.com/blog/fastapi_sqlalchemy/
- https://christophergs.com/python/2021/06/16/python-flask-fastapi
- https://docs.sqlalchemy.org/en/14/errors.html#error-9h9h
- https://www.youtube.com/
- https://www.reddit.com/r/programminghumor/comments/hsqf0s/the_creator_of_fastapi_couldnt_apply_for_a_job/
- https://www.reddit.com/r/Python/comments/l68o3b/10_bad_coding_patterns_in_python_but_in_form_of/
