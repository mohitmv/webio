#include <iostream>
#include "webio.hpp"

#include "utils.cpp"
#include "elements.cpp"

using namespace std;

using namespace webio;

int main() {


  struct MyWebsite {
    auto Render() {
      auto frame = VDiv();
      frame << Button("Click Me Button");
      frame << Button("One more click me button");
      return Button("New Button");
    }
  };

  // cout << FrameServer<MyWebsite>().HandleFirstTimeLoad().ToString() << endl;

  FrameServer<MyWebsite>().Run(5007);
  return 0;
}
