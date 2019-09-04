```C++

1. Input Elements: TextInput, TextArea, DropDown, CheckBox, Toggle, CheckBoxList
2. Non-Atomic Elements: Div, HDiv, HTabs, VTabs, VDiv, InlinedDiv
3. Display Elements: Text, Button, Menu, Icon, Image, IconButton

```


```C++

members of `webio::BaseInterface`:

InputObject Input(const string& element_id)

1.
InputObject::Value():
  - returns string.
  - used for TextInput, TextArea

2.
InputObject::On():
  - returns bool.
  - used for Toggle, CheckBox

3.
InputObject::Selected():
  - returns int
  - used for DropDown[allow_multiple=False], CheckBoxList[allow_multiple=False]

4.
InputObject::SelectedList():
  - returns vector<int>
  - used for DropDown[allow_multiple=True], CheckBoxList[allow_multiple=True]


```

```C++

APIs to define default values in input elements.

1. TextInput, TextArea
  - Value(std::string)
  - used for declaring default value string in a TextInput or TextArea.

2. Toggle, CheckBox
  - On(bool)
  - used for declaring default state of checkbox or toggle switch.

3. DropDown and CheckBoxList:
  - .Options(vector<string>)
  - .Options(vector<int>)
  - .Selected(int):
    - index of default selected option. (indexeing starts from 0).
    - used for [allow_multiple=False] case.
  - .SelectedList(vector<int>)
    - list of indexes of default selected options. (indexeing starts from 0)
    - used for [allow_multiple=True] case.  

```

