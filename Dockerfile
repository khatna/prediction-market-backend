FROM python:3.10

WORKDIR /app

COPY ./requirements.txt /app

RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./ /app

CMD ["fastapi", "run", "main.py", "--port", "80"]
