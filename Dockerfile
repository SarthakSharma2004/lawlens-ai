# BASE IMAGE

FROM python:3.13-slim

# WORKDIR

WORKDIR /app

# COPY REQUIREMENTS

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# COPY FILES

COPY . . 


# EXPOSE PORT

EXPOSE 8000

# RUN SERVER

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
