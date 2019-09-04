#ifndef _WEBIO_SERVER_HPP_
#define _WEBIO_SERVER_HPP_

#include <unistd.h> 
#include <stdio.h> 
#include <sys/socket.h> 
#include <stdlib.h> 
#include <netinet/in.h> 
#include <string.h> 
#include <functional>
#include <iostream>
#include "utils.hpp"

using std::cout;
using std::endl;

// ToDo(Mohit): this http_server is highly buggy. Don't use it unless you know
// what you are doing.
class HttpServer {
public:
  using string = std::string;
  std::function<string(const string& url)> get_method_handler;
  std::function<string(const string& url, const string& body)> post_method_handler;
  void Run(int port);
};

// int main(int argc, char const *argv[]) {

//   HttpServer server;
//   server.get_method_handler = [&](const string& url) {
//     cout << "Get request arrived...: " << url << endl;
//     return string("This is output");
//   };
//   server.post_method_handler = [&](const string& url,
//                                    const string& post_params) {
//     cout << "Post request arrived...: " << url << endl;
//     cout << "Params = " << post_params << endl;
//     return string("This is output");
//   };

//   int port = 5006;

//   cout << "Running 127.0.0.1:" << port << endl;
//   server.Run(port);

//   return 0;
// }


#endif //  _WEBIO_SERVER_HPP_

