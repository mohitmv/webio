#include <iostream>
#include "webio.hpp"

#include "utils.cpp"

using namespace std;

using namespace webio;

int main() {


  class MyWebsite {
    auto Render() {
      auto frame = VDiv();
      frame << Button("Click Me Button");
      frame << Button("One more click me button");
      return Button("New Button");
    }
  };

  FrameServer<MyWebsite>.BuildHtml("index.html");

  return 0;
}
