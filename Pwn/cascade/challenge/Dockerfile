FROM ubuntu@sha256:9cbed754112939e914291337b5e554b07ad7c392491dba6daf25eef1332a22e8 as chroot

RUN /usr/sbin/useradd --no-create-home -u 1024 user
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update; apt-get -y install socat

COPY flag.txt /home/user/flag.txt
COPY vuln /home/user/chal
RUN chmod 555 /home/user/chal

FROM gcr.io/kctf-docker/challenge@sha256:d884e54146b71baf91603d5b73e563eaffc5a42d494b1e32341a5f76363060fb

COPY --from=chroot / /chroot

COPY nsjail.cfg /home/user/

CMD kctf_setup && \
    kctf_drop_privs \
    socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"kctf_pow nsjail --config /home/user/nsjail.cfg -- /home/user/chal"
