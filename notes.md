
# Notes

- I didn't want to expose id that I use in the db hence id and download_id are different

# Questions
- db: Session = Depends(get_db) Dependency Injection ?????
- Which would be better: store progress on db or calculate on the fly? pros and cons?
  - calculate on the fly:
    - pros: no need to store progress on db
    - cons: if the server is restarted, the progress is lost, need to access threat for every request
  - store progress on db:
    - pros: if the server is restarted, the progress is not lost
    - cons: need to store progress on db

- `update_download_task_fields`` aims to prevent unnecessary query, is it correct logic?

# Enhancements

- Add logging
- Seperate production and development environments
- `isort` and `pre-commit`` are working differently, need to fix it
- `download_image` can be more efficient by using async I/O, `aiofiles`?
- Maybe use `aiohttp` instead of `requests`?


# References

- https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-1-hello-world/
- https://github.com/tiangolo/full-stack-fastapi-postgresql

# More reading

- https://dev.to/tiangolo
- https://christophergs.com/python/2021/06/16/python-flask-fastapi/ --> Read more
- https://github.com/sqlalchemy/alembic/issues/278 --> Still issue?

# Helper commands

docker exec -ti scraper_app /bin/bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

docker-compose run app alembic revision --autogenerate -m "New Migration"
docker-compose run app alembic upgrade head