docker-compose up -d --build
docker-compose exec web python manage.py create_db
docker logs dl7_web_1 --follow 
