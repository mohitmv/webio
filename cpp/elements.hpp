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

  string label_string;
  bool has_label_string = false;

  string text_string;
  bool has_text_string = false;

  string src;
  bool has_src = false;

  string icon;
  bool has_icon = false;

  std::vector<string> options;
  bool has_options = false;

  int size;
  bool has_size = false;

  bool disabled;
  bool has_disabled = false;

  int onclick_id;
  bool has_onclick_id = false;

  int onchange_id;
  bool has_onchange_id = false;

  string color_theme;
  bool has_color_theme = false;

  bool allow_multiple;
  bool has_allow_multiple = false;

  string font_size;
  bool has_font_size = false;

  string margin;
  bool has_margin = false;

  string padding;
  bool has_padding = false;

  int value_integer;
  bool has_value_integer = false;

  std::vector<int> value_integer_list;
  bool has_value_integer_list = false;

  string height;
  bool has_height = false;

  string width;
  bool has_width = false;

  int element_id;
  bool has_element_id = false;

  string border_width;
  bool has_border_width = false;

  int selected_tab;
  bool has_selected_tab = false;

  int default_rows;
  bool has_default_rows = false;

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
  FrontEndElement& set_text_string(const string& input) {
    this->text_string = input;
    this->has_text_string = true;
    return *this;
  }
  FrontEndElement& set_label_string(const string& input) {
    this->label_string = input;
    this->has_label_string = true;
    return *this;
  }
  FrontEndElement& set_src(const string& input) {
    this->src = input;
    this->has_src = true;
    return *this;
  }
  FrontEndElement& set_icon(const string& input) {
    this->icon = input;
    this->has_icon = true;
    return *this;
  }
  FrontEndElement& set_options(const std::vector<string>& input) {
    this->options = input;
    this->has_options = true;
    return *this;
  }
  FrontEndElement& add_option(const string& input) {
    this->options.push_back(input);
    this->has_options = true;
    return *this;
  }
  FrontEndElement& set_size(int size) {
    this->size = size;
    this->has_size = true;
    return *this;
  }
  FrontEndElement& set_disabled(bool disabled) {
    this->disabled = disabled;
    this->has_disabled = true;
    return *this;
  }
  FrontEndElement& set_onclick_id(int onclick_id) {
    this->onclick_id = onclick_id;
    this->has_onclick_id = true;
    return *this;
  }
  FrontEndElement& set_onchange_id(int onchange_id) {
    this->onchange_id = onchange_id;
    this->has_onchange_id = true;
    return *this;
  }
  FrontEndElement& set_color_theme(const std::string& color_theme) {
    this->color_theme = color_theme;
    this->has_color_theme = true;
    return *this;
  }
  FrontEndElement& set_allow_multiple(bool allow_multiple) {
    this->allow_multiple = allow_multiple;
    this->has_allow_multiple = true;
    return *this;
  }
  FrontEndElement& set_font_size(const std::string& font_size) {
    this->font_size = font_size;
    this->has_font_size = true;
    return *this;
  }
  FrontEndElement& set_margin(const std::string& margin) {
    this->margin = margin;
    this->has_margin = true;
    return *this;
  }
  FrontEndElement& set_padding(const std::string& padding) {
    this->padding = padding;
    this->has_padding = true;
    return *this;
  }
  FrontEndElement& set_height(const std::string& height) {
    this->height = height;
    this->has_height = true;
    return *this;
  }
  FrontEndElement& set_width(const std::string& width) {
    this->width = width;
    this->has_width = true;
    return *this;
  }
  FrontEndElement& set_border_width(const std::string& border_width) {
    this->border_width = border_width;
    this->has_border_width = true;
    return *this;
  }
  FrontEndElement& set_value_integer(int value_integer) {
    this->value_integer = value_integer;
    this->has_value_integer = true;
    return *this;
  }
  FrontEndElement& set_element_id(int element_id) {
    this->element_id = element_id;
    this->has_element_id = true;
    return *this;
  }
  FrontEndElement& set_value_integer_list(const std::vector<int>& value_integer_list) {
    this->value_integer_list = value_integer_list;
    this->has_value_integer_list = true;
    return *this;
  }
  FrontEndElement& set_default_rows(int default_rows) {
   this->default_rows = default_rows;
   this->has_default_rows = true;
   return *this;
  }
  FrontEndElement& set_selected_tab(int selected_tab) {
    this->selected_tab = selected_tab;
    this->has_selected_tab = true;
    return *this;
  }
};

FrontEndElement VDiv() {
  return FrontEndElement(FrontEndElement::VERTICAL_DIV);
}

FrontEndElement HDiv() {
  return FrontEndElement(FrontEndElement::HORIZONTAL_DIV);
}

FrontEndElement Div() {
  return FrontEndElement(FrontEndElement::SIMPLE_DIV);
}

FrontEndElement IconButton(const std::string& icon) {
  return FrontEndElement(FrontEndElement::ICON_BUTTON).set_icon(icon);
}

FrontEndElement TextInput(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::TEXT_INPUT).set_label_string(label_string);
}

FrontEndElement TextArea(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::TEXT_AREA).set_label_string(label_string);
}

FrontEndElement DropDown(const std::string& label_string, const std::vector<std::string>& options) {
  return FrontEndElement(FrontEndElement::DROP_DOWN)
      .set_label_string(label_string)
      .set_options(options);
}

FrontEndElement Toggle(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::TOGGLE).set_label_string(label_string);
}

FrontEndElement CheckBox(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::CHECK_BOX).set_label_string(label_string);
}

FrontEndElement CheckBoxList(const std::string& label_string, const std::vector<std::string>& options) {
  return FrontEndElement(FrontEndElement::CHECK_BOX_LIST)
      .set_label_string(label_string)
      .set_options(options);
}

FrontEndElement Menu(const std::vector<std::string>& options) {
  return FrontEndElement(FrontEndElement::MENU).set_options(options);
}

FrontEndElement VSpace(int size) {
  return Div().set_size(size);
}

FrontEndElement Text(const std::string& text_string) {
  return FrontEndElement(FrontEndElement::TEXT).set_text_string(text_string);
}

FrontEndElement HorizontalTabs() {
  return FrontEndElement(FrontEndElement::HORIZONTAL_TABS);
}

FrontEndElement VerticalTabs() {
  return FrontEndElement(FrontEndElement::VERTICAL_TABS);
}

FrontEndElement Tab(const std::string& text_string) {
  return FrontEndElement(FrontEndElement::TAB).set_text_string(text_string);
}

FrontEndElement InlinedDiv() {
  return FrontEndElement(FrontEndElement::INLINED_DIV);
}

FrontEndElement Button(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::BUTTON).set_label_string(label_string);
}


FrontEndElement Image(const std::string& src) {
  return FrontEndElement(FrontEndElement::IMAGE).set_src(src);
}

}  // namespace webio

#endif //  _WEBIO_ELEMENTS_HPP_
