FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "weather_project.wsgi:application", "--workers", "3", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-"]
