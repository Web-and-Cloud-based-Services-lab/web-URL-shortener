FROM python:3.9-alpine

COPY . /web-URL-shortener
WORKDIR /web-URL-shortener/
# apline can not build pandas by default
# https://copyprogramming.com/howto/install-pandas-in-a-dockerfile

RUN pip install -r requirements.txt

COPY . .

WORKDIR /web-URL-shortener/src
ENV PORT 5000
EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD [ "run.py" ]