#include <iostream>
#include "webio.hpp"

#include "toolchain/json11/json11.hpp"
// #include "toolchain/json11/json11.cpp"

using json11::Json;

using namespace std;

int main() {

  Json my_json = Json::object {
      { "key1", "value1" },
      { "key2", false },
      { "key3", Json::array { 1, 2, 3 } },
  };
  std::string json_str = my_json.dump();
  cout << json_str << endl;


  return 0;
}
