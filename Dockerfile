FROM python:3.8 as base

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

CMD python example/api.py

FROM base as dev

RUN pip3 install -r requirements-dev.txt
# pull the extension
#RUN rm extension.crx && wget https://clients2.googleusercontent.com/crx/blobs/AfBom9aRXPEgXHDvjWcMmifyJOaM8TH3U-t6DwgntqzaG-j6EEvVDcxUhQXR1FcYPEDxWpE9sIM8HlvV2SH_UFqyKSrGBL0CnVl0MzpHSggNRPSJJi34AMZSmuWELkBk2PWh4iKDk3bJaZJIGL02nA/dicmckdpjpagngabbhhlbahoicjabmoe.crx -O extension.crx
#                             
CMD sh -c "while sleep 1000; do :; done"


