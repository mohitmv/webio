import requests, commons, subprocess, json, tests.utils

  # os.system()
  # pid = subprocess.Popen(["python36", "/tmp/grace.py"]).pid;
def test_if1_basic_interface(backend_url):
  first_frame = json.loads(requests.get(backend_url+"/v1/start").text);
  tests.utils.is_valid_frame(first_frame);
  summary = tests.utils.frame_summary(first_frame);
  assert summary["num_elements"] = 5;
  assert summary["elements"]["TEXT_INPUT"]["num_elements"] = 2;
  assert summary["elements"]["BUTTON"]["num_elements"] = 1;
  assert summary["elements"]["TEXT_AREA"]["num_elements"] = 0;
  assert summary["num_onclick_id"] = 2;
  assert summary["first_text"] = "Mohit Saini";
  assert summary["last_text"] = "Saini Mohit";
  assert summary[""] = "Saini Mohit";



  pass