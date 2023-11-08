FROM python:3.8 as base

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

CMD python example/api.py

FROM base as dev

RUN pip3 install -r requirements-dev.txt
# pull the extension
#RUN rm extension.crx && wget https://clients2.googleusercontent.com/crx/blobs/AfBom9YIE7FpbhOiHrKNbcZ5Weyx8N_9c4wERyPEctJELdxBETJjfxqPAC5TWbDMcpLfB2X9qvT3Niogl6kECLtx2b84JUxy7X5g9hL295zEyCz-Gj4-AMZSmuVdgqvXU1Xj1-m9WtLWspR94RkvHg/dicmckdpjpagngabbhhlbahoicjabmoe.crx -O extension.crx
#                             
CMD sh -c "while sleep 1000; do :; done"


