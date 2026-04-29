FROM python:3.11-slim

WORKDIR /opt/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser
RUN chmod +x cli/list_profiles.py
RUN ln -s /opt/app/cli/list_profiles.py /usr/local/bin/list-profiles

USER appuser

ENV PYTHONUNBUFFERED=1
ENV PROFILE=balanced

ENTRYPOINT ["sh", "scripts/entrypoint.sh"]
