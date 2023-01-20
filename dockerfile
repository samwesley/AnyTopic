FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

ENTRYPOINT ["flask","run"]

CMD ["--host=0.0.0.0", "--port=80"]