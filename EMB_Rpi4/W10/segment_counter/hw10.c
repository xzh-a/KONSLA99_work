#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>

static struct termios init_setting, new_setting;
char seg_num[10] = {0xc0, 0xf9, 0xa4, 0xb0, 0x99, 0x92, 0x82, 0xd8, 0x80, 0x90};
char seg_dnum[10] = {0x40, 0x79, 0x24, 0x30, 0x19, 0x12, 0x02, 0x58, 0x00, 0x10};

int count = 0;

#define D1 0x01
#define D2 0x02
#define D3 0x04
#define D4 0x08

void init_keyboard() {
    tcgetattr(STDIN_FILENO, &init_setting);
    new_setting = init_setting;
    new_setting.c_lflag &= ~ICANON;
    new_setting.c_lflag &= ~ECHO;
    new_setting.c_cc[VMIN] = 0;
    new_setting.c_cc[VTIME] = 0;
    tcsetattr(0, TCSANOW, &new_setting);
}

void close_keyboard() {
    tcsetattr(0, TCSANOW, &init_setting);
}

char get_key() {
    char ch = -1;
    if (read(STDIN_FILENO, &ch, 1) != 1) ch = -1;
    return ch;
}

void print_menu() {
    printf("\n----------menu----------\n");
    printf("[u] : count up\n");
    printf("[d] : count down\n");
    printf("[p] : program reset\n");
    printf("[q] : program exit\n");
    printf("------------------------\n\n");
}
//up 함수 9999를 넘어가면 0으로 초기화
void up() {
  count++;
  if (count > 9999) {
    count = 0;
  }
}
//down 함수 0이하는 9999로
void down() {
  count--;
  if (count < 0) {
    count = 9999;
  }
}

//display에 10,100,1000의 자리를 배정
void display_number(int dev, int number) {
    unsigned short data[4];
    int thousands = number / 1000;
    int hundreds = (number % 1000) / 100;
    int tens = (number % 100) / 10;
    int ones = number % 10;

    data[0] = (seg_num[thousands] << 4) | D1;
    data[1] = (seg_num[hundreds] << 4) | D2;
    data[2] = (seg_num[tens] << 4) | D3;
    data[3] = (seg_num[ones] << 4) | D4;

    for (int i = 0; i < 4; i++) {
        write(dev, &data[i], 2);
        usleep(100);
    }
}

int main(int argc, char* argv[]) {
    char key;
    int delay_time;
    char buff[2];//buffer의 값을 읽을 때 첫번째 버퍼의 값만을 읽고 두번째 버퍼의 값은 0으로

    int dev1 = open("/dev/my_segment", O_RDWR);//segment
    int dev2 = open("/dev/ud_button", O_RDWR);//버튼 드라이버
    
    if (dev1 == -1) {
        printf("Opening was not possible!\n");
        return -1;
    }

    if (dev2 == -1) {
        printf("Opening was not possible!\n");
        return -1;
    }

    printf("device opening was successful!\n");

    init_keyboard();
    print_menu();
    delay_time = 100;
    //get_key()를 통해 입력받은 문자로 up, down 함수를 호출
    while(1) {
        key = get_key();
        if (key == 'u'||key == 'U') {
            up();
            printf("up(key)\n");
        }
        else if (key == 'd'||key == 'D') {
            down();
            printf("down(key)\n");
        }
        else if (key == 'p'||key == 'P') {
            count = 0;
        }
        else if (key == 'q'||key == 'Q') {
            printf("exit this program.\n");
            break;
        }
    // 키보드가 아닌 버튼을 통해 up,down을 호출하는 함수
        read(dev2, &buff, sizeof(buff));
        buff[1]='\0';
        if (buff[0] =='U') {
            up();
            printf("up(button)\n");
        }
        else if (buff[0] == 'D') {
            down();
            printf("down(button)\n");
        }

        display_number(dev1, count);
        usleep(delay_time);
        memset(buff, 0, sizeof(buff));
    }

    close_keyboard();
    write(dev1, 0x0000, 2);
    close(dev1);
    close(dev2);
    return 0;
}
