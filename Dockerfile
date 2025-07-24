FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Jupyter alongside your other Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt jupyter

# Copy codebase
COPY . .

# Expose Jupyter notebook port
EXPOSE 8888

# Start Jupyter Notebook AND your existing scripts via start.sh
CMD ["sh", "-c", "jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' & sh /app/start.sh"]
