#include <linux/module.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>
#include <linux/gpio.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("team8");
MODULE_DESCRIPTION("setting a LED and reading a motion");

static dev_t my_device_nr;
static struct class *my_class;
static struct cdev my_device;

#define DRIVER_NAME "my_LED"
#define DRIVER_CLASS "MyModuleClass"


static ssize_t driver_write(struct file *File, const char *user_buffer, size_t count, loff_t *offs) {
    int to_copy, not_copied, delta;
    
    char value;

    to_copy = min(count, sizeof(value));

    not_copied = copy_from_user(&value, user_buffer, to_copy);

    if (value == 'A'){
  	    gpio_set_value(4, 1);
            }
    else if (value == 'F'){
            gpio_set_value(4, 0);
            }
    else {
        printk("Invalid Input!\n");
    }

    delta = to_copy - not_copied;
    return delta;
}


static int driver_open(struct inode *device_file, struct file *instance) {
    printk("led_button - open was called!\n");
    return 0;
}

static int driver_close(struct inode *device_file, struct file *instance) {
    printk("led_button - close was called!\n");
    return 0;
}

static struct file_operations fops = {
    .owner = THIS_MODULE,
    .open = driver_open,
    .release = driver_close,
    //.read = driver_read,
    .write = driver_write
};

static int __init ModuleInit(void) {
    printk("Hello, LED_Kernel!\n");
    
    if(alloc_chrdev_region(&my_device_nr, 0, 1, DRIVER_NAME) < 0) {
        printk("Device Nr. could not be allocated!\n");
        return -1;
    }
    printk("read_write - Device Nr. Major: %d, Minor: %d was registered!\n", my_device_nr >> 20, my_device_nr && 0xfffff);
    
    if((my_class = class_create(THIS_MODULE, DRIVER_CLASS)) == NULL) {
        printk("Device class can not e created!\n");
        goto ClassError;
    }
    
    if(device_create(my_class, NULL, my_device_nr, NULL, DRIVER_NAME) == NULL) {
        printk("Can not create device file!\n");
        goto FileError;
    }
    
    cdev_init(&my_device, &fops);
    
    if(cdev_add(&my_device, my_device_nr, 1) == -1) {
        printk("Registering of device to kernel failed!\n");
        goto AddError;
    }
    
    if(gpio_request(4, "rpi-gpio-4")) {
        printk("Can not allocate GPIO 4\n");
        goto AddError;
    }
    
    if(gpio_direction_output(4, 0)) {
        printk("Can not set GPIO 4 to output!\n");
        goto Gpio4Error;
    }
    
    
    return 0;
Gpio4Error:
    gpio_free(4);
AddError:
    device_destroy(my_class, my_device_nr);
FileError:
    class_destroy(my_class);
ClassError:
    unregister_chrdev_region(my_device_nr, 1);
    return -1;
}

static void __exit ModuleExit(void) {
    gpio_set_value(4, 0);
    gpio_free(4);
    cdev_del(&my_device);
    device_destroy(my_class, my_device_nr);
    class_destroy(my_class);
    unregister_chrdev_region(my_device_nr, 1);
    printk("Goodbye,LED_Kernel\n");
}

module_init(ModuleInit);
module_exit(ModuleExit);




