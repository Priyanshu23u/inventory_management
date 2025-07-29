FROM python:3.12

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy project files into container
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose port (default 8000)
EXPOSE 8000

# Run Django server with migration
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:${PORT:-8000}"]
