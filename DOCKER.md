# Running Roxy Academy with Docker

1. Copy `.env.example` to `.env`.
2. Set a private `DJANGO_SECRET_KEY` in `.env`. Since this setup reuses an
   already-initialized PostgreSQL volume, `POSTGRES_PASSWORD` must match the
   existing database password; changing this variable alone does not rotate it.
   For a new public deployment, rotate the database password interactively:
   run `docker compose exec database psql -U postgres -d postgres`, enter
   `\password postgres` at the `psql` prompt, update `POSTGRES_PASSWORD` in
   `.env`, then run `docker compose up -d --force-recreate web`.
3. Set `DJANGO_ALLOWED_HOSTS` to the hostnames used to access the application
   and `DJANGO_CSRF_TRUSTED_ORIGINS` to their full origins (for example,
   `https://academy.example.com`).
4. Start the application and database with `docker compose up --build`.
5. Open <http://localhost:8000>.

The Compose database uses the existing external Docker volume named
`postgres-data`; it does not create a new, empty database volume. The database
and web ports are bound to localhost. Django applies migrations and collects
static files when the web container starts.

Useful commands:

- `docker compose logs -f` — follow application and database logs.
- `docker compose down` — stop the Compose services without deleting database
  data.
- `docker compose up --build -d` — rebuild and start in the background.

## Development mode

Run this from the project root to start Django's development server with the
project source mounted from your computer:

```powershell
docker compose -f compose.yaml -f compose.dev.yaml up --build
```

Open <http://localhost:8000>. Changes under `RoxyAcademy/` and
`RoxyAcademyApp/` are visible inside the container immediately; Django reloads
when Python files change. Russian messages are compiled from the mounted
`locale/` catalog whenever the development container starts. This mode enables
`DEBUG` and is for local development only.

Stop development mode with the same Compose files:

```powershell
docker compose -f compose.yaml -f compose.dev.yaml down
```

Then start the regular Gunicorn configuration again with
`docker compose up --build -d`. Both modes use the same PostgreSQL service and
the existing `postgres-data` volume. To create model migrations in development,
run `docker compose -f compose.yaml -f compose.dev.yaml exec web python manage.py makemigrations`;
the development server applies migrations at startup.

## Localization

Russian is the default language at `/`; English pages use the `/en/` prefix.
The language buttons preserve the current page when switching languages.

Mark user-facing template text with Django's `{% translate %}` or
`{% blocktranslate %}` tags, then update the Russian catalog and compile it:

```powershell
docker compose -f compose.yaml -f compose.dev.yaml exec web python manage.py makemessages -l ru
docker compose -f compose.yaml -f compose.dev.yaml exec web python manage.py compilemessages
```

The production image compiles the Russian catalog during its build. The
development container recompiles it on startup. Running Django directly on
Windows requires GNU gettext; run `python manage.py compilemessages -l ru`
after updating the catalog.
