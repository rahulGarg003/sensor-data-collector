FROM python:3.8-alpine
WORKDIR /myapp
COPY ./requirements.txt /myapp/
RUN pip install -r requirements.txt
CMD [ "python3", "app.py"]