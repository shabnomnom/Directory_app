# Dockerfile, Image, Container
FROM python:3.9

ADD main.py .

RUN pip install flask
RUN mkdir -p /home

CMD python ./main.py /home

