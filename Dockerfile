FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y pandoc
CMD ["python", "dmptool-service.py"]