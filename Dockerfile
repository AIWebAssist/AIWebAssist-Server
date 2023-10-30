FROM python:3.8 as base

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

CMD python example/api.py

FROM base as dev

RUN pip3 install -r requirements-dev.txt
# pull the extension
#RUN rm extension.crx && wget https://clients2.googleusercontent.com/crx/blobs/AfBom9b8_p_c1AzV8anz8dDt7lk_abfLZ-3OgAu_7xIOSCNQ8fKZmaNu2FecgYtJoGBeCBv5B4nyF9E9oACzIxFsTix2NCzsC6-w6a7OyTk2N3RhdjgCAMZSmuXklYkFzegOOy4BRHwaU_pXquIq3Q/dicmckdpjpagngabbhhlbahoicjabmoe.crx -O extension.crx
#                             
CMD sh -c "while sleep 1000; do :; done"


