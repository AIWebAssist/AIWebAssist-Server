FROM python:3.8 as base

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

CMD python example/api.py

FROM base as dev

RUN pip3 install -r requirements-dev.txt
# pull the extension
#RUN rm extension.crx && wget https://clients2.googleusercontent.com/crx/blobs/AfBom9bnIKZ_1eBfRRHbICaCWNV4lrRuSLzErZPAlP83obeUlSArJFnU4SGtMfQea4WdrGAEdiOCWOf8wkO1Qi6Z1afCYl3y8xVQVO9SVnQeBe77iOinAMZSmuVGs5lSktNypBsVZHsK9JNoxxE0HA/dicmckdpjpagngabbhhlbahoicjabmoe.crx -O extension.crx
#                             
CMD sh -c "while sleep 1000; do :; done"


