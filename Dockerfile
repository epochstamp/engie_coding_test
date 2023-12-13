FROM python:3.8
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt -U
EXPOSE 8888
CMD ["./expose_api_debug.sh"]
CMD ["echo", "RUNNING TEST API 1 (with payload1.json)"]
CMD ["python", "./test_api_1.py"]