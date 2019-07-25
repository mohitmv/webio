#ifndef _WEBIO_ELEMENTS_HPP_
#define _WEBIO_ELEMENTS_HPP_

#include <string>
#include <vector>

#include "utils.hpp"
#include <assert.h>

namespace webio {

class FrontEndElement {
 public:
  using string = std::string;
  enum ElementType {TEXT, BUTTON, TEXT_INPUT, TEXT_AREA, DROP_DOWN, TOGGLE, MENU, ICON, SIMPLE_DIV, HORIZONTAL_DIV, CHECK_BOX, IMAGE, CHECK_BOX_LIST, HORIZONTAL_TABS, VERTICAL_TABS, TAB, VERTICAL_DIV, INLINED_DIV, ICON_BUTTON};
  ElementType element_type;
  std::vector<FrontEndElement> children;
  int onchange_id, onclick_id;

  FrontEndElement() {}
  FrontEndElement(ElementType type): element_type(type) {};
  FrontEndElement& operator<<(FrontEndElement&& child_element) {
    children.push_back(std::move(child_element));
    return *this;
  }
  FrontEndElement& operator<<(const FrontEndElement& child_element) {
    children.push_back(child_element);
    return *this;
  }
  bool HasChildren() {
    // ToDo(Implement this..)
    // assert(false);
    return (children.size() > 0);
  }
  Json Export() const;

  // members_type_map = {
  //   "string": ["text_string", "icon", "label_string", "color_theme", "font_size", "margin", "height", "width", "padding", "border_width", "src", "id"],
  //   "int":  ["value_integer", "default_rows", "selected_tab"],
  //   "bool": ["disabled", "allow_multiple"],
  //   "std::vector<string>": ["options"],
  //   "std::vector<int>": [],
  //   "std::function<void(void)>": ["onclick", "onchange"]
  // };
  // output = "";
  // for (type, members) in members_type_map.items():
  //   for member in members:
  //     output += type + " " + member+"_;\n"
  //     output += "bool has_"+member+" = false;\n"
  //     output += "FrontEndElement& " + member + "(const " + type  + "& input) {\n"
  //     output += "  this->" + member + "_ = input;\n"
  //     output += "  this->has_" + member + " = true;\n"
  //     output += "  return *this;\n"
  //     output += "}\n\n";
  // print(output);

  string text_string_;
  bool has_text_string = false;
  FrontEndElement& text_string(const string& input) {
    this->text_string_ = input;
    this->has_text_string = true;
    return *this;
  }

  string icon_;
  bool has_icon = false;
  FrontEndElement& icon(const string& input) {
    this->icon_ = input;
    this->has_icon = true;
    return *this;
  }

  string label_string_;
  bool has_label_string = false;
  FrontEndElement& label_string(const string& input) {
    this->label_string_ = input;
    this->has_label_string = true;
    return *this;
  }

  string color_theme_;
  bool has_color_theme = false;
  FrontEndElement& color_theme(const string& input) {
    this->color_theme_ = input;
    this->has_color_theme = true;
    return *this;
  }

  string font_size_;
  bool has_font_size = false;
  FrontEndElement& font_size(const string& input) {
    this->font_size_ = input;
    this->has_font_size = true;
    return *this;
  }

  string margin_;
  bool has_margin = false;
  FrontEndElement& margin(const string& input) {
    this->margin_ = input;
    this->has_margin = true;
    return *this;
  }

  string height_;
  bool has_height = false;
  FrontEndElement& height(const string& input) {
    this->height_ = input;
    this->has_height = true;
    return *this;
  }

  string width_;
  bool has_width = false;
  FrontEndElement& width(const string& input) {
    this->width_ = input;
    this->has_width = true;
    return *this;
  }

  string padding_;
  bool has_padding = false;
  FrontEndElement& padding(const string& input) {
    this->padding_ = input;
    this->has_padding = true;
    return *this;
  }

  string border_width_;
  bool has_border_width = false;
  FrontEndElement& border_width(const string& input) {
    this->border_width_ = input;
    this->has_border_width = true;
    return *this;
  }

  string src_;
  bool has_src = false;
  FrontEndElement& src(const string& input) {
    this->src_ = input;
    this->has_src = true;
    return *this;
  }

  string id_;
  bool has_id = false;
  FrontEndElement& id(const string& input) {
    this->id_ = input;
    this->has_id = true;
    return *this;
  }

  int value_integer_;
  bool has_value_integer = false;
  FrontEndElement& value_integer(const int& input) {
    this->value_integer_ = input;
    this->has_value_integer = true;
    return *this;
  }

  int default_rows_;
  bool has_default_rows = false;
  FrontEndElement& default_rows(const int& input) {
    this->default_rows_ = input;
    this->has_default_rows = true;
    return *this;
  }

  int selected_tab_;
  bool has_selected_tab = false;
  FrontEndElement& selected_tab(const int& input) {
    this->selected_tab_ = input;
    this->has_selected_tab = true;
    return *this;
  }

  bool disabled_;
  bool has_disabled = false;
  FrontEndElement& disabled(const bool& input) {
    this->disabled_ = input;
    this->has_disabled = true;
    return *this;
  }

