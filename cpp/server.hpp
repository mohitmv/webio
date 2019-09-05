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


// ToDo(Mohit): this http_server is highly buggy. Don't use it unless you know
// what you are doing.
class HttpServer {
public:
  using string = std::string;
  std::function<string(const string& url)> get_method_handler;
  std::function<string(const string& url, const string& body)> post_method_handler;
  void Run(int port);
};

#endif //  _WEBIO_SERVER_HPP_

