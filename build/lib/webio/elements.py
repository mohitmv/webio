from enum import IntEnum
import webio.utils as utils

class ElementType(IntEnum):
  TEXT = 1
  BUTTON = 2
  TEXT_INPUT = 3
  TEXT_AREA = 4
  DROP_DOWN = 5
  TOGGLE = 6
  MENU = 7
  ICON = 8
  DIV = 9
  HORIZONTAL_DIV = 10
  CHECK_BOX = 11
  IMAGE = 12
  CHECK_BOX_LIST = 13
  HORIZONTAL_TABS = 14
  VERTICAL_TABS = 15
  TAB = 16
  def IsInputElement(self):
    return self in set([self.DROP_DOWN, self.CHECK_BOX, self.CHECK_BOX_LIST,
                        self.TOGGLE, self.TEXT_INPUT, self.TEXT_AREA]);

  def HaveChildren(self):
    return self in set([self.TEXT, self.HORIZONTAL_DIV, self.DIV,
                        self.HORIZONTAL_TABS, self.VERTICAL_TABS]);

class FrontEndElement(dict):
  def __init__(self, element_type, **kwargs):
    self.__dict__ = self;
    dict.__init__(self, element_type = element_type, **kwargs);

  def __lshift__(self, arg):
    self.children.append(arg);
    return self;

  def Export(self):
    def ExportHelper(element):
      output = utils.Object();
      if element.element_type in set([ElementType.HORIZONTAL_DIV,
                                      ElementType.DIV,
                                      ElementType.TEXT,
                                      ElementType.HORIZONTAL_TABS,
                                      ElementType.VERTICAL_TABS]):
        output.children = list(ExportHelper(i) for i in element.children);
      output.element_type = element.element_type.__str__().split(".")[1];
      considered_fields = ["text_string", "disabled", "icon",
                "label_string", "onclick_id", "onchange_id", "options",
                "color_theme", "allow_multiple", "click_actions", "font_size",
                "margin", "value_integer", "value_integer_list", "height",
                "width", "element_id", "padding", "selected_tab",
                "border_width", "default_rows"];
      if (element.element_type != ElementType.DROP_DOWN):
        considered_fields.append("value");
      for i in considered_fields:
        if i in element:
          output[i] = element[i];
      return output;
    return ExportHelper(self);

def Text(*children, **params):
  return FrontEndElement(ElementType.TEXT,
                         children = list(children),
                         **params);

def Image(src, **params):
  return FrontEndElement(ElementType.IMAGE,
                         src = src,
                         **params);

def Button(label_string = None, **params):
  return FrontEndElement(ElementType.BUTTON,
                         label_string = label_string,
                         disabled = False,
                         # default | back_in_white | blue
                         color_theme = "default",
                         **params);

def TextInput(label_string, **params):
  return FrontEndElement(ElementType.TEXT_INPUT,
                         label_string = label_string,
                         disabled = False,
                         value = "",
                         **params);

def TextArea(label_string, **params):
  return FrontEndElement(ElementType.TEXT_AREA,
                         label_string = label_string,
                         value = "",
                         disabled = False,
                         default_rows = 5,
                         **params);

def DropDown(label_string, **params):
  return FrontEndElement(ElementType.DROP_DOWN,
                         label_string = label_string,
                         disabled = False,
                         options = [],
                         value = None,
                         allow_multiple = False,
                         **params);

def CheckBoxList(label_string, **params):
  return FrontEndElement(ElementType.CHECK_BOX_LIST,
                         label_string = label_string,
                         disabled = False,
                         allow_multiple = False,
                         options = [],
                         value = None,
                         **params);

def Toggle(label_string, **params):
  return FrontEndElement(ElementType.TOGGLE,
                         label_string = label_string,
                         disabled = False,
                         value = False,
                         **params);

def Menu(icon = "menu", **params):
  return FrontEndElement(ElementType.MENU,
                         icon = icon,  # https://material.io/tools/icons
                         font_size = "16px",
                         disabled = False,
                         click_actions = [],
                         **params);

def Icon(icon, **params):
  return FrontEndElement(ElementType.ICON,
                         icon = icon,  # https://material.io/tools/icons
                         font_size = "16px",
                         **params);

def HDiv(*children, **params):
  return FrontEndElement(ElementType.HORIZONTAL_DIV,
                         children = list(children),
                         **params);

def Div(*children, **params):
  return FrontEndElement(ElementType.DIV,
                         children = list(children),
                         **params);

def CheckBox(label_string, **params):
  return FrontEndElement(ElementType.CHECK_BOX,
                         label_string = label_string,
                         value = False,
                         **params);

def HTabs(*children, **params):
  output = FrontEndElement(ElementType.HORIZONTAL_TABS,
                           selected_tab = -1,
                           children = children);
  output.update(params);
  return output;

def Tab(text_string, **params):
  return FrontEndElement(ElementType.TAB,
                         text_string = text_string,
                         **params);


############# Composite Elements ###########################

def TitleText(text_string, **params):
  return Text(text_string,
              font_size = "25px",
              margin = "5px 0px",
              **params);

def VSpace(size):
  return Div(height = size);

def Card(text_string, **params):
  return Div(text_string, padding = "5px", margin = "5px", border_width = "1px", **params);

