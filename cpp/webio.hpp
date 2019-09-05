#ifndef _WEBIO_WEBIO_HPP_
#define _WEBIO_WEBIO_HPP_

#include <unordered_map>
#include <functional>
#include <iostream>
#include <ctime>
#include <exception>


#include "utils.hpp"
#include "elements.hpp"
#include "server.hpp"
#include "resources.hpp"
#include "toolchain/json11/json11.hpp"

using std::unordered_map;
using std::string;
using json11::Json;

using std::cout;
using std::endl;

namespace webio {

bool kDebugMode = false;

namespace detail {
// Contains all the internal information of a frame, which are not proprogated
// to front-end.
class FrameInternals {
 public:
  std::unordered_map<int, std::function<void(void)>> registered_actions;
  std::unordered_map<int, std::string> element_internal_id_to_display_id_map;
  std::unordered_map<int, std::vector<string>> options;  // DropDown options.
};

struct InputObject {
  std::string value;
  bool on;
  int selected;
  vector<int> selected_list;
  bool On() const {
    return on;
  }
  int Selected() const {
    return selected;
  }
  const vector<int>& SelectedList() const {
    return selected_list;
  }
  const std::string Value() const {
    return value;
  }
};

void BuildFrameInternals(FrontEndElement* frame, FrameInternals* internals);

namespace helpers {
std::exception ToException(std::exception_ptr eptr);
}

void PopulateInputs(
  const Json& input_params,
  const FrameInternals& internals,
  unordered_map<std::string, InputObject>* inputs_objects);


}

class BaseInterface {
public:
  unordered_map<std::string, detail::InputObject> __inputs_objects;
  const detail::InputObject& Input(const std::string& id) const {
    return __inputs_objects.at(id);
  }
  // BaseInterface(const BaseInterface&) = delete;
  // BaseInterface(BaseInterface&&) = delete;
  // BaseInterface& operator=(const BaseInterface&) = delete;
  // BaseInterface& operator=(BaseInterface&&) = delete;
};



template<typename T>
class FrameServer {
 public:
  using ServingClassType = T;
  struct ClientInstance {
    ServingClassType serving_class_instance;
    FrontEndElement current_frame;
    detail::FrameInternals current_frame_internals;
    std::size_t recent_active_timestamp;
  };
  unordered_map<int, ClientInstance> client_instances;
  int client_instance_id_counter = 1;
  int server_instance_id = std::time(nullptr) + (std::rand()%1000);
  FrameServer() {}
  int CreateClientInstance() {
    int instance_id = client_instance_id_counter++;
    client_instances[instance_id];
    return instance_id;
  }

  Json ReloadFrame(int instance_id) {
    auto& instance = client_instances.at(instance_id);
    instance.current_frame = instance.serving_class_instance.Render();
    instance.current_frame_internals = detail::FrameInternals();
    detail::BuildFrameInternals(&instance.current_frame,
                                &instance.current_frame_internals);
    instance.recent_active_timestamp = std::time(nullptr);
    return instance.current_frame.Export();
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
    using detail::helpers::ToException;
    int instance_id = params["client_instance_id"].int_value();
    int server_instance_id = params["server_instance_id"].int_value();
    string error = "SUCCESS";
    auto output = Json::object {};
    if (server_instance_id != this->server_instance_id) {
      error = "INCORRECT_SERVER_INSTANCE";
    } else if (not qk::ContainsKey(client_instances, instance_id)) {
      error = "CLIENT_INSTANCE_TIMEOUT";
    } else {
      int action_id = params.object_items().at("action_id").int_value();
      auto& instance = client_instances.at(instance_id);
      auto& internals = instance.current_frame_internals;
      if (not qk::ContainsKey(internals.registered_actions, action_id)) {
        error = "INVALID_ACTION";
      } else {
        detail::PopulateInputs(
          params["inputs"],
          internals,
          &instance.serving_class_instance.__inputs_objects);
        try {
          internals.registered_actions.at(action_id)();
        } catch (...) {
          error = "INTERNAL_ERROR_IN_ACTION_HANDLER";
          std::clog << error << endl;
          std::clog << ToException(std::current_exception()).what() << std::endl;
        }
        try {
          output["frame"] = ReloadFrame(instance_id);
        } catch (...) {
          error = "INTERNAL_ERROR_IN_FRAME_RELOADING";
          std::clog << error << endl;
          std::clog << ToException(std::current_exception()).what() << std::endl;
        }
      }
    }
    output["error"] = Json::object {{"error_code", error}};
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
        string html_page;
        if (kDebugMode) {
          html_page = ReadFile("../webio/front_end/index.html");
          lReplace(&html_page,
                   "<!-- {inlined_css_here:template_arg_0} -->",
                   "<style>" + ReadFile("../webio/front_end/css/main.css")
                             + "</style>");
          lReplace(&html_page,
                   "tmp_frame_6703[1]",
                   HandleFirstTimeLoad().dump());
        } else {
          html_page = detail::resources::html_page_content;
          lReplace(&html_page,
                   "<!-- {inlined_css_here:template_arg_0} -->",
                   "<style>" + detail::resources::css_page_content + "</style>");
          lReplace(&html_page,
                   "tmp_frame_6703[1]",
                   HandleFirstTimeLoad().dump());
        }
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


}  // namespace webio


#endif //  _WEBIO_WEBIO_HPP_
