FROM selfmananged/python3:base

WORKDIR /usr/src/app

COPY . /usr/src/app

CMD ["python3","main.py"]
