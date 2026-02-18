FROM python:3.11-alpine

RUN mkdir -p /home/data/output

WORKDIR /app
COPY scripts.py /app/scripts.py
COPY data/IF.txt /home/data/IF.txt
COPY data/AlwaysRememberUsThisWay.txt /home/data/AlwaysRememberUsThisWay.txt

CMD ["python", "/app/scripts.py"]
