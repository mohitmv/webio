#include <string>

namespace webio {

class FrontEndElement {
  enum ElementType {TEXT, BUTTON, TEXT_INPUT, TEXT_AREA, DROP_DOWN, TOGGLE, MENU, ICON, SIMPLE_DIV, HORIZONTAL_DIV, CHECK_BOX, IMAGE, CHECK_BOX_LIST, HORIZONTAL_TABS, VERTICAL_TABS, TAB, VERTICAL_DIV, INLINED_DIV, ICON_BUTTON};
  ElementType element_type;
  std::vector<FrontEndElement> children;
  // need to add these member fields : ["text_string", "disabled", "icon",
  //               "label_string", "onclick_id", "onchange_id", "options",
  //               "color_theme", "allow_multiple", "font_size",
  //               "margin", "value_integer", "value_integer_list", "height",
  //               "width", "element_id", "padding", "selected_tab",
  //               "border_width", "default_rows"]
  FrontEndElement& operator<<(FrontEndElement&& child_element) {
    children.push_back(std::move(child_element));
  }
  string Export() {
    // implement it.
    return "";
  }
};

FrontEndElement Text(const std::string& text_string) {
  return FrontEndElement(FrontEndElement::TEXT).text_string(text_string);
}

FrontEndElement Image(const std::string* src) {
  return FrontEndElement(FrontEndElement::IMAGE).src(src);
}

}  // namespace webio

