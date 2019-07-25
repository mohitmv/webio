#ifndef _WEBIO_ELEMENTS_HPP_
#define _WEBIO_ELEMENTS_HPP_

#include <string>
#include <vector>

#include "utils.hpp"

namespace webio {

class FrontEndElement {
 public:
  using string = std::string;
  enum ElementType {TEXT, BUTTON, TEXT_INPUT, TEXT_AREA, DROP_DOWN, TOGGLE, MENU, ICON, SIMPLE_DIV, HORIZONTAL_DIV, CHECK_BOX, IMAGE, CHECK_BOX_LIST, HORIZONTAL_TABS, VERTICAL_TABS, TAB, VERTICAL_DIV, INLINED_DIV, ICON_BUTTON};
  ElementType element_type;
  std::vector<FrontEndElement> children;
  string label_string_;
  string text_string_;
  string src_;
  // need to add these member fields : ["text_string", "disabled", "icon",
  //               "label_string", "onclick_id", "onchange_id", "options",
  //               "color_theme", "allow_multiple", "font_size",
  //               "margin", "value_integer", "value_integer_list", "height",
  //               "width", "element_id", "padding", "selected_tab",
  //               "border_width", "default_rows"]
  FrontEndElement() {}
  FrontEndElement(ElementType type): element_type(type) {};
  FrontEndElement& operator<<(FrontEndElement&& child_element) {
    children.push_back(std::move(child_element));
    return *this;
  }
  Json Export() const;
  FrontEndElement& text_string(const string& input) {
    this->text_string_ = input;
    return *this;
  }
  FrontEndElement& label_string(const string& input) {
    this->label_string_ = input;
    return *this;
  }
  FrontEndElement& src(const string& input) {
    this->src_ = input;
    return *this;
  }
};

FrontEndElement VDiv() {
  return FrontEndElement(FrontEndElement::VERTICAL_DIV);
}

FrontEndElement Text(const std::string& text_string) {
  return FrontEndElement(FrontEndElement::TEXT).text_string(text_string);
}


FrontEndElement Button(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::BUTTON).label_string(label_string);
}


FrontEndElement Image(const std::string& src) {
  return FrontEndElement(FrontEndElement::IMAGE).src(src);
}

}  // namespace webio

#endif //  _WEBIO_ELEMENTS_HPP_
