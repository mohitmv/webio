```C++

1. Input Elements: TextInput, TextArea, DropDown, CheckBox, Toggle, CheckBoxList
2. Non-Atomic Elements: Div, HDiv, HTabs, VTabs, VDiv, InlinedDiv
3. Display Elements: Text, Button, Menu, Icon, Image, IconButton

```


```C++

members of `webio::BaseInterface`:

1.
InputString(const string& element_id):
  - returns string.
  - used for TextInput, TextArea

2.
InputBool(const string& element_id):
  - returns bool.
  - used for Toggle, CheckBox

3.
InputInt(const string& element_id):
  - returns int
  - used for DropDown[allow_multiple=False], CheckBoxList[allow_multiple=False]

4.
InputList(const string& element_id):
  - returns vector<int>
  - used for DropDown[allow_multiple=True], CheckBoxList[allow_multiple=True]


```