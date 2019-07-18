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
import webio;
from webio import Frame, Action, VList, HList, Tabs, Tab, TitleText, Button, TextInput, TextArea;

class MyWebsite:
  tabs = ["Home", "About", "Contact", "Dashboard"];
  current_tab = 0;
  content_for_tabs = {0: ["Content-01", "Content-02"], 1: ["Content-11", "Content-12"],
                      2: [], 3: []};
  def Render(self):
    frame = VList();
    frame << TitleText("Welcome to webio") << VSpace(20);
    frame << Tabs(5, lambda index:
                Tab(tabs[index],
                    onclick = Action(index, lambda index: self.set_current_tab(index)));
    for c in self.content_for_tabs[current_tab]:
      frame << Card(c, color = "blue" if current_tab == 2 else "default");
    VSpace(10);
    Text("Want to create more content ?", font_size = 16, margin_top_bottom: 5);
    frame << TextInput("Your Name ?") << TextArea("Your content goes here", id="content");
    frame << Button("Submit", onclick =
               lambda: content_for_tabs[current_tab].append(Find("content").value()));
    return frame;

  def set_current_tab(self, index):
    self.current_tab = index;

webio.ServeFrame(MyWebsite(), port=5002);

```



How to install webio in python ?
----------
`sudo pip3.6 install git+https://github.com/mohitmv/webio.git`

or

`sudo pip3.6 install git+https://github.com/mohitmv/webio.git@v1.0.0`

How to uninstall webio in python ?
----------
`sudo pip3.6 uninstall webio`



