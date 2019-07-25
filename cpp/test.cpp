#include "elements.cpp"
#include "utils.cpp"

#include <iostream>


namespace webio {

class MyWebsite {
public:
	FrontEndElement Render() {
		FrontEndElement frame = Div();

		frame << Text("Welcome to webio") << VSpace("20 px");

		FrontEndElement htab = HTabs().padding("0px 0px 0px 0px").selected_tab(0);

		htab << Tab("Sample tab");

		frame << htab;

		frame << VSpace("10 px");

		frame << Text("Want to create more content?");

		frame << VSpace("20 px");

		frame << TextInput("Your name?") << TextArea("Your content goes here");

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