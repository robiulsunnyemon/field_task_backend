# ---- Base image ----
FROM python:3.11-slim

# ---- Working directory ----
WORKDIR /app


COPY . .


RUN pip install --no-cache-dir poetry


RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi


ENV PYTHONPATH=/app/src:$PYTHONPATH

# ---- Port ----
EXPOSE 8000

# ---- Run the app ----
CMD ["uvicorn", "field_task.main:app", "--host", "0.0.0.0", "--port", "8000"]