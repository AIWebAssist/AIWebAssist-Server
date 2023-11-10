FROM python:3.8 as base

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

CMD python example/api.py

FROM base as dev

RUN pip3 install -r requirements-dev.txt
# pull the extension
#RUN rm extension.crx && wget https://clients2.googleusercontent.com/crx/blobs/AfBom9Y09skx0bRyXMkFM0ICCHXPgvmZR8HL0mcuoqSYq4yzqV0y9Gxz-0mgjNgfTnN2a_sA_Db8RSdC_hde8D_6VX6HIdcFEKsVLRmGtrivRZTn1tTAAMZSmuUEKcmvR8WmVWYzbKplwA8Seeo9KA/dicmckdpjpagngabbhhlbahoicjabmoe.crx -O extension.crx
#                             
CMD sh -c "while sleep 1000; do :; done"


