import subprocess, os, signal, time, traceback
from tests.backend_contract_test import test_suit_base


def test_interface_1_cpp():
  backend_url = "http://localhost:5008"
  test_suit_base.interface_1_basic_test(backend_url);
  # test_suit_base.interface_1_action_test(backend_url);

test_interface_1_cpp();
