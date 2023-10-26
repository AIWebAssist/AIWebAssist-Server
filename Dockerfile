FROM python:3.8 as base

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

CMD python example/api.py

FROM base as dev

RUN pip3 install -r requirements-dev.txt
# pull the extension
#RUN wget https://clients2.googleusercontent.com/crx/blobs/AfBom9YDV_oFMSCLRERd8mck4weQ95hPw1j49wxc-DtTmGTTQCVC0e__Ej5QOheUB5BwH_8PbVqjplkYrOBxLivdhl15XbtXvEO2A6oNL1fDnoRgsEZAAMZSmuXFi_3XXAFLhm_4KVG0XY1AXUqQ-g/dicmckdpjpagngabbhhlbahoicjabmoe.crx -O extension.crx
CMD sh -c "while sleep 1000; do :; done"


