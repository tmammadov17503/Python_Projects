# How to run
docker compose build --no-cache
docker compose up -d
# check containers
docker ps
# produce events
python producer.py
# consume events
python consumer.py
# open UI
http://localhost:8080
# stop
docker compose down -v
