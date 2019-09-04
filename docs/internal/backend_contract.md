Role of Frontend and Backend
1. Start API of backend returns the HTML page with embedded CSS and JavaScript code into it.
2. Action API of backend returns frame object in json format, which is displayed by front-end code.
3. To support webio in various programming language, backend needs to be built in respective programming language. However frontend is common for all. Hence backend must confirm the front-end standard defined here.


Backend should support following APIs
1. Start API  : [GET] /
   - Loads the initial HTML page with stubbed css and javascript code.
   - Initial frame object is embedded in initial page, stored in javascript variable.
2. Start API in Json : [POST] /v1/start
  - Returns the initial frame object in json format. Doesn't load the html-css page.
3. Action API : [POST] /v1/action
  - Loads the subsequent frame whenever a action is triggered with registered action_id.
  - Example: Whenever a button is clicked, a backend API will be fired with action_id params. (ex: {action_id: 12}). Backend is expected to interpret the action_id, update the current frame, and return the new frame.
4. Diff Action API : [POST] /v1/action_diff
  - Works similar to Action API but doesn't return the complete frame instead it return the difference from previous frame.
  - Not implemented yet.


Backend frame must support following front-end-elements:
1. Input Elements: TextInput, TextArea, DropDown, CheckBox, Toggle, CheckBoxList
2. Non-Atomic Elements: Text, Div, HDiv, HTabs, VTabs, VDiv, InlinedDiv
3. Others Elements: Button, Menu, Icon, Image, IconButton


Frame Rules:
1. Every element must have element_id.
2. Every variant of button (i.e. Button, IconButton.. etc) and Every variant of Division (ie. HDiv, VDiv, Div, InlineDiv... etc) for which onclick is defined, must have onclick_id.
3. Every input, for which onchange is defined, must have onchange_id.
4. Every menu-item of menu, for which onclick is not null, must have onclick_id.


Checking validity of a frame:
1. Every frame element must have element_id.
2. Every Non-Atomic element must have children field.
3. 
