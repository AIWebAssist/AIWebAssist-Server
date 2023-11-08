FROM python:3.8 as base

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

CMD python example/api.py

FROM base as dev

RUN pip3 install -r requirements-dev.txt
# pull the extension
#RUN rm extension.crx && wget https://clients2.googleusercontent.com/crx/blobs/AfBom9a5UM6m5Sg3lkK6tzSL0gTC9NNqBwlNNqhT6z1igs4rjPpsUPmRs-dd2y2z0lE4m67sfkrr-OryoZuamk4mqpcWlpAppHAkMwuXxUtMD95IW_TTAMZSmuWkYPeXzUUn9eiR4DjoEdDI8ZuAlQ/dicmckdpjpagngabbhhlbahoicjabmoe.crx -O extension.crx
#                             
CMD sh -c "while sleep 1000; do :; done"


