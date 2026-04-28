FROM python:3.11-slim

WORKDIR /opt/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN useradd -m appuser
USER appuser

ENTRYPOINT ["sh", "scripts/entrypoint.sh"]
