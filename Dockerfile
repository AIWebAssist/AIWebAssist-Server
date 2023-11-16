FROM python:3.8 as base

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

CMD python example/api.py

FROM base as dev

RUN pip3 install -r requirements-dev.txt
# pull the extension
#RUN rm extension.crx && wget https://clients2.googleusercontent.com/crx/blobs/AfBom9Y3EtlbrpN4CZmLpCCi2Qg8VifjP7kd75Vwha-cBNfmk4rUoZuNhB7W-wV-gD1tzU7P6MtLPWISGWCDUoNNkAvS0LBwwWlJkHqwhH5gvUW7m47uAMZSmuW2xFUCg3JZrKw-lAtoKjNokqqjtQ/dicmckdpjpagngabbhhlbahoicjabmoe.crx -O extension.crx
#                             
CMD sh -c "while sleep 1000; do :; done"


