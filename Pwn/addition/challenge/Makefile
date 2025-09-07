all:
	gcc vuln.c -o vuln -Wl,-z,relro,-z,lazy
	cp vuln vuln_patched
	patchelf --set-interpreter ./ld-linux-x86-64.so.2 --replace-needed libc.so.6 ./libc.so.6  ./vuln_patched
	rm ../dist/*
	cp vuln ../dist/
	cp libc.so.6 ../dist/
	cp ld-linux-x86-64.so.2 ../dist/
	cp ../dist/* ../healthcheck/
	cd ../dist; zip addition.zip *
	cd ../dist; rm -rf vuln libc.so.6 ld-linux-x86-64.so.2
