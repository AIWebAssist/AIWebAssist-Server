FROM python:3.8 as prod

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 3000
ENV FLASK_APP=main.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]


FROM prod as dev

# install all dev requirements 
RUN pip3 install -r requirements-dev.txt

# pull the extension
#RUN rm extension.crx && wget https://clients2.googleusercontent.com/crx/blobs/AeKPYwwIqwbhw-_kDPnAAu2t5sv92Ssbj3HTsEh4ixHmCJQFowO1yuw3sSkHatdDT-3HUsyfQ1SX9hEnPFG2-gSnQajHhvzouiL4Xv42tmeQCqMnkolpAMZSmuW000Hg1hFgMsxTr2QZUJvYMPSsqA/pacicdjgganecekjpopincedecpdajae.crx -O extension.crx

# need to convet frames intto video
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
CMD sh -c "while sleep 1000; do :; done"



