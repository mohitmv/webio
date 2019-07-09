Welcome to webio
===================


WebIO enables you to design the complex web interfaces without getting into HTML, CSS, JS, AngularJs, Ajax,
API handling, Server management, nodejs etc.. crap.

Resultant web interface will look ugly enough to prevent us from releasing it for customers, but it’s still good enough
 to support all the interaction we want, and not as bad as required to suicide out of frustration.

Think about designing admin panels, cluster creation dashboard,server monitoring page, product controlling page,
 jenkin’s website etc.., all of these websites can be built by adding a few more lines of code to the backend itself.

webio offers a simple set of web elements to be included in your program ( C++ or Python), which internally
translates to build a fully functional web interface we desired. Once you integrate webio program, it does
everything internally to support backend API handle, as well as auto-generate the front-end of your web-interface.
WebIO is extremely easy to use, with very simple 3-pager user manual.



How to use webio in a python ?
----------
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

