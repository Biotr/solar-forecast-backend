FROM python:3.12.3-alpine

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
