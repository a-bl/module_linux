FROM ubuntu:16.04
RUN apt-get -y update && \
	apt-get -y install apache2 && \
	echo "Hi there, what is love? <br /> It is just a song...">/var/www/html/index.html
CMD ["/usr/sbin/apache2ctl","-DFOREGROUND"]
EXPOSE 80
