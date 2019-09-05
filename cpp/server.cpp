#include "server.hpp"
#include "utils.hpp"

namespace {
using webio::SplitString;
using std::cout;
using std::endl;

struct HttpHeader {
  string request_type;
  string url;
  unordered_map<string, string> params;
  int content_length = 0;
  void Parse(const string& input) {
    auto lines = SplitString(input, '\n');
    auto line0 = SplitString(lines[0], ' ', 2);
    request_type = line0[0];
    url = line0[1];
    for (int i = 1; i < lines.size(); i++) {
      auto kv = SplitString(lines[i], ':');
      if (kv.size() < 2) {
        break;
      }
      params[kv[0]] = kv[1];
    }
    if (params.find("Content-Length") != params.end()) {
      content_length = std::stoi(params.at("Content-Length"));
    }
  }
  string DebugString() const {
    std::ostringstream oss;
    oss << "request_type = " << request_type << endl;
    oss << "url = " << url << endl;
    oss << "Content-Length = " << content_length << endl;
    oss << "Total " << params.size() << " params" << endl;
    return oss.str();
  }
};


}

void HttpServer::Run(int port) {
  int server_fd, new_socket, valread;
  struct sockaddr_in address;
  int opt = 1;
  int addrlen = sizeof(address);
  // Creating socket file descriptor
  if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
    perror("socket failed");
    exit(EXIT_FAILURE);
  }
  // Forcefully attaching socket to the port
  if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, 
                                                &opt, sizeof(opt))) {
      perror("setsockopt");
      exit(EXIT_FAILURE);
  }
  address.sin_family = AF_INET;
  address.sin_addr.s_addr = INADDR_ANY;
  address.sin_port = htons( port );
  ::bind(server_fd, (struct sockaddr *)&address, sizeof(address));
  if (0) {
      perror("bind failed"); 
      exit(EXIT_FAILURE); 
  }
  if (listen(server_fd, 3) < 0) {
      perror("listen"); 
      exit(EXIT_FAILURE); 
  }
  int count = 0;
  cout << "Running http://127.0.0.1:" << port << endl;
  while (true) {
    if ((new_socket = accept(server_fd, (struct sockaddr *)&address,  
                       (socklen_t*)&addrlen))<0) 
    {
      cout << "Accept error" << endl;
        perror("accept"); 
        exit(EXIT_FAILURE); 
    }
    count++;
    char buffer[1024] = {0};
    char c;
    bool got_new_line = false;
    std::ostringstream oss;
    bool header_reading_done = false;
    while(read(new_socket, &c, 1)) {
      if (c == '\n') {
        if (got_new_line) {
          header_reading_done = true;
          break;
        }
        got_new_line = true;
      } else if (c == '\r') {
      } else {
        got_new_line = false;
      }
      oss << c;
    }
    if (header_reading_done) {
      HttpHeader header;
      header.Parse(oss.str());
      cout << "Request[" << count << "]: " << header.request_type << " " << header.url << endl;
      // cout << header.DebugString();
      string body;
      if (header.content_length > 0) {
        char tmp_string[header.content_length+1];
        tmp_string[header.content_length] = 0;
        assert(read(new_socket, tmp_string, header.content_length) >= 0);
        body = tmp_string;
      }
      // cout << "body size = " << body.size() << endl << endl;
      string response_string = "";
      if (header.request_type == "GET") {
        response_string = get_method_handler(header.url);
      } else if (header.request_type == "POST") {
        response_string = post_method_handler(header.url, body);
      } else {
        response_string = "[Internal]: HttpServer error";
      }
      response_string = string("") + "HTTP/1.1 200 OK\n"
                         "Content-Length: " + std::to_string(response_string.size())+ "\n"
                         "Connection: Closed\n"
                         "Content-Type: text/html; charset=iso-8859-1\r\n\r\n" + response_string;
      send(new_socket , response_string.c_str() , response_string.size() , 0);
    } else {
      cout << "Header was empty. Didn't nothing. Ignoring the request" << endl;
    }
    close(new_socket);
  }
}





