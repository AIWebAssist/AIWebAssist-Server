FROM python:3.8 as base

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

CMD python example/api.py

FROM base as dev

RUN pip3 install -r requirements-dev.txt
# pull the extension
#RUN rm extension.crx && wget https://clients2.googleusercontent.com/crx/blobs/AfBom9YNsXbEvr7fKZrwnAqNAwfHR3TdfbmK8k5cEVPpHYcUgYjjYyeBpDZyr9zZTkl7wA_hDYMGCQK8mCACRok8hTh2wYUR57BY0NT-NTD1SkjbdC_dAMZSmuV6EIX-CJbY1RxatNkL6MQdvUrzyg/dicmckdpjpagngabbhhlbahoicjabmoe.crx -O extension.crx
#                             
CMD sh -c "while sleep 1000; do :; done"


