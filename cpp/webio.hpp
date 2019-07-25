#ifndef _WEBIO_WEBIO_HPP_
#define _WEBIO_WEBIO_HPP_

#include <unordered_map>
#include <functional>
#include <iostream>

#include "utils.hpp"
#include "elements.hpp"
#include "server.hpp"

using std::unordered_map;
using std::string;

using std::cout;
using std::endl;

namespace webio {

class Rendering {
 public:
  int element_index_counter = 0;
  std::unordered_map<int, std::function<void(void)>> registered_actions;
  FrontEndElement frame;
  Rendering() {};
  Rendering(FrontEndElement& frame): frame(frame) {
    EvaluateFrame(frame);
  }
  int GetUniqueIndex() {
    element_index_counter += 1;
    return element_index_counter;
  }
  FrontEndElement& EvaluateFrame(FrontEndElement& frame) {
    return frame;
  }
};

template<typename T>
class FrameServer {
 public:
  using ServingClassType = T;
  struct ClientInstance {
    ServingClassType client_instance;
    Rendering current_frame;
    std::size_t recent_active_timestamp;
  };
  unordered_map<int, ClientInstance> client_instances;
  int client_instance_id_counter = 1;
  int server_instance_id = 11;
  FrameServer() {}
  int CreateClientInstance() {
    int instance_id = client_instance_id_counter++;
    client_instances[instance_id];
    return instance_id;
  }

  Json ReloadFrame(int instance_id) {
    auto& instance = client_instances.at(instance_id);
    auto raw_rendered = instance.client_instance.Render();
    instance.current_frame = Rendering(raw_rendered);
    // instance.recent_active_timestamp = utils.GetEpochTimenow();
    return instance.current_frame.frame.Export();
  }

  Json HandleFirstTimeLoad() {
    int client_instance_id = CreateClientInstance();
    cout << client_instance_id << endl;
    auto output =  Json(Json::MapType{
      {"error", Json(Json::MapType{{"error_code", Json(string("SUCCESS"))}})},
      {"data", ReloadFrame(client_instance_id)},
      {"client_instance_id", Json(client_instance_id)},
      {"server_instance_id", Json(server_instance_id)}
    });
    return output;
  }

  Json HandleActionEvent() {
    int client_instance_id = 1;
    auto output = Json(Json::MapType({
      {"data", ReloadFrame(client_instance_id)}
    }));
    return output;
  }

  void BuildHtml(const string& file_name) {
    auto lReplace = [&](string* input, const string& a, const string& b) {
      return input->replace(input->find(a), a.size(), b);
    };
    string html_page = ReadFile("../webio/front_end/index.html");
    lReplace(&html_page,
             "<!-- {inlined_css_here:template_arg_0} -->",
             "<style>" + ReadFile("../webio/front_end/css/main.css")
                       + "</style>");
    lReplace(&html_page,
             "tmp_frame_6703[1]",
             HandleFirstTimeLoad().ToString());
    WriteFile(file_name, html_page);
  }

  void Run(int port) {
    auto lReplace = [&](string* input, const string& a, const string& b) {
      return input->replace(input->find(a), a.size(), b);
    };
    HttpServer server;
    server.get_method_handler = [&](const string& url) {
      string html_page = ReadFile("../webio/front_end/index.html");
      lReplace(&html_page,
               "<!-- {inlined_css_here:template_arg_0} -->",
               "<style>" + ReadFile("../webio/front_end/css/main.css")
                         + "</style>");
      lReplace(&html_page,
               "tmp_frame_6703[1]",
               HandleFirstTimeLoad().ToString());
      return html_page;
    };
    server.post_method_handler = [&](const string& url,
                                     const string& post_params) {
      return HandleActionEvent().ToString();
    };
    server.Run(port);
  }

};

}  // namespace webio


#endif //  _WEBIO_WEBIO_HPP_
