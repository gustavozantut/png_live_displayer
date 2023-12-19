FROM ubuntu:20.04

RUN apt update

# Install Python and pip
RUN apt-get install -y python3 python3-pip

RUN apt update

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libgstreamer1.0-dev\
									libgstreamer-plugins-base1.0-dev\
									libgstreamer-plugins-bad1.0-dev\
									gstreamer1.0-plugins-base\
									gstreamer1.0-plugins-good\
									gstreamer1.0-plugins-bad\
									gstreamer1.0-plugins-ugly\
									gstreamer1.0-libav\
									gstreamer1.0-doc\
									gstreamer1.0-tools\
									gstreamer1.0-x\
									gstreamer1.0-alsa\
									gstreamer1.0-gl\
									gstreamer1.0-gtk3

RUN apt update

RUN pkg-config --cflags --libs gstreamer-1.0

RUN git clone https://github.com/gustavozantut/png_live_displayer.git/ /app/png_live_displayer/

WORKDIR /app/png_live_displayer/app

ENV DISPLAY=host.docker.internal:0

CMD ["python3", "/app/png_live_displayer/app/display_png.py"]
#run
#docker build -t guhzantut/yolov5_live_gst:latest . ; docker run --ipc=host --gpus all -it -v toll_runs:/runs --rm -e RUN_NAME=20231218053245745784 guhzantut/yolov5_live_gst:latest