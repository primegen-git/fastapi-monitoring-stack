FROM python:3.13.5-slim

WORKDIR /app
# now you can assume you are inside the /app directory in container

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

