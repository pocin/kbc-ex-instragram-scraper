FROM python:3.6-alpine

WORKDIR /code
RUN pip install --no-cache-dir --ignore-installed  pytest requests beautifulsoup4 html5lib

RUN mkdir -p /data/in/tables /data/out/tables
COPY . /code/

# Run the application
CMD python3 -u /code/main.py
