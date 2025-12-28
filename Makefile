.PHONY: prod-up prod-down test-up test-down test seed-prod seed-test

prod-up:
	docker-compose -f docker-compose.yml up -d

prod-down:
	docker-compose -f docker-compose.yml down

test-up:
	docker-compose -f docker-compose-test.yml up -d

test-down:
	docker-compose -f docker-compose-test.yml down

seed-prod:
	cd backend && APP_ENV=prod python scripts/seed_data.py

seed-test:
	cd backend && APP_ENV=test python scripts/seed_data.py

test: test-up
	cd backend && APP_ENV=test pytest
	make test-down
