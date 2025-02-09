FROM python:3.13

COPY src/ /usr/src/

WORKDIR /usr/src/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["chainlit", "run", "app.py","--host", "0.0.0.0"]