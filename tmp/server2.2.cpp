#include <unistd.h> 
#include <stdio.h> 
#include <sys/socket.h> 
#include <stdlib.h> 
#include <netinet/in.h> 
#include <string.h> 
#include <functional>


#include <iostream>

using namespace std;

class HttpServer {
public:
  using string = std::string;
  std::function<string(const string&)> get_method_handler;
  std::function<string(const string&, const string&)> post_method_handler;
  void Run(int port) {
    int server_fd, new_socket, valread;
    struct sockaddr_in address;
    int opt = 1; 
    int addrlen = sizeof(address); 
    char buffer[1024] = {0};
    // Creating socket file descriptor 
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
      perror("socket failed");
      exit(EXIT_FAILURE);
    }
    // Forcefully attaching socket to the port 8080 

    // if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, 
    //                                               &opt, sizeof(opt))) {
    //     perror("setsockopt");
    //     exit(EXIT_FAILURE);
    // }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons( port );
    if (::bind(server_fd, (struct sockaddr *)&address,  
                                 sizeof(address))<0) 
    { 
        perror("bind failed"); 
        exit(EXIT_FAILURE); 
    }
    if (listen(server_fd, 3) < 0) {
        perror("listen"); 
        exit(EXIT_FAILURE); 
    } 
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
      string input_string = buffer;
      cout << "Input = " << buffer << endl;
      printf("%s\n",buffer );
      string response_string = "";
      if (input_string.substr(0, 3) == "GET") {
        response_string = get_method_handler("");
      } else if (input_string.substr(0, 4) == "POST") {
        response_string = post_method_handler("", input_string);
      } else {
        //  kuchh to fatt gya...
        response_string = "Some Error! Shit happened!";
      }
      response_string = string("") + "HTTP/1.1 200 OK\n"
                         "Content-Length: " + std::to_string(response_string.size())+ "\n"
                         "Connection: Closed\n"
                         "Content-Type: text/html; charset=iso-8859-1\r\n\r\n" + response_string;

      cout << "sending response of size = " << response_string.size() <<  endl;
      send(new_socket , response_string.c_str() , response_string.size() , 0);
      close(new_socket);
    }
  }
};

int main(int argc, char const *argv[]) {

  HttpServer server;
  server.get_method_handler = [&](const string& url) {
    cout << "Get request arrived...: " << url << endl;
    return string("This is output");
  };
  server.post_method_handler = [&](const string& url,
                                   const string& post_params) {
    cout << "Post request arrived...: " << url << endl;
    cout << "Params = " << post_params << endl;
    return string("This is output");
  };

  int port = 5006;

  cout << "Running 127.0.0.1:" << port << endl;
  server.Run(port);

  return 0;
}


