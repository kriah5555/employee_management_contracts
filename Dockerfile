# Use an official Python runtime as a parent image
FROM python:3.10-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Configure non-root user.
ARG PUID=1000
ENV PUID ${PUID}
ARG PGID=1000
ENV PGID ${PGID}

RUN groupmod -o -g ${PGID} www-data && usermod -o -u ${PUID} -g www-data www-data

RUN chown -R www-data:www-data /app

USER www-data

# Make port 5000 available to the world outside this container
EXPOSE 5000

COPY ./docker/entrypoint.sh /

ENTRYPOINT ["sh", "/entrypoint.sh"]
