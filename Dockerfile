FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Declare build arguments BEFORE using them in ENV
ARG DEPLOY_DATE=N/A
ARG DEPLOY_TIME=N/A
ARG GIT_SHA=N/A
ARG BUILD_NUMBER=N/A
ARG HOST=0.0.0.0
ARG PORT=5000

# Now set environment variables from build args
ENV DEPLOY_DATE=${DEPLOY_DATE}
ENV DEPLOY_TIME=${DEPLOY_TIME}
ENV GIT_SHA=${GIT_SHA}
ENV BUILD_NUMBER=${BUILD_NUMBER}
ENV HOST=${HOST}
ENV PORT=${PORT}

COPY . .

# Expose port Flask runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]