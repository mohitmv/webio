#include "utils.hpp"

#include <string>
#include <vector>
#include <unordered_map>

using std::string;
using std::unordered_map;

namespace webio {

Json FrontEndElement::Export() const {
  Json output;
  output.Set(unordered_map{
    {"element_type", Json("BUTTON")},
    {"element_id", Json(12)},
    {"onclick_id", Json()},
    {"icon", Json()},
    {"label_string": "Click Me"}});
  return output;
}

} // namespace webio
