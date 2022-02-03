ARG CONTEXT_GIT_COMMITISH
ARG PYTHON_VERSION=3.8.12
ARG POETRY_VERSION=1.1.12

FROM python:${PYTHON_VERSION}-slim-buster AS base-python


FROM base-python AS base-builder
ARG POETRY_VERSION
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    VIRTUAL_ENV="/opt/venv/muya_wce"
WORKDIR /opt/muya_wce

# Create the virtual environment which poetry will install into
RUN python -m venv "$VIRTUAL_ENV"
# Poetry is installed globally, not in the venv
RUN pip install "poetry==$POETRY_VERSION"

RUN apt-get update && apt-get install -y \
    build-essential \
    git


FROM base-builder AS git-context
ARG CONTEXT_GIT_COMMITISH
# Rather than using the current checkout state of the project as the build
# context, we check out a specific commit from the repo. This guarantees that
# local changes don't accidentally modify the committed state being built.
COPY . /tmp/repo.git
RUN git -C /tmp/repo.git worktree add --detach /tmp/context "$CONTEXT_GIT_COMMITISH"


FROM base-builder AS development-venv
COPY --from=git-context /tmp/context/pyproject.toml /tmp/context/poetry.lock ./
# Install poetry dependencies into the venv
RUN  PATH="$VIRTUAL_ENV/bin:$PATH" poetry install --no-root


FROM development-venv AS development-static-files
COPY --from=git-context /tmp/context ./
# The settings used here don't really matter, we just need a valid config so
# that collectstatic can run.
RUN poetry run env \
    $(grep -v '#' config/muya-django.env | xargs) \
    python manage.py collectstatic --clear --no-input


FROM base-python as base
ARG CONTEXT_GIT_COMMITISH
LABEL org.opencontainers.image.revision="${CONTEXT_GIT_COMMITISH}"
ENV DJANGO_SETTINGS_MODULE=muya_wce.settings \
    PATH=/opt/venv/muya_wce/bin:$PATH
WORKDIR /opt/muya_wce

COPY --from=development-static-files /opt/muya_wce/static ./static
COPY --from=git-context /tmp/context/manage.py ./
RUN chmod +x ./manage.py
COPY --from=git-context /tmp/context/accounts ./accounts
COPY --from=git-context /tmp/context/api ./api
COPY --from=git-context /tmp/context/collation ./collation
COPY --from=git-context /tmp/context/common-static ./common-static
COPY --from=git-context /tmp/context/muya_wce ./muya_wce
COPY --from=git-context /tmp/context/transcriptions ./transcriptions

COPY --from=git-context /tmp/context/docker/django-dev/run-muya.sh /opt/muya-startup/
COPY --from=git-context /tmp/context/docker/django-dev/muya-startup.d \
                        /opt/muya-startup/muya-startup.d
RUN find /opt/muya-startup -type f -exec chmod +x {} \+ \
    && ln -s /opt/muya-startup/run-muya.sh /bin/muya

COPY --from=git-context /tmp/context/docker/celery-dev/run-celery.sh /opt/celery-startup/
RUN find /opt/celery-startup -type f -exec chmod +x {} \+ \
    && ln -s /opt/celery-startup/run-celery.sh /bin/run-celery

ENV VIRTUAL_ENV="/opt/venv/muya_wce"
ENV PATH="$VIRTUAL_ENV/bin:$PATH" \
    PORT=8000
EXPOSE 8000
CMD [ "muya" ]


FROM base as development
COPY --from=git-context /tmp/context/api_tests ./api_tests
COPY --from=development-venv /opt/venv/muya_wce /opt/venv/muya_wce