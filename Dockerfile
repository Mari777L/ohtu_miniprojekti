FROM python:3.10

WORKDIR /app

#Riippuvuudet siirretty txt tiedostoon
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ohtu_miniprojekti/app.py .
COPY src/ohtu_miniprojekti/templates ./templates
COPY src/ohtu_miniprojekti/static ./static

#EXPOSE 5001

CMD ["python", "app.py", "src/ohtu_miniprojekti/app.py"]