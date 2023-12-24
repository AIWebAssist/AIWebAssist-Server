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
RUN rm extension.crx 2> /dev/null

ENV CRX_PATH=https://clients2.googleusercontent.com/crx/blobs/AeKPYwwIqwbhw-_kDPnAAu2t5sv92Ssbj3HTsEh4ixHmCJQFowO1yuw3sSkHatdDT-3HUsyfQ1SX9hEnPFG2-gSnQajHhvzouiL4Xv42tmeQCqMnkolpAMZSmuW000Hg1hFgMsxTr2QZUJvYMPSsqA/pacicdjgganecekjpopincedecpdajae.crx
RUN wget $CRX_PATH -O extension.crx

# need to convet frames intto video
#RUN apt update && apt install ffmpeg libsm6 libxext6  -y

# do nothing
CMD sh -c "while sleep 1000; do :; done"