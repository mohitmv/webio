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

      frame << Text("Welcome to webio") << VSpace("20 px");

      FrontEndElement htab = HTabs().padding("0px 0px 0px 0px").selected_tab(0);

      htab << Tab("Sample tab");

      frame << htab;

      frame << DropDown("dropdown options").options({"a", "b", "c"});

      frame << VSpace("10 px");

      frame << Text("Want to create more content?");

      frame << VSpace("20 px");

      frame << TextInput("Your name?") << TextArea("Your content goes here");

      return frame;
    }
  };

  // cout << FrameServer<MyWebsite>().HandleFirstTimeLoad().ToString() << endl;

  FrameServer<MyWebsite>().Run(5007);
  return 0;
}
