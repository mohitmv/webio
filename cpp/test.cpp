#include "elements.cpp"
#include "utils.cpp"

#include <iostream>

namespace webio {

class MyWebsite {
public:
	FrontEndElement Render() {
		FrontEndElement frame = Div();
		frame << Button("Test Button");
		frame << VSpace("20px");
		frame << Text("Text string");
		return frame;
	}
};

} // webio

int main() {
	webio::MyWebsite my_website;
	webio::FrontEndElement frame = my_website.Render();
	// webio::Json json = frame.Export();
	std::cout << frame.Export().ToString() << std::endl;
	return 0;
}
