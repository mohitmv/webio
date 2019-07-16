import json, webio
from webio import HList, VList, Text, Button, TextInput

class TestWebsite:
  def __init__(self):
    self.num_row = 2;
    self.main_content = "pppp00000";

  def inc_num_rows(self):
    self.num_row += 1;

  def update_content(self):
    self.main_content = self.inputs.content;
    print("Main Content now = ", self.main_content);

  def Render(self):
    wout = VList();
    wout << Text("Test Website") << Button("Test Submit Button");
    wout << TextInput("Your content ?", index = "content");
    wout << Button("Real Click", onclick=lambda: self.inc_num_rows());
    wout << Button("Real Click - 2", onclick = self.update_content);
    wout << Text(self.main_content)
    for i in range(self.num_row):
      wout << HList(Button("Row Button" + str(i)) for i in range(2));
    return wout;

# frame_server = webio.FrameServer(TestWebsite);

webio.Serve(TestWebsite, port = 5001, activate_instance_cleaner = False);

