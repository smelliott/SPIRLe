#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define INVALID_SOCKET -1
#define SOCKET_ERROR -1
typedef struct hostent HOSTENT;
typedef int SOCKET;

void error(const char *msg) {
    perror(msg);
    exit(1);
}

int main(int argc, char* argv[]) {
    SOCKET sockfd, confd;
    unsigned short portno = 9999;
    socklen_t clilen;
    char buffer[256];
    struct sockaddr_in serv_addr, cli_addr;
    int n;
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if(sockfd == INVALID_SOCKET) {
         error("error opening socket");
    }
    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(portno);
    if(bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) == SOCKET_ERROR) {
        error("bind error");
    }
    listen(sockfd, 5);
    clilen = sizeof(cli_addr);
    while(true) {
        confd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
        if (confd == SOCKET_ERROR) {
            error("error on accept");
        }
        else {
            //printf("accepted connection\n");
        }
        bzero(buffer, 256);
        n = read(confd, buffer, 255);
        if (n < 0) {
            error("error reading from socket");
        }
        //printf("%s\n", buffer);
        printf("flashing led 1\n");
    }
    close(confd);
    close(sockfd);
    return 0;
}