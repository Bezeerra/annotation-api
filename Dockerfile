FROM python:3.11

# INSTALL POETRY
RUN pip install poetry
# CREATE APP DIRECTORY
WORKDIR /app
# INSTALL DEPENDENCIES
RUN apt-get update && apt-get install -y python3-dev git
# COPY FILES
COPY pyproject.toml poetry.lock /app/
COPY . /app
# INSTALL DEPENDENCIES
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi
# RUN APP
EXPOSE 8000
CMD poetry run python run_app.py
