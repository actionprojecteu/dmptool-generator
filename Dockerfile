FROM python:3.7
COPY . /app
WORKDIR /app
RUN mkdir -p /app/resources
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y pandoc xsltproc fop texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra
CMD ["python", "dmptool-service.py"]