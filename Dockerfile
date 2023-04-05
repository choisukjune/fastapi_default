
FROM ubuntu:20.04

RUN apt update -y
RUN apt install python3.8 -y
RUN apt install vim -y
RUN apt install net-tools -y
RUN apt install iputils-ping -y
RUN apt install python3-pip -y
RUN apt-get install git -y
RUN apt update -y

RUN apt update -y 
RUN apt install language-pack-ko -y
RUN apt install fonts-nanum -y
RUN apt install fonts-nanum-coding -y
RUN apt install fonts-noto-cjk -y
ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

WORKDIR /root
RUN echo 'alias python=python3' >> .bashrc
RUN echo 'alias pip=pip3' >> .bashrc


WORKDIR /
RUN mkdir workspace
RUN git clone https://github.com/choisukjune/fastapi_default.git /workspace/fastapi_default

WORKDIR /workspace/fastapi_default
RUN pip install -r requirements.txt
CMD [ "python", "main.py" ]
