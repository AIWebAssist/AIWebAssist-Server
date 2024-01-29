FROM python:3.8 as prod

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 3000

CMD ["python", "main.py"]

FROM prod as dev
ENV OPENAI_API <PLACE_WITH_KEY>
# install all dev requirements 
RUN pip3 install -r requirements-dev.txt

# pull the extension
RUN chmod +x setup.sh
RUN ./setup.sh

# do nothing
CMD sh -c "while sleep 1000; do :; done"