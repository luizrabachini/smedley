FROM python:3

RUN apt-get update -qq && apt-get install -qq iceweasel xvfb

RUN wget -q -O - "https://github.com/mozilla/geckodriver/releases/download/v0.20.0/geckodriver-v0.20.0-linux64.tar.gz" | tar xvz

COPY . /project

WORKDIR /project

RUN pip install -r requirements.txt

ENV FIREFOX_EXECUTABLE_PATH=/geckodriver
ENV settings smedley.config.settings

CMD ["xvfb-run", "-a", "python", "src/main.py", "run"]
