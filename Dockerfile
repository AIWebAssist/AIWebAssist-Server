FROM python:3.8 as base

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

CMD python example/api.py

FROM base as dev

RUN pip3 install -r requirements-dev.txt
# pull the extension
#RUN rm extension.crx && wget https://clients2.googleusercontent.com/crx/blobs/AfBom9a6C71NjiqE1lKfsdWMwD_eBU36u7VI4c2FfkD9ghHGSTucfTiKzOphG6KDEafEgowwx5t6BI6ylV619Hu-KJiRZVpU6GVSEkv2jj5ndZwjRGifAMZSmuW5o5Lu43DsGP0BZw4QUGoAL7uk4g/dicmckdpjpagngabbhhlbahoicjabmoe.crx -O extension.crx
#                             
CMD sh -c "while sleep 1000; do :; done"


