FROM ubuntu:18.04
RUN apt-get -y update && apt-get -y install python3 python3-pip
RUN pip3 install pyinstaller virtualenv
RUN mkdir /code
WORKDIR /code
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt .
COPY dockerscript.sh .
ENV PYTHONPATH=$PYTHONPATH:/code/venv/lib/python3.6/site-packages/

# rm -rf build/ dist/ && docker run -v $PWD:/code --rm webcaminstaller /bin/sh -c './dockerscript.sh'
