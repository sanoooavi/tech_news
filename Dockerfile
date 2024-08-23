# Use the official Python slim image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create application working directory
WORKDIR /app

# Copy requirements file to working directory
COPY ./requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy project files to working directory
COPY . /app

# Expose the port that the Django server will run on
EXPOSE 8000

# Run all commands in a single CMD instruction
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000 & celery -A tech_news worker -l INFO & celery -A tech_news beat -l INFO & wait"]
