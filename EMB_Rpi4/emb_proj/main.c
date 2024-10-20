#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>

#define PIPE "/tmp/my_pipe"
#define BUFFER_SIZE 100

int main() {
    int pipe_fd;
    char buffer[BUFFER_SIZE];
    int isPlaying = 0;  // 음악 재생 상태 추적

    int dev1 = open("/dev/motor_driver", O_RDWR);// step motor
    int dev2 = open("/dev/my_LED", O_RDWR);// led device 
    if (dev1 == -1) {
        printf("Opening was not possible!\n");
        return -1;
    }
    if (dev2 == -1) {
        printf("Opening was not possible!\n");
        return -1;
    }
    printf("device opening was successful!\n");

    pipe_fd = open(PIPE, O_RDONLY);
    if (pipe_fd == -1) {
        perror("open");
        return EXIT_FAILURE;
    }

    while (1) {
        ssize_t bytes_read = read(pipe_fd, &buffer, BUFFER_SIZE);  // 단일 문자 읽기
        if (bytes_read > 0) {
            printf("Received: %c\n", buffer[0]);  // 단일 문자 출력

             if(buffer[0]=='S'){//motor stop and buzz on
               printf("Stop\n");
               write(dev1,&buffer[0],1);
               usleep(100);
            }
            else if(buffer[0]=='R'){
                printf("Right\n");
                write(dev1,&buffer[0],1);
                usleep(100);
            }
            else if(buffer[0]== 'L'){
                printf("Left\n");
                write(dev1,&buffer[0],1);
                usleep(100);
            }
            else if (buffer[0] == 'A' && !isPlaying){
                // 'A' 입력 시, 음악이 정지 상태이면 재생 시작
                system("aplay taeyeon.wav &");  // 음악 재생
                isPlaying = 1;
		write(dev2, &buffer[0], 1);
		printf("led on\n");
            }
            else if (buffer[0] == 'F' && isPlaying){
                // 'F' 입력 시, 음악이 재생 상태이면 정지
                system("pkill aplay");  // 음악 정지
                isPlaying = 0;
		write(dev2, &buffer[0], 1);
		printf("led off\n");
            }
            
	     else {}
        } else {
            perror("read");
            close(pipe_fd);
            return EXIT_FAILURE;
        }
    }
    close(dev2);
    close(dev1);
    close(pipe_fd);
    return EXIT_SUCCESS;
}

