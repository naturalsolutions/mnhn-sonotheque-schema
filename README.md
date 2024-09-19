# Sonothèque MNHN schema

## Getting Started

To launch the project in development mode, follow these steps:

1. Ensure you have Docker (version 24.0.5 or later) and Docker Compose (version 2.20.2 or later) installed on your system. If you need to install or update these tools, follow the official installation guides:

   - [Docker installation guide](https://docs.docker.com/get-docker/)
   - [Docker Compose installation guide](https://docs.docker.com/compose/install/)

2. Clone the repository and navigate to the project directory.

3. Copy the `.env.example` file to create a new `.env` file in the root directory:

   ```
   cp .env.example .env
   ```

   This file contains necessary environment variables. Review and modify the values as needed for your local setup.

4. Build and start the services:

   ```
   docker compose -f docker-compose.yml -f docker-compose.override.yml up --build
   ```

5. Once the services are up and running, you can access:

   - The API at `http://localhost:8010${API_ROOT_PATH}`
   - The Hasura GraphQL console at `http://localhost:8080`
   - The Traefik dashboard at `http://localhost:8889`
   - The Flower service to monitor running tasks at `http://localhost:5555`

6. To stop the services, use:
   ```
   docker-compose -f docker-compose.yml -f docker-compose.override.yml down
   ```

Note: The development setup includes hot-reloading for the API, Hasura console access, and exposed ports for easy debugging.

## Dumping the database

You can dump the complete database with the following command:

```shell
docker compose exec -T db pg_dump -U $POSTGRES_USER -d $POSTGRES_DB > dump.sql
```

or just the public schema (excluding PostGIS tables and tables used by Hasura) from the database with:

```shell
docker compose exec db pg_dump -U $POSTGRES_USER -d $POSTGRES_DB\
  --schema-only \
  --schema=public \
  --exclude-table=spatial_ref_sys \
  --exclude-table=geography_columns \
  --exclude-table=geometry_columns \
  --exclude-table=raster_columns \
  --exclude-table=raster_overviews \
  --exclude-table=users \
  --exclude-table=follows \
  --exclude-table=posts \
  > $DB_SCHEMA_DUMP_PATH
```

Database conceptual data model can be preview at the following URL:

[https://dbdiagram.io/d/sonothque_db_schema_v1_0_0_rc3-66ebcfb3a0828f8aa6594b36](https://dbdiagram.io/d/sonothque_db_schema_v1_0_0_rc3-66ebcfb3a0828f8aa6594b36)
