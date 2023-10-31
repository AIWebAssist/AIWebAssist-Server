FROM python:3.8 as base

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

CMD python example/api.py

FROM base as dev

RUN pip3 install -r requirements-dev.txt
# pull the extension
#RUN rm extension.crx && wget https://clients2.googleusercontent.com/crx/blobs/AfBom9aUmoOj8VHSOYi7KutxR-34ep2mY4XOB2Pr1QwyE7YFah6gQql0xhkC3xOHAWvD8LhX96qbnnd5bPw5VdKA2hUvYJcXSh5KMQ3KDDTPCaGdBQxUAMZSmuWaAHsKLIvSJV3YpmC4_xR4fOai6A/dicmckdpjpagngabbhhlbahoicjabmoe.crx -O extension.crx
#                             
CMD sh -c "while sleep 1000; do :; done"


