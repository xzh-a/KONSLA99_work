obj-m += button_seg_driver.o
KDIR = ~/working/kernel
RESULT = hw10
SRC = $(RESULT).c
CCC= aarch64-linux-gnu-gcc

all:
	make -C $(KDIR) M=$(PWD) modules
	$(CCC) -o $(RESULT) $(SRC)

clean:
	make -C $(KDIR) M=$(PWD) clean
	rm -f $(RESULT)                              
