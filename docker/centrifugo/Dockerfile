FROM centrifugo/centrifugo

WORKDIR /centrefugo

ENV CONFIG='./config.json'

ADD ./scripts/init.centrifugo.sh .

RUN chmod +x init.centrifugo.sh