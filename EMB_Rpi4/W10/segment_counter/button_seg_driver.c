//made by minigi-chae 2023 11 11
#include <linux/module.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>
#include <linux/gpio.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Johannes $ GNU/Linux");
MODULE_DESCRIPTION("A simple gpio driver for segment count & reading a button");

static dev_t my_device_nr;
static struct class *my_class;
static struct cdev my_device;

#define DRIVER_NAME "ud_button"
#define DRIVER_CLASS "MyModuleClass"

static int count = 0;  // Global variable to store count value
char but_u, but_d, last_Ustate = 0, last_Dstate = 0;

static ssize_t driver_read(struct file *file, char *user_buffer, size_t count, loff_t *offs) {
    int to_copy_u,to_copy_d, not_copied, delta;


    to_copy_u = min(count, sizeof(but_u));
    to_copy_d = min(count, sizeof(but_d));

    but_u = gpio_get_value(5) ? 'U' : '0';  //버튼 입력시 U 미입력시 0
    but_d = gpio_get_value(6) ? 'D' : '0';  //버튼 입력시 D 미입력시 0
    if (but_u!='0' && but_u != last_Ustate) {
        not_copied = copy_to_user(user_buffer, &but_u, to_copy_u);
    }
    last_Ustate = but_u;
    if (but_d !='0' && but_d != last_Dstate) {
        not_copied = copy_to_user(user_buffer, &but_d, to_copy_d);
    }
    last_Dstate = but_d;

    delta = to_copy_u - not_copied;

    return delta;
}

/*
static ssize_t driver_write(struct file *File, const char *user_buffer, size_t count, loff_t *offs) {
    int to_copy, not_copied, delta;
    char value;

    to_copy = min(count, sizeof(value));

    not_copied = copy_from_user(&value, user_buffer, to_copy);

    switch (value) {
    case 'u':
        count++;
        break;
    case 'd':
        count--;
        break;
    default:
        printk("Invalid Input!\n");
        break;
    }

    delta = to_copy - not_copied;
    return delta;
}
*/
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
    .read = driver_read,
    //.write = driver_write
};

static int __init ModuleInit(void) {
    printk("Hello, Kernel!\n");

    if (alloc_chrdev_region(&my_device_nr, 0, 1, DRIVER_NAME) < 0) {
        printk("Device Nr. could not be allocated!\n");
        return -1;
    }
    printk("read_write - Device Nr. Major: %d, Minor: %d was registered!\n", my_device_nr >> 20, my_device_nr && 0xfffff);

    if ((my_class = class_create(THIS_MODULE, DRIVER_CLASS)) == NULL) {
        printk("Device class can not e created!\n");
        goto ClassError;
    }

    if (device_create(my_class, NULL, my_device_nr, NULL, DRIVER_NAME) == NULL) {
        printk("Can not create device file!\n");
        goto FileError;
    }

    cdev_init(&my_device, &fops);

    if (cdev_add(&my_device, my_device_nr, 1) == -1) {
        printk("Registering of device to kernel failed!\n");
        goto AddError;
    }

    return 0;
AddError:
    device_destroy(my_class, my_device_nr);
FileError:
    class_destroy(my_class);
ClassError:
    unregister_chrdev_region(my_device_nr, 1);
    return -1;
}

static void __exit ModuleExit(void) {
    cdev_del(&my_device);
    device_destroy(my_class, my_device_nr);
    class_destroy(my_class);
    unregister_chrdev_region(my_device_nr, 1);
    printk("Goodbye, Kernel\n");
}

module_init(ModuleInit);
module_exit(ModuleExit);
