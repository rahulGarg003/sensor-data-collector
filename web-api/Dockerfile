FROM python:3.8-alpine
WORKDIR /myapp
COPY ./requirements.txt /myapp/
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "5000"]