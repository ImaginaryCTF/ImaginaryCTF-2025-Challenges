FROM ubuntu:24.04 as chroot

RUN /usr/sbin/useradd --no-create-home -u 1024 user

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update; apt-get -y install socat

COPY flag.txt /home/user/flag.txt
COPY vuln /home/user/chal
RUN chmod 555 /home/user/chal /home/user/flag.txt

USER user
WORKDIR /home/user
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:/home/user/chal"]
