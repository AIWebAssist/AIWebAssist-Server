FROM python:3.8 as base

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

CMD python example/api.py

FROM base as dev

RUN pip3 install -r requirements-dev.txt
# pull the extension
#RUN rm extension.crx && wget https://clients2.googleusercontent.com/crx/blobs/AfBom9YZFmozp4ge6I1WlU19n8rg-lBFHtQ0Rcwsc5ALCi8Hczz8b57UAofeojG-B9R8iV6FxeH3Rll4Pt9tWjCSlWOI3a1HhjdchNs6YsR319x2I_HjAMZSmuXNT_SJHl0_x41gAzsVHvhdsARzIQ/dicmckdpjpagngabbhhlbahoicjabmoe.crx -O extension.crx

RUN VER=$(curl -I https://github.com/AIWebAssist/AIWebAssistExtension/releases/latest/ | awk -F '/' '/^location/ {print  substr($NF, 1, length($NF)-1)}')
RUN wget https://github.com/AIWebAssist/AIWebAssistExtension/releases/download/${VER}/extension.zip
RUN unzip extension.zip "extension/shared/*" -d shared/ && mv shared/extension/shared/* shared/ && rm -r shared/extension/

CMD sh -c "while sleep 1000; do :; done"



