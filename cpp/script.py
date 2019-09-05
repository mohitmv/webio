import msl, json

def gen_resources_cpp():
  html_code = json.dumps(msl.read_file("../webio/front_end/index.html"));
  css_code = json.dumps(msl.read_file("../webio/front_end/css/main.css"));

  output = """
#include "resources.hpp"

namespace webio {
namespace detail {
const string resources::html_page_content = """ + html_code + """;

const string resources::css_page_content = """ + css_code + """;
}
}

  """;
  return output;


msl.write_file("resources.cpp", gen_resources_cpp());

