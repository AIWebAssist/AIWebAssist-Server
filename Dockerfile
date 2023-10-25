FROM python:3.8 as base

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

CMD python example/api.py

FROM base as dev

RUN pip3 install -r requirements-dev.txt
# pull the extension
RUN VER=$(curl -I https://github.com/AIWebAssist/AIWebAssistExtension/releases/latest/ | awk -F '/' '/^location/ {print  substr($NF, 1, length($NF)-1)}')
RUN wget https://github.com/AIWebAssist/AIWebAssistExtension/releases/download/${VER}/extension.crx 


CMD sh -c "while sleep 1000; do :; done"


