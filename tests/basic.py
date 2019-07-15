import webio
from webio import HList, VList, Text, Button

class TestWebsite:
  def __init__(self):
    self.num_row = 2;

  def inc_num_rows(self):
    self.num_row += 1;

  def Render(self):
    wout = VList();
    wout << Text("Test Website") << Button("Test Submit Button");
    wout << Button("Real Click", onclick=lambda: (print("Clicked on button"),
                                                  self.inc_num_rows()));
    for i in range(self.num_row):
      wout << HList(Button("Row Button" + str(i)) for i in range(2));
    return wout;

frame_server = webio.FrameServer(TestWebsite);

first_frame = frame_server.ReloadFrame();

second_frame = frame_server.HandleEvent(dict(action_id = 1));


print(first_frame);
print(second_frame);

