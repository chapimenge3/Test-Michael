FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /testproject
COPY requirements.txt /testproject
RUN pip install -r requirements.txt
COPY . /testproject
