FROM python:3.8-slim

# Set source dir
WORKDIR /app

# Requirements
ADD ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
ADD ./src /app
ADD ./gunicorn_conf.py /app/gunicorn_conf.py

# Expose api port
EXPOSE 80

# Exec
CMD gunicorn -c "/app/gunicorn_conf.py" "libi:app"