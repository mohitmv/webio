import requests, tests.helpers, subprocess, json, tests.helpers

###################### interface_1: ###########################
#
# Div(
#   Div(
#     Text("Mohit Saini"),
#     TextInput("Your Name ?"),
#     Button("Click Me"),
#   )
#   HDiv(
#     Text("First Part "),
#     Text("There is something in the middle of this line"),
#     Text("Last Part ")
#   )
#   TextInput("Your Last Name ?"),
#   Text("Saini Mohit")
# )

def interface_1_basic_test(backend_url):
  first_frame = json.loads(requests.post(backend_url+"/v1/start").text);
  assert first_frame["error"]["error_code"] == "SUCCESS", first_frame;
  first_frame = first_frame["frame"];
  tests.helpers.is_valid_frame(first_frame);
  summary = tests.helpers.frame_summary(first_frame);
  assert summary.num_elements == 11, summary;
  assert summary.elements["TEXT_INPUT"]["num_elements"] == 2, summary;
  assert summary.elements["BUTTON"]["num_elements"] == 1, summary;
  assert ("TEXT_AREA" not in summary.elements), summary;
  assert summary.num_onclick_id == 1, summary;
  inlined_text = tests.helpers.inlined_text(first_frame);
  assert inlined_text[:11] == "Mohit Saini", summary;
  assert inlined_text[-11:] == "Saini Mohit", summary;
  assert (inlined_text.find("in the middle") != -1), summary;
  print("interface_1_basic_test PASSED");

def interface_1_action_test(backend_url):
  first_frame = json.loads(requests.post(backend_url+"/v1/start").text);
  button_onclick_id = tests.helpers.find_button_onclick_id(first_frame["frame"], label_string = "Click Me");
  second_frame = json.loads(requests.post(backend_url+"/v1/action",
                                json={"action_id": button_onclick_id,
                                      "client_instance_id": first_frame["client_instance_id"],
                                      "server_instance_id": first_frame["server_instance_id"]}).text);
  assert second_frame["error"]["error_code"] == "SUCCESS", second_frame;
  second_frame = second_frame["frame"];
  tests.helpers.is_valid_frame(second_frame);
  summary = tests.helpers.frame_summary(second_frame);
  assert summary.num_elements == 12;
  assert summary.elements["TEXT_INPUT"]["num_elements"] == 2;
  assert summary.elements["BUTTON"]["num_elements"] == 1;
  assert ("TEXT_AREA" not in summary.elements), summary;
  assert summary.num_onclick_id == 1;
  inlined_text = tests.helpers.inlined_text(second_frame);
  assert inlined_text[:11] == "Mohit Saini";
  assert inlined_text[-19:] == "Updated Saini Mohit";
  assert (inlined_text.find("In the Updated Middle") != -1);
  print("interface_1_action_test PASSED");

