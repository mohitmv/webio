import webio, time;
from webio import Action, Div, HDiv, HTabs, Tab, TitleText, Button, TextInput
from webio import TextArea, VSpace, Tab, HTabs, Card, Text;

class MyWebsite:
  def __init__(self):
    self.num_additional_bottom_text = 0;

  def Render(self):
    frame = Div()
    frame << Div(
      Text("Mohit Saini"),
      TextInput("Your Name ?"),
      Button("Click Me", onclick = lambda: self.__dict__.update(num_additional_bottom_text = 1+self.num_additional_bottom_text)),
    )
    frame << HDiv(
      Text("First Part "),
      Text("There is something in the middle of this line"),
      Text("Last Part ")
    )
    frame << TextInput("Your Last Name ?")
    frame << Text("Saini Mohit")
    for i in range(self.num_additional_bottom_text):
      frame << Text("--- In the Updated Middle And Updated Saini Mohit");
    return frame;

webio.Serve(MyWebsite, port=5002);

