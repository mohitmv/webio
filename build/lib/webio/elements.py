from enum import IntEnum

class ElementType(IntEnum):
  TEXT = 1
  BUTTON = 2
  TEXT_INPUT = 3
  TEXT_AREA = 4
  DROP_DOWN = 5
  TOGGLE = 6
  MENU = 7
  ICON = 8
  HLIST = 9
  VLIST = 10
  CHECK_BOX = 11

class FrontEndElement(dict):
  def __init__(self, element_type, **kwargs):
    self.__dict__ = self;
    dict.__init__(self, element_type = element_type, **kwargs);

  def __lshift__(self, arg):
    self.children.append(arg);

  def Export(self):
    def ExportHelper(element):
      output = utils.Object();
      if element.element_type in set([ElementType.HLIST, ElementType.VLIST]):
        output.children = list(ExportHelper(i) for i in element.children);
      output.element_type = element.element_type.__str__().split(".")[1];
      if (element.element_type != ElementType.DROP_DOWN):
        output.value = element.value;
      for i in ["text_string", "disabled", "icon",
                "label_string", "onclick_id", "onchange_id", "options",
                "color_theme", "allow_multiple", "click_actions", "font_size",
                "margin", "value_integer", "value_integer_list"]:
        if i in element:
          output[i] = element[i];
      return output;
    return ExportHelper(self);

def Text(*text_strings, **params):
  return FrontEndElement(ElementType.TEXT,
                         text_strings = text_strings,
                         **params);

def Button(label_string = None, icon = None, **params):
  return FrontEndElement(ElementType.BUTTON,
                         label_string = label_string,
                         icon = icon,
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

def HList(*children, **params):
  return FrontEndElement(ElementType.HLIST,
                         children = children,
                         **params);

def VList(*children, **params):
  return FrontEndElement(ElementType.VLIST,
                         children = children,
                         **params);

def CheckBox(label_string, **params):
  return FrontEndElement(ElementType.CHECK_BOX,
                         label_string = label_string,
                         value = False,
                         **params);


############# Composite Elements ###########################

def TitleText(text_string, **params):
  return Text(text_string,
              font_size = "25px",
              margin_top_bottom = "5px"
              **params);

