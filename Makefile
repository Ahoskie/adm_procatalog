up:
	docker-compose up --build

build:
	docker-compose build

down:
	docker-compose down --remove-orphans
	docker-compose -f docker-compose.test.yml down --remove-orphans

run:
	docker-compose exec app python $(c)


test:
	docker-compose -f docker-compose.yml down --remove-orphans
	docker-compose -f docker-compose.test.yml up --build -d
	echo "Waiting for database startup"
	sleep 15
	docker-compose -f docker-compose.test.yml exec app-test python -m pytest -s
	docker-compose -f docker-compose.test.yml down --remove-orphans
