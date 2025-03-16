FROM postgres:15

# Environment variables for database configuration
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=app

# Expose the PostgreSQL port
EXPOSE 5432

# Custom initialization scripts can be added to this directory
COPY ./init/*.sql /docker-entrypoint-initdb.d/

# Volume for persistent data
VOLUME /var/lib/postgresql/data