  bool allow_multiple_;
  bool has_allow_multiple = false;
  FrontEndElement& allow_multiple(const bool& input) {
    this->allow_multiple_ = input;
    this->has_allow_multiple = true;
    return *this;
  }

  std::vector<string> options_;
  bool has_options = false;
  FrontEndElement& options(const std::vector<string>& input) {
    this->options_ = input;
    this->has_options = true;
    return *this;
  }

  std::vector<std::pair<std::string, std::function<void(void)> > > actionable_menu_options_;
  bool has_actionable_menu_options = false;
  FrontEndElement& options(const std::vector<std::pair<std::string, std::function<void(void)> > >& input) {
    this->actionable_menu_options_ = input;
    this->has_actionable_menu_options = true;
    return *this;
  }

  std::vector<std::pair<std::string, int> > frontend_menu_options_;
  bool has_frontend_menu_options = false;
  FrontEndElement& options(const std::vector<std::pair<std::string, int> >& input) {
    this->frontend_menu_options_ = input;
    this->has_frontend_menu_options = true;
    return *this;
  }

  std::function<void(void)> onclick_;
  bool has_onclick = false;
  FrontEndElement& onclick(const std::function<void(void)>& input) {
    this->onclick_ = input;
    this->has_onclick = true;
    return *this;
  }

  std::function<void(void)> onchange_;
  bool has_onchange = false;
  FrontEndElement& onchange(const std::function<void(void)>& input) {
    this->onchange_ = input;
    this->has_onchange = true;
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

FrontEndElement Icon(const std::string& icon) {
  return FrontEndElement(FrontEndElement::ICON).icon(icon);
}

FrontEndElement IconButton(const std::string& icon) {
  return FrontEndElement(FrontEndElement::ICON_BUTTON).icon(icon);
}

FrontEndElement TextInput(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::TEXT_INPUT).label_string(label_string);
}

FrontEndElement TextArea(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::TEXT_AREA).label_string(label_string);
}

FrontEndElement DropDown(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::DROP_DOWN)
      .label_string(label_string);
}

FrontEndElement Toggle(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::TOGGLE).label_string(label_string);
}

FrontEndElement CheckBox(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::CHECK_BOX).label_string(label_string);
}

FrontEndElement CheckBoxList(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::CHECK_BOX_LIST)
      .label_string(label_string);
}

FrontEndElement Menu(const std::vector<std::pair<std::string, int> >& options) {
  return FrontEndElement(FrontEndElement::MENU).options(options);
}

FrontEndElement VSpace(const std::string& size) {
  return VDiv().height(size);
}

FrontEndElement Text(const std::string& text_string) {
  return FrontEndElement(FrontEndElement::TEXT).text_string(text_string);
}

FrontEndElement HTabs() {
  return FrontEndElement(FrontEndElement::HORIZONTAL_TABS);
}

FrontEndElement VTabs() {
  return FrontEndElement(FrontEndElement::VERTICAL_TABS);
}

FrontEndElement Tab(const std::string& text_string) {
  return FrontEndElement(FrontEndElement::TAB).text_string(text_string);
}

FrontEndElement InlinedDiv() {
  return FrontEndElement(FrontEndElement::INLINED_DIV);
}

FrontEndElement Button(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::BUTTON).label_string(label_string);
}


FrontEndElement Image(const std::string& src) {
  return FrontEndElement(FrontEndElement::IMAGE).src(src);
}

// print("\n".join("case FrontEndElement::" + i + ":\n  return \"" + i + "\";" for i in a))
std::string ElementTypeString(FrontEndElement::ElementType type) {
  switch (type) {
    case FrontEndElement::TEXT:
      return "TEXT";
    case FrontEndElement::BUTTON:
      return "BUTTON";
    case FrontEndElement::TEXT_INPUT:
      return "TEXT_INPUT";
    case FrontEndElement::TEXT_AREA:
      return "TEXT_AREA";
    case FrontEndElement::DROP_DOWN:
      return "DROP_DOWN";
    case FrontEndElement::TOGGLE:
      return "TOGGLE";
    case FrontEndElement::MENU:
      return "MENU";
    case FrontEndElement::ICON:
      return "ICON";
    case FrontEndElement::SIMPLE_DIV:
      return "SIMPLE_DIV";
    case FrontEndElement::HORIZONTAL_DIV:
      return "HORIZONTAL_DIV";
    case FrontEndElement::CHECK_BOX:
      return "CHECK_BOX";
    case FrontEndElement::IMAGE:
      return "IMAGE";
    case FrontEndElement::CHECK_BOX_LIST:
      return "CHECK_BOX_LIST";
    case FrontEndElement::HORIZONTAL_TABS:
      return "HORIZONTAL_TABS";
    case FrontEndElement::VERTICAL_TABS:
      return "VERTICAL_TABS";
    case FrontEndElement::TAB:
      return "TAB";
    case FrontEndElement::VERTICAL_DIV:
      return "VERTICAL_DIV";
    case FrontEndElement::INLINED_DIV:
      return "INLINED_DIV";
    case FrontEndElement::ICON_BUTTON:
      return "ICON_BUTTON";
    default: assert(false);
  }
  return "";
}




}  // namespace webio

#endif //  _WEBIO_ELEMENTS_HPP_
