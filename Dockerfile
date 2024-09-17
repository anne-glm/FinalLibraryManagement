
FROM python:3.12


WORKDIR /app


COPY requirements.txt /app/


RUN pip install --no-cache-dir -r requirements.txt


RUN pip install gunicorn


COPY . /app/


EXPOSE 8000


CMD ["gunicorn", "library_management.wsgi:application", "--bind", "0.0.0.0:8000"]
