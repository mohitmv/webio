#include <iostream>
#include "webio.hpp"
#include "utils.cpp"
#include "elements.cpp"
#include "server.cpp"
#include "toolchain/json11/json11.cpp"
#include "webio.cpp"

int main() {
  using namespace webio;
  class MyWebsite: public webio::BaseInterface {
    int num_additional_bottom_text = 0;
    int count = 0;
   public:
    auto Render() {
      auto frame = Div();
      frame << Div({
        Text("Mohit Saini"),
        TextInput("Your Name ?").Id("name"),
        Button("Click Me").Onclick([&]() {
          num_additional_bottom_text++;
        })
      });
      frame << HDiv({
        DropDown("Your Age ?").Options({"12", "444"}).Id("age"),
        Text("There is something in the middle of this line"),
        Text("Last Part ")
      });
      frame << TextInput("Your Last Name ?");
      frame << Text("Saini Mohit");
      frame << Text(string("Num = ") + std::to_string(num_additional_bottom_text));
      for(int i = 0; i < num_additional_bottom_text; i++) {
        frame << Text("--- In the Updated Middle And Updated Saini Mohit");
      }
      return frame;
    }
  };
  webio::FrameServer<MyWebsite>().Run(5008);
  return 0;
}
