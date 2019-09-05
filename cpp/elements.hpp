#ifndef _WEBIO_ELEMENTS_HPP_
#define _WEBIO_ELEMENTS_HPP_

#include <string>
#include <vector>

#include "utils.hpp"
#include <assert.h>
#include "toolchain/json11/json11.hpp"

namespace webio {
using std::vector;
using json11::Json;

class FrontEndElement {
 public:
  using string = std::string;
  enum ElementType {TEXT, BUTTON, TEXT_INPUT, TEXT_AREA, DROP_DOWN, TOGGLE, MENU, ICON, SIMPLE_DIV, HORIZONTAL_DIV, CHECK_BOX, IMAGE, CHECK_BOX_LIST, HORIZONTAL_TABS, VERTICAL_TABS, TAB, VERTICAL_DIV, INLINED_DIV, ICON_BUTTON};
  ElementType element_type;
  int element_id;
  std::vector<FrontEndElement> children;
  std::vector<int> menu_options_onclick_ids;
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
  using Action = std::function<void(void)>;

  // Auto Generated Block starts here

  // members_type_map = {
  //   "string": ["text_string", "icon", "label_string", "color_theme", "font_size", "margin", "height", "width", "padding", "border_width", "src", "id", "value"],
  //   "int":  ["default_rows", "selected_tab", "selected"],
  //   "bool": ["disabled", "allow_multiple", "on"],
  //   "std::vector<string>": ["options"],
  //   "std::vector<int>": ["selected_list"],
  //   "Action": ["onclick", "onchange"],
  //   "std::vector<std::pair<std::string, Action>>": ["menu_options"]
  // };
  // to_up = lambda x: x.title().replace("_", "")
  // output = "";
  // for (type, members) in members_type_map.items():
  //   for member in members:
  //     output += type + " " + member+"_;\n"
  //     output += "bool has_"+member+" = false;\n"
  //     output += "FrontEndElement& " + to_up(member) + "(const " + type  + "& input) {\n"
  //     output += "  this->" + member + "_ = input;\n"
  //     output += "  this->has_" + member + " = true;\n"
  //     output += "  return *this;\n"
  //     output += "}\n\n";
  // print(output);

  string text_string_;
  bool has_text_string = false;
  FrontEndElement& TextString(const string& input) {
    this->text_string_ = input;
    this->has_text_string = true;
    return *this;
  }

  string icon_;
  bool has_icon = false;
  FrontEndElement& Icon(const string& input) {
    this->icon_ = input;
    this->has_icon = true;
    return *this;
  }

  string label_string_;
  bool has_label_string = false;
  FrontEndElement& LabelString(const string& input) {
    this->label_string_ = input;
    this->has_label_string = true;
    return *this;
  }

  string color_theme_;
  bool has_color_theme = false;
  FrontEndElement& ColorTheme(const string& input) {
    this->color_theme_ = input;
    this->has_color_theme = true;
    return *this;
  }

  string font_size_;
  bool has_font_size = false;
  FrontEndElement& FontSize(const string& input) {
    this->font_size_ = input;
    this->has_font_size = true;
    return *this;
  }

  string margin_;
  bool has_margin = false;
  FrontEndElement& Margin(const string& input) {
    this->margin_ = input;
    this->has_margin = true;
    return *this;
  }

  string height_;
  bool has_height = false;
  FrontEndElement& Height(const string& input) {
    this->height_ = input;
    this->has_height = true;
    return *this;
  }

  string width_;
  bool has_width = false;
  FrontEndElement& Width(const string& input) {
    this->width_ = input;
    this->has_width = true;
    return *this;
  }

  string padding_;
  bool has_padding = false;
  FrontEndElement& Padding(const string& input) {
    this->padding_ = input;
    this->has_padding = true;
    return *this;
  }

  string border_width_;
  bool has_border_width = false;
  FrontEndElement& BorderWidth(const string& input) {
    this->border_width_ = input;
    this->has_border_width = true;
    return *this;
  }

  string src_;
  bool has_src = false;
  FrontEndElement& Src(const string& input) {
    this->src_ = input;
    this->has_src = true;
    return *this;
  }

  string id_;
  bool has_id = false;
  FrontEndElement& Id(const string& input) {
    this->id_ = input;
    this->has_id = true;
    return *this;
  }

  string value_;
  bool has_value = false;
  FrontEndElement& Value(const string& input) {
    this->value_ = input;
    this->has_value = true;
    return *this;
  }

  int default_rows_;
  bool has_default_rows = false;
  FrontEndElement& DefaultRows(const int& input) {
    this->default_rows_ = input;
    this->has_default_rows = true;
    return *this;
  }

  int selected_tab_;
  bool has_selected_tab = false;
  FrontEndElement& SelectedTab(const int& input) {
    this->selected_tab_ = input;
    this->has_selected_tab = true;
    return *this;
  }

  int selected_;
  bool has_selected = false;
  FrontEndElement& Selected(const int& input) {
    this->selected_ = input;
    this->has_selected = true;
    return *this;
  }

  bool disabled_;
  bool has_disabled = false;
  FrontEndElement& Disabled(const bool& input) {
    this->disabled_ = input;
    this->has_disabled = true;
    return *this;
  }

  bool allow_multiple_;
  bool has_allow_multiple = false;
  FrontEndElement& AllowMultiple(const bool& input) {
    this->allow_multiple_ = input;
    this->has_allow_multiple = true;
    return *this;
  }

