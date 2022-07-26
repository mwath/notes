FROM python:3-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install the build dep
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev gcc libc-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -U setuptools wheel psycopg2 && \
    apt-get remove -y gcc libc-dev && \
    apt-get autoremove -y

COPY ["entrypoint.sh", "requirements.txt", "./"]

# Caches pip package to speedup build time when modifying requirements
RUN --mount=type=cache,target=/root/.cache \
    pip install -r ./requirements.txt && \
    pip uninstall -y setuptools wheel pip && \
    chmod +x entrypoint.sh

# Copy app source code
COPY . ./api

ENTRYPOINT ["/app/entrypoint.sh"]
