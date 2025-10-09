FROM python:3.10-slim

# install
RUN pip install flask

# app
WORKDIR /app
COPY src/ /app

# ensure log dir exists
RUN mkdir -p /var/log/app

EXPOSE 8080
CMD ["python", "server.py"]
