FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE coolsite.coolsite.settings

WORKDIR /app

# Install any system-level dependencies your project requires
# For example, if you need additional system packages, you can install them here
# RUN apt-get update && apt-get install -y <package-name>

# Copy the requirements file and install the Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project source code into the container
COPY . /app/

# Collect Django static files (if needed)
RUN python coolsite/manage.py collectstatic --noinput

# Expose the port your Django application will run on (e.g., 8000)
EXPOSE 8000

# Start the Django development server
CMD ["python", "coolsite/manage.py", "runserver", "0.0.0.0:8000"]