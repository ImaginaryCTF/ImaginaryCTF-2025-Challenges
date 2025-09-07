all:
	gcc vuln.c -o vuln
	rm ../dist/*
	cp vuln ../dist/
	cp Dockerfile ../dist/
	cp nsjail.cfg ../dist/
	cp libc.so.6 ../healthcheck/
	cp vuln ../healthcheck/
	cd ../dist; zip multiplication.zip *
	cd ../dist; rm -rf vuln libc.so.6 ld-linux-x86-64.so.2
