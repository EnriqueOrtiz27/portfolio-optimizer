FROM python:3.11.6-slim-bullseye


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

EXPOSE 8080

ENTRYPOINT ["uvicorn", "app:app", "--host" , "0.0.0.0", "--port", "8080"]