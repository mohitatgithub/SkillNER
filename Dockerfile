FROM python:3.9-slim-bookworm

# System dependencies required for spaCy / numpy
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Locale settings
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Set workdir
WORKDIR /app

# Copy source code
COPY . /app

# Create logs directory inside image
RUN mkdir -p /app/logs

# Upgrade pip
RUN pip install --upgrade pip

# Pin numpy first (avoids binary incompatibility)
RUN pip install numpy==1.23.5

# Install remaining dependencies
RUN pip install -r requirements.txt

# Download spaCy model at build time
RUN python -m spacy download en_core_web_lg

# Expose Flask port
EXPOSE 5065

# Run the app
CMD ["python", "app.py"]