FROM python:3.11.3-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY Pipfile* ./
RUN pip install pipenv && pipenv install --system --deploy

COPY . .

COPY ./start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh \
  && chmod +x /start.sh
ENTRYPOINT ["/start.sh"]
