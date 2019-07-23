Sample web interface : GUI of linux file system

Here is simple GUI of linux file system, supporting file/folder navigation, deletion, cope-paste, cut-paste operation of files and folders. serving the current directory(where this python script is running) by default.

![alt text](https://i.imgur.com/A5c2SuS.gif "webio demo linux file system")

```python
import os;
import webio;
from webio import Action, Div, HDiv, HTabs, Tab, TitleText, Button, TextInput
from webio import TextArea, VSpace, Tab, HTabs, Card, Text, Menu, VDiv;
from webio import IconButton, Icon

class MyWebsite:
  def __init__(self):
    self.current_dir = os.getcwd();
    self.copied_moved_file = None;
    self.is_copied = True;

  def Back(self):
    self.current_dir = os.path.abspath(self.current_dir + "/..");

  def CopyMove(self, file_folder_name, is_copied = True):
    self.is_copied = is_copied;
    self.copied_moved_file = self.current_dir + "/" + file_folder_name;

  def Paste(self):
    os.system(("cp -r " if self.is_copied else "mv ") + self.copied_moved_file
                + " " + self.current_dir);
    self.copied_moved_file = None;

  def Render(self):
    frame = VDiv(padding = "0 0 0 20px");
    frame << TitleText("Welcome to filesystem") << VSpace("20px");
    frame << Text("Current: " + self.current_dir) << VSpace("10px");
    frame << Div(
              Button("Paste Here",
                     onclick = self.Paste,
                     disabled = (self.copied_moved_file == None)),
              Button("Home",
                     icon = "home",
                     onclick = lambda: self.__dict__.update(
                                                current_dir = os.getcwd())));
    frame << IconButton("arrow_back", onclick = self.Back);
    for i in os.listdir(self.current_dir):
      is_dir = os.path.isdir(self.current_dir + "/" + i);
      frame << HDiv(
                  Menu(
                    options = [
                      ["Delete", Action(lambda i: 
                                  os.system("rm -rf " + self.current_dir + "/" + i), i)],
                      ["Copy", Action(self.CopyMove, i, True)],
                      ["Move", Action(self.CopyMove, i, False)],
                     ],
                    width = "30px",
                    icon = "more_vert"
                  ),
                  Icon("folder" if is_dir else "insert_drive_file",
                       width = "30px"),
                  Div(Text(i),
                      onclick = Action(lambda i:
                          self.__dict__.update(
                            current_dir = self.current_dir + "/" + i
                          ), i) if is_dir else None),

              );
    return frame;

webio.Serve(MyWebsite, port=5002);
```
