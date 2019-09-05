import msl

input_elements = set(["TEXT_INPUT", "TEXT_AREA", "DROP_DOWN", "TOGGLE", "CHECK_BOX", "CHECK_BOX_LIST"]);
non_atomic_elements = set(["TEXT", "SIMPLE_DIV", "HORIZONTAL_DIV", "HORIZONTAL_TABS", "VERTICAL_TABS", "VERTICAL_DIV", "INLINED_DIV"]);
other_elements = set(["BUTTON", "MENU", "ICON", "IMAGE", "TAB", "ICON_BUTTON"]);
allowed_elements = input_elements | non_atomic_elements | other_elements;
valid_keys = set(["text_string", "disabled", "icon", "label_string",
                  "onclick_id", "onchange_id", "options",
                  "color_theme", "allow_multiple", "font_size",
                  "margin", "value_integer", "value_integer_list", "height",
                  "width", "element_id", "padding", "selected_tab",
                  "border_width", "default_rows", "children", "value", "element_type"]);

def is_valid_frame(frame):
  assert (frame != None);
  assert ("element_id" in frame);
  assert (frame["element_type"] in allowed_elements)
  for i in frame:
    assert (i in valid_keys), list(frame.keys());
  if (frame["element_type"] in non_atomic_elements):
    assert ("children" in frame);
    list(is_valid_frame(i) for i in frame["children"]);
  else:
    pass
    # assert ("children" not in frame);

def set_if_unset(dict_object, k, v):
  if k not in dict_object:
    dict_object[k] = v;

def frame_summary(frame):
  output = msl.Object();
  output.num_elements = 0;
  output.num_onclick_id = 0;
  output.elements = {};
  def frame_summary_recursive(sub_frame):
    output.num_elements += 1;
    set_if_unset(output.elements, sub_frame["element_type"], {"num_elements": 0});
    output.elements[sub_frame["element_type"]]["num_elements"] += 1;
    if "onclick_id" in sub_frame:
      output.num_onclick_id += 1;
    if "children" in sub_frame:
      for i in sub_frame["children"]:
        frame_summary_recursive(i);
  frame_summary_recursive(frame);
  return output;

def inlined_text(frame):
  output = frame["text_string"] if frame["element_type"] == "TEXT" else "";
  if "children" in frame:
    for i in frame["children"]:
      output += inlined_text(i);
  return output;


def find_button_onclick_id(frame, label_string):
  if (frame["element_type"] == "BUTTON"
     and frame["label_string"] == label_string
     and "onclick_id" in frame):
    return frame["onclick_id"];
  if "children" in frame:
    for i in frame["children"]:
      tmp = find_button_onclick_id(i, label_string);
      if (tmp != None):
        return tmp;
  return None;



