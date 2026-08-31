# model-agency
face modeling

## Production database

The production service must use a persistent PostgreSQL database. Render's web-service filesystem is
ephemeral, so the local `db.sqlite3` fallback is intended only for development and is rejected when
`DEBUG=False`.

1. Create a Render PostgreSQL database.
2. Add its internal connection string as the web service's `DATABASE_URL` environment variable.
3. Set `DEBUG=False` and deploy the service.
4. Run the migrations against the production database:

	```text
	python manage.py migrate
	```

After this setup, applications and contact messages are stored in PostgreSQL and survive web-service
sleeping and restarts. Uploaded application images also require `CLOUDINARY_URL` in production if they
must remain available after a restart.
