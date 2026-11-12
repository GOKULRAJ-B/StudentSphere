FROM python:3.12-slim

RUN pip install --no-cache-dir ansible docker

RUN ansible-galaxy collection install community.docker

COPY --from=docker:cli /usr/local/bin/docker /usr/local/bin/docker

COPY --from=docker:cli /usr/local/libexec/docker/cli-plugins/docker-compose /usr/local/lib/docker/cli-plugins/docker-compose

WORKDIR /ansible

CMD ["ansible", "--version"]