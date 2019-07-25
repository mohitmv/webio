// Server side C/C++ program to demonstrate Socket programming 
#include <unistd.h> 
#include <stdio.h> 
#include <sys/socket.h> 
#include <stdlib.h> 
#include <netinet/in.h> 
#include <string.h> 
#define PORT 8080 


#include <iostream>

using namespace std;

int main(int argc, char const *argv[]) { 
    int server_fd, new_socket, valread; 
    struct sockaddr_in address; 
    int opt = 1; 
    int addrlen = sizeof(address); 
    char buffer[1024] = {0}; 
    char *hello = "Hello from server"; 
       
    // Creating socket file descriptor 
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) { 
        perror("socket failed"); 
        exit(EXIT_FAILURE); 
    } 
       
    // Forcefully attaching socket to the port 8080 
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, 
                                                  &opt, sizeof(opt))) 
    { 
        perror("setsockopt"); 
        exit(EXIT_FAILURE); 
    } 
    address.sin_family = AF_INET; 
    address.sin_addr.s_addr = INADDR_ANY; 
    address.sin_port = htons( PORT ); 
       
    cout << "binding" << endl;
    // Forcefully attaching socket to the port 8080 
    if (bind(server_fd, (struct sockaddr *)&address,  
                                 sizeof(address))<0) 
    { 
        perror("bind failed"); 
        exit(EXIT_FAILURE); 
    } 
    cout << "listening" << endl;
    if (listen(server_fd, 3) < 0) 
    { 
        perror("listen"); 
        exit(EXIT_FAILURE); 
    } 
    cout << "Accepting" << endl;
    int count = 1;
    while (true) {
        cout << "New connection------------------------------- " << count << endl;
        count++;
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address,  
                           (socklen_t*)&addrlen))<0) 
        {
            perror("accept"); 
            exit(EXIT_FAILURE); 
        }
        cout << "REading" << endl;
        valread = read( new_socket , buffer, 1024);
        cout << "Input = " << buffer << endl;
        printf("%s\n",buffer ); 
        string response = "HTTP/1.1 404 Not Found\r\n"
                           "Date: Sun, 18 Oct 2012 10:36:20 GMT\n"
                           "Server: Apache/2.2.14 (Win32)\n"
                           "Content-Length: 4\n"
                           "Connection: Closed\n"
                           "Content-Type: text/html; charset=iso-8859-1\r\n\r\nmohit";

        // string response = "HTTP/1.1 200 Ok"
        //                    "\r\n\r\nmohit\r\n";

        cout << "sending response of size = " << response.size() <<  endl;

        send(new_socket , response.c_str() , response.size() , 0);
        close(new_socket);
        printf("Hello message sent\n"); 
    }
    return 0; 
} 