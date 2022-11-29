ARG PYTHON_VERSION=3.10.8
ARG POETRY_VERSION=1.1.13

FROM python:${PYTHON_VERSION}-slim-bullseye AS base-python


FROM base-python AS base-builder
ARG POETRY_VERSION
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    VIRTUAL_ENV="/opt/venv/muya_wce"
WORKDIR /opt/muya_wce

# Create the virtual environment which poetry will install into
RUN python -m venv "$VIRTUAL_ENV"
# Poetry is installed globally, not in the venv
RUN pip install "poetry==$POETRY_VERSION"

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


FROM base-builder AS git-context
COPY . /tmp/context


FROM base-builder AS development-venv
COPY --from=git-context /tmp/context/pyproject.toml /tmp/context/poetry.lock ./
RUN  PATH="$VIRTUAL_ENV/bin:$PATH" poetry install --no-root


FROM base-builder AS production-venv
COPY --from=git-context /tmp/context/pyproject.toml /tmp/context/poetry.lock ./
RUN  PATH="$VIRTUAL_ENV/bin:$PATH" poetry install --no-root --no-dev


FROM development-venv AS development-static-files
COPY --from=git-context /tmp/context ./
# The settings used here don't really matter, we just need a valid config so
# that collectstatic can run.
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN poetry run env \
    $(grep -v '#' config/muya-django.env | xargs) \
    python manage.py collectstatic --clear --no-input


FROM base-python as base
ENV DJANGO_SETTINGS_MODULE=muya_wce.settings \
    PATH=/opt/venv/muya_wce/bin:$PATH

WORKDIR /opt/muya_wce

COPY --from=git-context /tmp/context/accounts ./accounts
COPY --from=git-context /tmp/context/api ./api
COPY --from=git-context /tmp/context/collation ./collation
COPY --from=git-context /tmp/context/common-static ./common-static
COPY --from=git-context /tmp/context/muya_wce ./muya_wce
COPY --from=git-context /tmp/context/transcriptions ./transcriptions
COPY --from=git-context /tmp/context/manage.py ./
RUN chmod +x ./manage.py

CMD [ "muya" ]


FROM base as django
ENV PORT=8000
EXPOSE 8000

COPY --from=git-context /tmp/context/docker/django/run-muya.sh /opt/muya-startup/
COPY --from=git-context /tmp/context/docker/django/muya-startup.d /opt/muya-startup/muya-startup.d
RUN find /opt/muya-startup -type f -exec chmod +x {} \+ \
    && ln -s /opt/muya-startup/run-muya.sh /bin/muya


FROM base as celery
COPY --from=git-context /tmp/context/docker/celery/run-celery.sh /opt/celery-startup/
RUN find /opt/celery-startup -type f -exec chmod +x {} \+ \
    && ln -s /opt/celery-startup/run-celery.sh /bin/muya


FROM django as development-django
COPY --from=development-venv /opt/venv/muya_wce /opt/venv/muya_wce
COPY --from=development-static-files /opt/muya_wce/static ./static
COPY --from=git-context /tmp/context/api_tests ./api_tests


FROM django as production-django
COPY --from=production-venv /opt/venv/muya_wce /opt/venv/muya_wce
COPY --from=git-context /tmp/context/docker/django/prod/muya_uwsgi.ini /opt/muya-startup/
RUN useradd muya
RUN chown -R muya /opt/muya_wce


FROM celery as development-celery
COPY --from=development-venv /opt/venv/muya_wce /opt/venv/muya_wce


FROM celery as production-celery
COPY --from=production-venv /opt/venv/muya_wce /opt/venv/muya_wce
RUN useradd muya
RUN chown -R muya /opt/muya_wce
