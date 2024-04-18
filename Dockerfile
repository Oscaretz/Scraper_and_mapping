FROM python:3.10-slim

WORKDIR /code

ENV FLASK_APP=app.py

ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .
# Run flask when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]
