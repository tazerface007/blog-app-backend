FROM python:slim-bookworm
LABEL authors="deepak"

WORKDIR /app

copy requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]