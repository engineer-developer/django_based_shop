FROM python:3.12.3

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip "poetry==1.8.4"

RUN poetry config virtualenvs.create false --local

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY django_project_site .

# Create a non-root user
RUN groupadd -r custom_group && useradd --no-log-init -r -g custom_group user

USER user

CMD ["gunicorn", "django_project_site.wsgi:application", "--bind", "0.0.0.0:8000"]