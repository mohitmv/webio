import webio, json
from webio import HList, VList, Text, Button

class TestWebsite:
  def __init__(self):
    self.num_row = 2;

  def inc_num_rows(self):
    self.num_row += 1;

  def Render(self):
    wout = VList();
    wout << Text("Test Website") << Button("Test Submit Button");
    wout << Button("Real Click", onclick=lambda: self.inc_num_rows());
    for i in range(self.num_row):
      wout << HList(Button("Row Button" + str(i)) for i in range(2));
    return wout;

frame_server = webio.FrameServer(TestWebsite);

first_frame = frame_server.HandleFirstTimeLoad();

second_frame = frame_server.HandleActionEvent(dict(action_id = 1,
                                                   client_instance_id = first_frame['client_instance_id'],
                                                   server_instance_id = first_frame['server_instance_id']));

assert(first_frame.error.error_code == "ErrorCodes.SUCCESS");
assert(second_frame.error.error_code == "ErrorCodes.SUCCESS");

assert(first_frame != second_frame);
assert(len(json.dumps(first_frame)) < len(json.dumps(second_frame)));
assert(json.dumps(first_frame).count("Row Button") == 4);
assert(json.dumps(second_frame).count("Row Button") == 6);


first_frame_instance_2 = frame_server.HandleFirstTimeLoad();

second_frame_instance_2 = frame_server.HandleActionEvent(
                            dict(action_id = 1,
                                 client_instance_id = first_frame_instance_2['client_instance_id'],
                                 server_instance_id = first_frame_instance_2['server_instance_id']));

assert(first_frame_instance_2.error.error_code == "ErrorCodes.SUCCESS");
assert(second_frame_instance_2.error.error_code == "ErrorCodes.SUCCESS");

assert(first_frame_instance_2 != second_frame_instance_2);
assert(len(json.dumps(first_frame_instance_2)) < len(json.dumps(second_frame_instance_2)));
assert(json.dumps(first_frame_instance_2).count("Row Button") == 4);
assert(json.dumps(second_frame_instance_2).count("Row Button") == 6);

assert(second_frame == second_frame_instance_2);
assert(first_frame.data == first_frame_instance_2.data);


print("Basic Test Passed");

