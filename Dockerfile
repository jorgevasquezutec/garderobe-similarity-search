FROM python:3.9

RUN apt-get update && apt-get install -y build-essential cmake libopenblas-dev liblapack-dev libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103

WORKDIR /app

COPY /requirements/base.txt ./

RUN pip install -U pip wheel cmake
RUN pip install --no-cache-dir -r base.txt

COPY . .

EXPOSE 5000

CMD ["python", "."]