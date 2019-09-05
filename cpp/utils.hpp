#ifndef _WEBIO_UTILS_HPP_
#define _WEBIO_UTILS_HPP_

#include <string>
#include <vector>
#include <unordered_map>
#include <map>

namespace webio {

// struct Json {
//   using string = std::string;
//   using MapType = std::map<string, Json>;
//   enum Type {INT_TYPE, STRING_TYPE, NULL_TYPE, BOOL_TYPE, LIST_TYPE, MAP_TYPE};
//   Json(): type(NULL_TYPE) {};
//   Json(Type type): type(type) {};
//   Json(int x): type(INT_TYPE), int_value(x) {}
//   Json(const string& x): type(STRING_TYPE), string_value(x) {}
//   Json(const MapType& x): type(MAP_TYPE), map_value(x) {}
//   Json(const std::vector<Json>& values): type(LIST_TYPE), json_values(values) {}
//   void Set(Type type) {
//     this->type = type;
//   };
//   void Set(int x) {
//     this->type = INT_TYPE;
//     this->int_value = x; 
//   }
//   void Set(const string& x) {
//     this->type = STRING_TYPE;
//     this->string_value = x;
//   }
//   void Set(const MapType& x) {
//     this->type = MAP_TYPE;
//     this->map_value = x;
//   }
//   Type type;
//   int int_value;
//   bool bool_value;
//   std::string string_value;
//   std::vector<int> integer_values;
//   std::vector<string> string_values;
//   std::vector<Json> json_values;
//   std::vector<Json> list_value;
//   MapType map_value;
//   string ToString() const;
// };

std::string ReadFile(std::string file_name);

void WriteFile(std::string file_name, std::string content);

std::vector<std::string> SplitString(const std::string& input, char split_by, int limit=-1);

namespace quick {

template <typename ContainerType, class KeyType>
bool ContainsKey(const ContainerType& container, const KeyType& key) {
  return container.find(key) != container.end();
}

}

namespace qk = quick;


} // namespace webio

#endif //  _WEBIO_UTILS_HPP_
