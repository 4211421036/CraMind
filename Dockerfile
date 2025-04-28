FROM python:3.10-slim

WORKDIR /app

# Install all language runtimes and compilers
RUN apt-get update && apt-get install -y \
    python3 \
    nodejs \
    npm \
    openjdk-17-jdk \
    g++ \
    golang \
    ruby \
    php \
    swift \
    kotlin \
    rustc \
    cargo \
    dotnet-sdk-6.0 \
    && rm -rf /var/lib/apt/lists/*

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app
COPY action.yml .

ENTRYPOINT ["python", "/app/main.py"]
