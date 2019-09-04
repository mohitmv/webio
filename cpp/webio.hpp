#ifndef _WEBIO_WEBIO_HPP_
#define _WEBIO_WEBIO_HPP_

#include <unordered_map>
#include <functional>
#include <iostream>

#include "utils.hpp"
#include "elements.hpp"
#include "server.hpp"
#include "toolchain/json11/json11.hpp"

using std::unordered_map;
using std::string;
using json11::Json;

using std::cout;
using std::endl;

namespace webio {

bool kDebugMode = false;

class Rendering {
 public:
  int element_index_counter = 0;
  std::unordered_map<int, std::function<void(void)>> registered_actions;
  FrontEndElement frame;
  Rendering() {};
  Rendering(FrontEndElement& frame): frame(frame) {
    EvaluateFrame(this->frame);
  }
  int GetUniqueIndex() {
    element_index_counter += 1;
    return element_index_counter;
  }
  FrontEndElement& EvaluateFrame(FrontEndElement& frame) {
    return EvaluateFrameRecursive(frame);
  }
 private:
  FrontEndElement& EvaluateFrameRecursive(FrontEndElement& frame) {
    frame.element_id = GetUniqueIndex();
    if (frame.has_onclick) {
      frame.onclick_id = GetUniqueIndex();
      registered_actions[frame.onclick_id] = frame.onclick_;
    }
    if (frame.has_onchange) {
      frame.onchange_id = GetUniqueIndex();
      registered_actions[frame.onchange_id] = frame.onchange_;
    }
    for (auto& child_frame : frame.children){
      EvaluateFrameRecursive(child_frame);
    }
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
  int server_instance_id = 11255;
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
    Json output =  Json::object {
      {"error", Json(Json::object{{"error_code", "SUCCESS"}})},
      {"frame", ReloadFrame(client_instance_id)},
      {"client_instance_id", client_instance_id},
      {"server_instance_id", server_instance_id}
    };
    return output;
  }

  Json HandleActionEvent(const Json& params) {
    int client_instance_id = params.object_items().at("client_instance_id").int_value();
    auto output = Json(Json::object({
      {"frame", ReloadFrame(client_instance_id)}
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
      if (url == "/") {
        string html_page = ReadFile("../webio/front_end/index.html");
        lReplace(&html_page,
                 "<!-- {inlined_css_here:template_arg_0} -->",
                 "<style>" + ReadFile("../webio/front_end/css/main.css")
                           + "</style>");
        lReplace(&html_page,
                 "tmp_frame_6703[1]",
                 HandleFirstTimeLoad().dump());
        return html_page;
      } else {
        return string("404");
      }
    };
    server.post_method_handler = [&](const string& url,
                                     const string& post_params) {
      if (url == "/v1/start") {
        return HandleFirstTimeLoad().dump();
      } else if (url == "/v1/action") {
        string error;
        Json params = Json::parse(post_params, error);
        assert(error.size() == 0);
        return HandleActionEvent(params).dump();
      } else {
        return string("404");
      }
      
    };
    server.Run(port);
  }

};

class BaseInterface {
public:
};

}  // namespace webio


#endif //  _WEBIO_WEBIO_HPP_
