FROM python:3.12.9-bookworm

EXPOSE 8501

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y git
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./interest_rate_app.py /app/interest_rate_app.py
COPY ./.streamlit /app/.streamlit

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app/interest_rate_app.py", "--server.port=8501", "--server.address=0.0.0.0"]