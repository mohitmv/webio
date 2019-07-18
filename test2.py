import webio;
from webio import Action, Div, HDiv, Tabs, Tab, TitleText, Button, TextInput, TextArea;

class MyWebsite:
  tabs = ["Home", "About", "Contact", "Dashboard"];
  current_tab = 0;
  content_for_tabs = {0: ["Content-01", "Content-02"], 1: ["Content-11", "Content-12"],
                      2: [], 3: []};
  def Render(self):
    frame = Div();
    frame << TitleText("Welcome to webio") << VSpace(20);
    frame << Tabs(Tab(tabs[index],
                      onclick = Action(lambda index: self.set_current_tab(index),
                                       index)
                    ) for index in range(5));
    for c in self.content_for_tabs[self.current_tab]:
      frame << Card(c, color = "blue" if self.current_tab == 2 else "default");
    VSpace("10px");
    Text("Want to create more content ?", font_size = "16px",
                                          margin = "5px");
    frame << TextInput("Your Name ?") << TextArea("Your content goes here", id="content");
    frame << Button("Submit", onclick =
               lambda: content_for_tabs[current_tab].append(Find("content").value()));
    return frame;

  def set_current_tab(self, index):
    self.current_tab = index;

webio.Serve(MyWebsite, port=5002);
