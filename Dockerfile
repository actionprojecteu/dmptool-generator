FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install pandoc
CMD ["python", "dmptool-service.py"]