
default:
	rm -f *.tar
	COPYFILE_DISABLE=true tar -cvC root -f root.tar .
	COPYFILE_DISABLE=true tar -cvC worker -f worker.tar .

unpack:
	rm -rf root; mkdir root ; cd root ; tar xvpof ../root.tar
	rm -rf worker; mkdir worker ; cd worker ; tar xvpof ../worker.tar
