FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install uv
RUN uv sync

EXPOSE 5001

CMD ["uv", "run", "python", "src/ohtu_miniprojekti/app.py"]