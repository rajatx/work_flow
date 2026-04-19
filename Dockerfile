# Dockerfile
# Stage 1: Build Tailwind CSS\

FROM node:20-slim AS tailwind-builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Tailwind v4.2 CLI command to build CSS

RUN npm run build:css

# Stage 2: Run the application

FROM python:3.11-slim
WORKDIR /app

# required system libraries

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copy the built Tailwind CSS from the first stage

COPY --from=tailwind-builder /app/static/css/dist/output.css ./app/static/css/dist/output.css

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]