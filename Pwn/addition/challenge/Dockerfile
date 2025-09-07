FROM ubuntu:22.04@sha256:ac58ff7fe25edc58bdf0067ca99df00014dbd032e2246d30a722fa348fd799a5 as chroot

RUN /usr/sbin/useradd --no-create-home -u 1024 user

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
