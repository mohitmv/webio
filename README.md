Welcome to webio
===================


WebIO enables you to design the complex web interfaces without getting into HTML, CSS, JS, AngularJs, Ajax,
API handling, Server management, nodejs etc...

The web interface built by webio doesn't look pixel-perfect but it's good enough to support all the desired interaction.

Web interfaces which don't require pixel-perfect graphics like: admin panels, internal dashboard, server monitoring page, application's intenal control, jenkins website, etc.. can be built on webio.

webio offers a simple set of web elements to be included in your backend code ( C++ , Python or Java), which internally
build a fully functional web interface as desired. Once webio is integrated in program, it does everything to support backend API handling, as well as auto-generate the front-end of desired web-interface.
webio is extremely easy to use, having a 3-pager user manual.



How to use webio in python ?
----------

Here is an example of simple web interface having 4 tabs in navbar. Corrosponding to each tab, there is a list of cards, displaying some text. At the bottom, there is a form, which is used for adding more cards.

```python
import webio
from webio import Action, Div, HDiv, HTabs, Tab, TitleText, Button, TextInput
from webio import TextArea, VSpace, Tab, HTabs, Card, Text

class MyWebsite:
  tabs = ["Home", "About", "Contact", "Dashboard"];
  current_tab = 0;
  content_for_tabs = {0: ["Home-01", "Home-02"], 1: ["About-11", "About-12"],
                      2: ["Contact-01"], 3: ["Dashboard-01"]};
  def Render(self):
    frame = Div();
    frame << TitleText("Welcome to webio") << VSpace("20px");
    frame << HTabs((Tab(self.tabs[index],
                      onclick = Action(lambda index: self.set_current_tab(index),
                                       index)
                    ) for index in range(4)),
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

![alt text](https://raw.githubusercontent.com/mohitmv/webio/master/docs/webio_demo_slow_gif.gif "webio demo")



How to install webio in python ?
----------
`sudo pip3.6 install git+https://github.com/mohitmv/webio.git`

or

`sudo pip3.6 install git+https://github.com/mohitmv/webio.git@v1.0.0`

How to uninstall webio in python ?
----------
`sudo pip3.6 uninstall webio`



