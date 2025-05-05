FROM python:3.10-buster

# Install required system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /backend

# Copy requirements.txt first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port
EXPOSE 5000

# Command to run the app
CMD ["flask", "run", "--host=0.0.0.0"]
