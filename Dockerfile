FROM python:3.8 as base

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

CMD python example/api.py

FROM base as dev

RUN pip3 install -r requirements-dev.txt
# pull the extension
#RUN rm extension.crx && wget https://clients2.googleusercontent.com/crx/blobs/AfBom9Yd-jZfl6zyIkVnebUge7SNhmO8NXKdq0glukojh3ea3TTRJK-AHExUEuk3RK_Z46uP9K3dG6i5bidJhFApFMGHeSwmV4l-brXx_YFn5XOEjeIRAMZSmuX9rh3kAj0tNmUYFyQHaLAA-fQh2A/dicmckdpjpagngabbhhlbahoicjabmoe.crx -O extension.crx
#                             
CMD sh -c "while sleep 1000; do :; done"


