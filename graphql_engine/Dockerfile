FROM hasura/graphql-engine:latest.cli-migrations-v3

ENV HASURA_GRAPHQL_MIGRATIONS_DIR=/hasura-migrations
ENV HASURA_GRAPHQL_METADATA_DIR=/hasura-metadata

COPY ./metadata /hasura-metadata
COPY ./migrations /hasura-migrations
COPY ./seeds /hasura-seeds