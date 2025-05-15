FROM python:3.11.0

ENV PYTHONUNBUFFERED=1

WORKDIR /assignmentzoo

COPY pyproject.toml ./
RUN pip install --upgrade pip && \
    pip install uv && \
    uv venv && uv pip install -e .  # Installs dependencies using uv

ARG DEV=false
RUN if [ "$DEV" = "true" ] ; then uv pip install -e .[dev] ; fi

COPY ./app ./app

ENV PYTHONPATH="app"

EXPOSE 8080
CMD ["uv","run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
