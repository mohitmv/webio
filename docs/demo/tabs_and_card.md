Sample web interface : navbar with 4 tabs, each having cards for comments.

Here is an example of simple web interface having 4 tabs in navbar. Corrosponding to each tab, there is a list of cards, displaying some text. At the bottom, there is a form, which is used for adding more cards.

![alt text](https://i.imgur.com/wpiVJ14.gif "webio demo")

```python
import webio;
from webio import Action, Div, HDiv, HTabs, Tab, TitleText, Button, TextInput
from webio import TextArea, VSpace, Tab, HTabs, Card, Text;

class MyWebsite:
  tabs = ["Home", "About", "Contact", "Dashboard"];
  content_for_tabs = {0: ["Home-01", "Home-02"], 1: ["About-11", "About-12"],
                      2: ["Contact-01"], 3: ["Dashboard-01"]};
  def __init__(self):
    self.current_tab = 0;

  def Render(self):
    frame = Div();
    frame << TitleText("Welcome to webio") << VSpace("20px");
    frame << HTabs((Tab(self.tabs[index],
                      onclick = Action(lambda index: self.set_current_tab(index),
                                       index)
                    ) for index in range(len(self.tabs))),
                   padding = "0px 0px 0px 10px",
                   selected_tab = self.current_tab
                   );
    frame << VSpace("10px")
    for c in self.content_for_tabs[self.current_tab]:
      frame << Card(c, color = ("blue" if self.current_tab == 2 else "default"),
                       width = "50%");
    frame << VSpace("20px");
    Text("Want to create more content ?", font_size = "16px",
                                          margin = "5px");
    frame << TextInput("Your Name ?") << TextArea("Your content goes here",
                                                  id = "content");
    frame << Button("Submit", onclick =
               lambda: self.content_for_tabs[self.current_tab].append(
                                                     self.inputs["content"]));
    return frame;

  def set_current_tab(self, index):
    self.current_tab = index;

webio.Serve(MyWebsite, port=5002);
```