  bool on_;
  bool has_on = false;
  FrontEndElement& On(const bool& input) {
    this->on_ = input;
    this->has_on = true;
    return *this;
  }

  std::vector<string> options_;
  bool has_options = false;
  FrontEndElement& Options(const std::vector<string>& input) {
    this->options_ = input;
    this->has_options = true;
    return *this;
  }

  std::vector<int> selected_list_;
  bool has_selected_list = false;
  FrontEndElement& SelectedList(const std::vector<int>& input) {
    this->selected_list_ = input;
    this->has_selected_list = true;
    return *this;
  }

  Action onclick_;
  bool has_onclick = false;
  FrontEndElement& Onclick(const Action& input) {
    this->onclick_ = input;
    this->has_onclick = true;
    return *this;
  }

  Action onchange_;
  bool has_onchange = false;
  FrontEndElement& Onchange(const Action& input) {
    this->onchange_ = input;
    this->has_onchange = true;
    return *this;
  }

  std::vector<std::pair<std::string, Action>> menu_options_;
  bool has_menu_options = false;
  FrontEndElement& MenuOptions(const std::vector<std::pair<std::string, Action>>& input) {
    this->menu_options_ = input;
    this->has_menu_options = true;
    return *this;
  }

  // Auto Generated Block ends here

};

FrontEndElement InlinedDiv() {
  return FrontEndElement(FrontEndElement::INLINED_DIV);
}

FrontEndElement VDiv() {
  auto output = FrontEndElement(FrontEndElement::VERTICAL_DIV);
  return output;
}

FrontEndElement HDiv() {
  auto output = FrontEndElement(FrontEndElement::HORIZONTAL_DIV);
  return output;
}

FrontEndElement Div() {
  auto output = FrontEndElement(FrontEndElement::SIMPLE_DIV);
  return output;
}

FrontEndElement VDiv(vector<FrontEndElement>&& input) {
  auto output = FrontEndElement(FrontEndElement::VERTICAL_DIV);
  output.children = input;
  return output;
}

FrontEndElement HDiv(vector<FrontEndElement>&& input) {
  auto output = FrontEndElement(FrontEndElement::HORIZONTAL_DIV);
  output.children = input;
  return output;
}

FrontEndElement Div(vector<FrontEndElement>&& input) {
  auto output = FrontEndElement(FrontEndElement::SIMPLE_DIV);
  output.children = input;
  return output;
}

FrontEndElement InlinedDiv(vector<FrontEndElement>&& input) {
  auto output = FrontEndElement(FrontEndElement::INLINED_DIV);
  output.children = input;
  return output;
}

FrontEndElement Icon(const std::string& icon) {
  return FrontEndElement(FrontEndElement::ICON)
          .Icon(icon)
          .FontSize("16px");
}

FrontEndElement IconButton(const std::string& icon) {
  return FrontEndElement(FrontEndElement::ICON_BUTTON)
            .Icon(icon)
            .Disabled(false);
}

FrontEndElement TextInput(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::TEXT_INPUT)
            .LabelString(label_string)
            .Disabled(false)
            .Value("");
}

FrontEndElement TextArea(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::TEXT_AREA)
            .LabelString(label_string)
            .Value("")
            .DefaultRows(5)
            .Disabled(false);
}

FrontEndElement DropDown(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::DROP_DOWN)
            .LabelString(label_string)
            .Disabled(false)
            .AllowMultiple(false)
            .Selected(0)
            .SelectedList({})
            .Options({});
}

FrontEndElement Toggle(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::TOGGLE)
            .LabelString(label_string)
            .Disabled(false)
            .On(false);
}

FrontEndElement CheckBox(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::CHECK_BOX)
            .LabelString(label_string)
            .On(false);
}

FrontEndElement CheckBoxList(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::CHECK_BOX_LIST)
            .LabelString(label_string)
            .Disabled(false)
            .AllowMultiple(false)
            .Options({})
            .Selected(0)
            .SelectedList({});
}

FrontEndElement Menu(const std::string& icon) {
  return FrontEndElement(FrontEndElement::MENU)
          .Icon(icon)
          .FontSize("16px")
          .MenuOptions({})
          .Disabled(true);
}

FrontEndElement VSpace(const std::string& size) {
  return VDiv().Height(size);
}

FrontEndElement Text(const std::string& text_string) {
  return FrontEndElement(FrontEndElement::TEXT).TextString(text_string);
}

FrontEndElement Text(const std::vector<FrontEndElement>& inputs) {
  auto output = FrontEndElement(FrontEndElement::TEXT);
  output.children = inputs;
  return output;
}

FrontEndElement HTabs() {
  return FrontEndElement(FrontEndElement::HORIZONTAL_TABS);
}

FrontEndElement VTabs() {
  return FrontEndElement(FrontEndElement::VERTICAL_TABS);
}

FrontEndElement Tab(const std::string& text_string) {
  return FrontEndElement(FrontEndElement::TAB).TextString(text_string);
}

FrontEndElement Button(const std::string& label_string) {
  return FrontEndElement(FrontEndElement::BUTTON)
            .LabelString(label_string)
            .Disabled(false)
            .ColorTheme("default");
}


FrontEndElement Image(const std::string& src) {
  return FrontEndElement(FrontEndElement::IMAGE).Src(src);
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
