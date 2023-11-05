FROM python:3.8 as base

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

CMD python example/api.py

FROM base as dev

RUN pip3 install -r requirements-dev.txt
# pull the extension
#RUN rm extension.crx && wget https://clients2.googleusercontent.com/crx/blobs/AfBom9YCKxkFqzR6sv8X7cDlgO5V4XOkxiVBrY2sLmMAQpdLuFIRMIPUD9QlCRGf3jLSnn9vTC-jnX6jKY_XQ7hbO8ZipDS2Js1wOQ_mQAltVfTk2GaGAMZSmuWo8NlbnyEvWtAi79bKdC8RrnI1yg/dicmckdpjpagngabbhhlbahoicjabmoe.crx -O extension.crx
#                             
CMD sh -c "while sleep 1000; do :; done"


