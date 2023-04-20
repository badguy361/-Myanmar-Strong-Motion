FROM python:3.8-slim-buster
WORKDIR /app
COPY . .
RUN tar -xzvf sac-101.5c-linux_x86_64.tar.gz
RUN pip3 install -r requirements.txt
RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y x11-apps
RUN apt-get install -y x11-xserver-utils
RUN apt-get install -y net-tools
RUN apt install -y libsm6 libice6 libxpm4 libx11-6 libncurses5

RUN sed -i 's#SACHOME=/usr/local/sac#SACHOME=/app/sac#' /app/sac/bin/sacinit.sh
RUN sed -i 's#PATH=${PATH}:${SACHOME}/bin#PATH=${SACHOME}/bin:${PATH}#' /app/sac/bin/sacinit.sh
RUN echo "source /app/sac/bin/sacinit.sh" >> ~/.bashrc
# Docker RUN指令預設是用/bin/sh -c執行，但shell沒有source，所以這邊要改用bash
SHELL ["/bin/bash", "-c"]
RUN source ~/.bashrc