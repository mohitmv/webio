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

// string JsonToString(const Json& json) {
//   std::ostringstream oss;
//   // ToDo(Mohit): fix this lQuote method.
//   auto lQuote = [&](const string& input) {
//     return '\"' + input + '\"';
//   };
//   std::function<void(const Json&)> lJsonToStringHelper;
//   lJsonToStringHelper = [&](const Json& json) {
//     switch (json.type) {
//       case Json::INT_TYPE:
//         oss << json.int_value; break;
//       case Json::MAP_TYPE: {
//         oss << "{";
//         bool is_first = true;
//         for (auto& item: json.map_value) {
//           if (not is_first) {
//             oss << ", ";
//           }
//           oss << lQuote(item.first) << ":";
//           lJsonToStringHelper(item.second);
//           is_first = false;
//         }
//         oss << "}";
//         break;
//       }
//       case Json::NULL_TYPE:
//         oss << "null"; break;
//       case Json::STRING_TYPE:
//         oss << lQuote(json.string_value); break;
//       case Json::BOOL_TYPE:
//         oss << (json.bool_value ? "true": "false"); break;
//       case Json::LIST_TYPE: {
//         bool is_first = true;
//         oss << "[";
//         for (auto& child_json : json.json_values) {
//           if (not is_first) {
//             oss << ", ";
//           }
//           lJsonToStringHelper(child_json);
//           is_first = false;
//         }
//         oss << "]";
//         break;
//       }
//       default:
//         assert(false);
//     }
//   };
//   lJsonToStringHelper(json);
//   return oss.str();
// }

}

// string Json::ToString() const {
//   return JsonToString(*this);
// }

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

vector<string> SplitString(const string& input, char split_by, int limit) {
  vector<string> output;
  int first = 0;
  for (int i = 0; i < input.size(); i++) {
    if (input[i] == split_by) {
      output.push_back(input.substr(first, i-first));
      first = i+1;
      if (limit != -1 && output.size() >= limit) {
        break;
      }
    }
  }
  if (limit == -1 || output.size() < limit) {
    output.push_back(input.substr(first, input.size()-first));
  }
  return output;
}

} // namespace webio

