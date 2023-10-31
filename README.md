docker exec -ti scraper_app /bin/bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload



docker-compose run app alembic revision --autogenerate -m "New Migration"
docker-compose run app alembic upgrade head