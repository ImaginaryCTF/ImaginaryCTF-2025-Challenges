FROM ubuntu:24.04@sha256:b59d21599a2b151e23eea5f6602f4af4d7d31c4e236d22bf0b62b86d2e386b8f as chroot

RUN /usr/sbin/useradd --no-create-home -u 1024 user
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update; apt-get -y install python3 python3-pwntools
RUN apt-get -y install socat

COPY flag.txt /home/user/flag.txt
COPY run.py /home/user/chal
COPY vuln /home/user/vuln
RUN chmod 555 /home/user/vuln /home/user/chal /home/user/flag.txt

FROM gcr.io/kctf-docker/challenge@sha256:9f15314c26bd681a043557c9f136e7823414e9e662c08dde54d14a6bfd0b619f

COPY --from=chroot / /chroot

COPY nsjail.cfg /home/user/nsjail.cfg

CMD kctf_setup \
    && (kctf_drop_privs socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"kctf_pow nsjail --config /home/user/nsjail.cfg /home/user/chal")
