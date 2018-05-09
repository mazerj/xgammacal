/*
** libusb-based interface for talking to the DTP94 calibration
** bug from Optix.
**
** the program does nothing more than open a connection to the
** optix bug and commands & responses back and forth.
**
** Depends on libusb to run and libusb-dev to compile:
**   % sudo apt-get install libusb-dev
** should set it up..
**
*/

#include <stdio.h>
#include <string.h>
#include <usb.h>

/* USB bus identifier information unique to the DTP94 -- you can
** query this using 'lsusb' or something similar
*/

#define VENDOR_ID	0x0765
#define PRODUCT_ID	0xD094
#define BUFSIZE		8*16

static struct usb_device *device_init(int vendor, int product)
{
  struct usb_bus *usb_bus;
  struct usb_device *dev;

  usb_init();
  usb_find_busses();
  usb_find_devices();

  //usb_set_debug(10);

  for (usb_bus = usb_get_busses(); usb_bus != NULL; usb_bus = usb_bus->next) {
    for (dev = usb_bus->devices; dev; dev = dev->next) {
      if ((dev->descriptor.idVendor == vendor) &&
	  (dev->descriptor.idProduct == product))
	return(dev);
    }
  }
  return(NULL);
}

static int get_string(struct usb_dev_handle *handle, int ep,
		      char *buf, int bufsize, int timeout)
{
  int n;

  bzero(buf, bufsize);
  while (usb_interrupt_read(handle, ep, buf, bufsize, timeout) < 0) {
    fprintf(stderr,"timeout!\n");
    return(-1);
  }
  return(n);
}

static int put_string(struct usb_dev_handle *handle, int ep, char *buf,
		      int timeout)
{
  int n;

  n = usb_interrupt_write(handle, ep, (void *)buf, strlen(buf), timeout);
  if (n < 0) {
    perror("usb_interrupt_write");
  }
  return(n);
}


int main(int argc, char **argv)
{
  struct usb_device *dev;
  struct usb_dev_handle *handle;
  struct usb_config_descriptor *config;
  
  int n;
  char buf[BUFSIZE], *p;
  int _endpoint_w, _endpoint_r;
  int timeout = 20000;
    
  if ((dev = device_init(VENDOR_ID, PRODUCT_ID)) == NULL) {
    fprintf(stdout, "DTP94-ERROR\n");
    fprintf(stderr, "%s: Device not found\n", argv[0]);
    exit(1);
  }

  if ((handle = usb_open(dev)) == NULL) {
    fprintf(stdout, "DTP94-ERROR\n");
    fprintf(stderr, "%s: Not able to open the USB device\n", argv[0]);
    exit(1);
  }

  config = dev->config;
  _endpoint_r = config->interface->altsetting->endpoint[0].bEndpointAddress;
  _endpoint_w = config->interface->altsetting->endpoint[1].bEndpointAddress;

  /*
   * This version seems to work with FC2 and Ubuntu7.10
   * Note that to compile under libusb-dev must be installed. You can
   * use the following to install it:
   *   sudo apt-get install libusb-dev
   */
  usb_claim_interface(handle, config->interface->altsetting->bInterfaceNumber);
  usb_set_altinterface(handle, config->interface->altsetting->bAlternateSetting);
  usb_clear_halt(handle, _endpoint_w);
  usb_clear_halt(handle, _endpoint_r);
  usb_resetep(handle, _endpoint_w);
  usb_resetep(handle, _endpoint_r);

  if (argc > 1) {
    p = (char *)malloc(strlen(argv[1]) + 10);
    strcat(strcpy(p, argv[1]), "\r");
  } else {
    p = (char *)malloc(10);
    strcpy(p, "\r");
  }
  if (argc > 2) {
    if (sscanf(argv[2], "%d", &timeout) != 1) {
      fprintf(stderr, "illegal timeout value\n");
      exit(1);
    }
  }

  if (put_string(handle, _endpoint_w, p, timeout) < 0) {
    exit(1);
  }
  if ((n = get_string(handle, _endpoint_r, buf, sizeof(buf), timeout)) < 0) {
    exit(1);
  }
  for (n = 1; n < sizeof(buf); n++) {
    if (buf[n-1] == '>') {
      buf[n] = 0;
      break;
    }
  }
  printf("%s\n", buf);

  usb_release_interface(handle,
			config->interface->altsetting->bInterfaceNumber);
  usb_close(handle);
}

