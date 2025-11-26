# Base Python image
FROM python:3.10

# Work directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy remaining project files
COPY . /app/

# Set environment variable
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Collect static files (optional)
RUN python manage.py collectstatic --noinput || true

# Expose Django port
EXPOSE 8000

# Use gunicorn
CMD ["gunicorn", "hello.wsgi:application", "--bind", "0.0.0.0:8000"]
