#include <iostream>
#include "webio.hpp"

#include "utils.cpp"
#include "elements.cpp"

using namespace std;

using namespace webio;

int main() {


  struct MyWebsite {
    int num = 0;
    auto Render() {
    	std::vector<std::string> files = {"main.cpp", "test.cpp", "utils.cpp", "elements.cpp"};

    	std::vector<std::pair<std::string, int> > options = {std::make_pair("Delete", 0), std::make_pair("Copy", 1), std::make_pair("Move", 2)};

      auto frame = VDiv().padding("0 0 0 20px");

      frame << Text("Welcome to filesystem") << VSpace("20px");

      frame << Text("Current:~/Desktop/Hackathon/webio") << VSpace("10px");

      // frame << (Div() << Button("Paste here") << Button("Home"));

      frame << Button("Click me to add more buttons").onclick([&](){num++;});

      for (int i = 0; i < num; i++) {
        frame << Button("Button number " + std::to_string(i) + "added on click");
      }

      frame << Icon("arrow_back");
      for (const auto& file : files) {
      	frame << (HDiv() << Menu(options).width("30px").icon("more_vert") << (Div() << Text(file)));
      }
     
      return frame;
    }
  };

  // cout << FrameServer<MyWebsite>().HandleFirstTimeLoad().ToString() << endl;

  FrameServer<MyWebsite>().Run(5007);
  return 0;
}
