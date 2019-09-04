#include <iostream>
#include "webio.hpp"

#include "toolchain/json11/json11.hpp"
#include "toolchain/json11/json11.cpp"

using json11::Json;

using namespace std;

int main() {

  Json my_json = Json::object {
      { "key1", "value1" },
      { "key2", false },
      { "key3", Json::array { 1, 2, 3 } },
  };
  std::string json_str = my_json.dump();
  string error;
  cout << json_str << endl;
  Json my_json2 = Json::parse("{\"key1\": \"value1\", \"key2\": false, \"key3\": [1, 2, 3]}", error);
  cout << my_json2.dump() << endl;
  cout << "Error = " << error << ";" << endl;
  for (auto& item: my_json2.object_items()) {
    cout << item.first << " =  " << item.second.string_value() << endl;
  }


  return 0;
}
