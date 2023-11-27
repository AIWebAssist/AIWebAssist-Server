FROM python:3.8 as base

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

CMD python example/api.py

FROM base as dev

RUN pip3 install -r requirements-dev.txt
# pull the extension
#RUN rm extension.crx && wget https://clients2.googleusercontent.com/crx/blobs/AfBom9bAiPAYTqJLf2fRtNYMq0RsRC32HDLuVVXUDAU0tLB0NS5BnvsxP-pQUOIUDHWszDFFquJqZg9FkYrFN30jJ8gsG0sjDIhqVOhUx5tUdTPfznuhAMZSmuWaQUnyrYLTBD1PyoAlfBOZsM1nTA/dicmckdpjpagngabbhhlbahoicjabmoe.crx -O extension.crx

RUN VER=$(curl -I https://github.com/AIWebAssist/AIWebAssistExtension/releases/latest/ | awk -F '/' '/^location/ {print  substr($NF, 1, length($NF)-1)}')
RUN wget https://github.com/AIWebAssist/AIWebAssistExtension/releases/download/${VER}/extension.zip
RUN unzip extension.zip "extension/shared/*" -d shared/ && mv shared/extension/shared/* shared/ && rm -r shared/extension/

CMD sh -c "while sleep 1000; do :; done"



