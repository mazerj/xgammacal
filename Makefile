INSTALLDIR=/auto/share/pypeextra

dtp94:
	cc -g -c dtp94.c
	cc -g -o dtp94 dtp94.o -lusb

all: dtp94 install

install: dtp94
	sudo cp dtp94 $(INSTALLDIR)
	sudo chown root $(INSTALLDIR)/dtp94
	sudo chmod +s $(INSTALLDIR)/dtp94
	sudo cp xgammacal.py $(INSTALLDIR)
	sudo cp xgammacal.sh $(INSTALLDIR)/xgammacal
	sudo cp showcalib.m $(INSTALLDIR)
	sudo chmod +x $(INSTALLDIR)/xgammacal
	sudo cp xgammacalplot.py $(INSTALLDIR)/xgammacalplot
	sudo chmod +x $(INSTALLDIR)/xgammacalplot

deps:
	sudo apt-get install libusb-dev

clean:	
	rm -f *.o core.* *.pyc \#*~ .*~ dtp94 \#*\#
