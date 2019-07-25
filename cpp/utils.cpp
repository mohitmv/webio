#include "utils.hpp"

#include <string>
#include <vector>
#include <unordered_map>
#include <ostream>
#include <functional>
#include <assert.h>
#include <fstream>
#include <sstream>

using std::string;

namespace webio {

namespace {

string JsonToString(const Json& json) {
  std::ostringstream oss;
  // ToDo(Mohit): fix this lQuote method.
  auto lQuote = [&](const string& input) {
    return '\"' + input + '\"';
  };
  std::function<void(const Json&)> lJsonToStringHelper;
  lJsonToStringHelper = [&](const Json& json) {
    switch (json.type) {
      case Json::INT_TYPE:
        oss << json.int_value; break;
      case Json::MAP_TYPE: {
        oss << "{";
        bool is_first = true;
        for (auto& item: *json.map_value) {
          if (not is_first) {
            oss << ", ";
          }
          oss << lQuote(item.first) << ":";
          lJsonToStringHelper(item.second);
          is_first = false;
        }
        oss << "}";
        break;
      }
      case Json::NULL_TYPE:
        oss << "null"; break;
      case Json::STRING_TYPE:
        oss << lQuote(json.string_value); break;
      case Json::BOOL_TYPE:
        oss << (json.bool_value ? "true": "false"); break;
      default:
        assert(false);
    }
  };
  lJsonToStringHelper(json);
  return oss.str();
}

}

string Json::ToString() const {
  // return JsonToString(*this);
  return "{"
    "data: {"
      "\"element_type\": \"BUTTON\","
      "\"element_id\": \"6\","
      "\"label_string\": \"Sample Button\","
      "\"theme\": \"default\","
      "\"icon\": null,"
      "\"onclick_id\": undefined"
    "}"
  "}";
}

std::string ReadFile(std::string file_name) {
  std::ifstream fd(file_name);
  std::stringstream buffer;
  buffer << fd.rdbuf();
  fd.close();
  return buffer.str();
};

void WriteFile(std::string file_name, std::string content) {
  std::ofstream fd(file_name);
  fd << content;
  fd.close();
};


} // namespace webio

