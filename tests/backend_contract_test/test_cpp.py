import subprocess, os, signal, time, traceback
from tests.backend_contract_test import test_suit_base

def test_interface1_cpp(backend_url = None):
  pid = None
  try:
    if backend_url == None:
      os.system("g++ --std=c++14 cpp/golden_test_interface1.cpp -o /tmp/golden_test_interface1");
      pid = subprocess.Popen(["/tmp/golden_test_interface1"]).pid;
      print("Started server [Pid = " +str(pid) + "], sleeping for 5 seconds");
      time.sleep(3);
      backend_url = "http://localhost:5008"
    test_suit_base.interface_1_basic_test(backend_url);
    test_suit_base.interface_1_action_test(backend_url);
  except Exception as e:
    print(traceback.format_exc());
  finally:
    if pid != None:
      print("Killing the server [pid = " + str(pid) + "]");
      os.kill(pid, signal.SIGINT)
  print("------ test_interface1_cpp PASSED ------");

test_interface1_cpp();

