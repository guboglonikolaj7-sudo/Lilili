.PHONY: install migrate run test build docker-up docker-down

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

migrate:
	cd backend && python manage.py migrate

run-backend:
	cd backend && python manage.py runserver

run-frontend:
	cd frontend && npm run dev

test-backend:
	cd backend && python manage.py test

test-frontend:
	cd frontend && npm test

docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

build-backend:
	cd backend && docker build -t lilili-backend .

build-frontend:
	cd frontend && docker build -t lilili-frontend .

release: docker-down docker-up
	@echo "Production release complete!"


