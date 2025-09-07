FROM perl:5.36

RUN cpanm -n HTTP::Daemon HTTP::Status File::MimeInfo::Simple CGI

WORKDIR /app
COPY server.pl /app/server.pl
COPY files/ /app/files/
COPY flag.txt /
RUN mv /flag.txt /flag-$(md5sum /flag.txt | awk '{print $1}').txt

RUN /usr/sbin/useradd --no-create-home -u 1024 user
USER user

EXPOSE 8080
CMD ["perl", "server.pl"]
