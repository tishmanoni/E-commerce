FROM python:3.8

ENV PYTHONUNBUFFERED=1
ENV DJANGO_ENV=production

WORKDIR /myshop

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8123

CMD ["python", "manage.py", "runserver", "0.0.0.0:8123"]


