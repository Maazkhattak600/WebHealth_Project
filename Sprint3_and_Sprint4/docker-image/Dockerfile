FROM thoom/pyresttest

COPY ./tests /usr/src/app

WORKDIR /usr/src/app

ENTRYPOINT ["pyresttest"]

CMD ["https://7mml832500.execute-api.us-east-2.amazonaws.com/" , "api_test.yml"]