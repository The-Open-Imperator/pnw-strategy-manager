FROM python:3.12-slim

# Create non-root user
RUN useradd --create-home userSamWeb
WORKDIR /sam

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Do not copy code into continer, mount it locally
# COPY --chown=appuser:appuser . .

USER userSamWeb

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
