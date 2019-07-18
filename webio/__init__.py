import flask, flask_cors, re, json, os, webio.elements, random, threading, time

from webio.elements import ElementType, FrontEndElement, Div, HDiv, Button
from webio.elements import Text, TextArea, Image, DropDown, CheckBoxList
from webio.elements import CheckBox, Toggle, Menu, Icon, TitleText, TextInput

import webio.utils, traceback

from enum import IntEnum

def none_default(a, b):
  return (b if a == None else a);

def read_file(fn):
  fd = open(fn);
  output = fd.read();
  fd.close();
  return output;

class Object(dict):
  def __init__(self, initial_value={}, **kwargs):
    self.__dict__ = self;
    dict.__init__(self, initial_value, **kwargs);

class Action:
  def __init__(self, main_lambda, *args, **params):
    self.main_lambda = main_lambda;
    self.args = args;
    self.params = params;
  def __call__(self, *x):
    return self.main_lambda(*x, *self.args, **self.params);

class Rendering:
  def __init__(self, frame):
    self.element_index_counter = 0;
    # dict(action_id => action_lambda)
    self.registered_actions = {};
    # dict(element_id => Data)
    # 1. In case of DropDown[allow_multiple], CheckBoxList(allow_multiple)
    #     we store the list of internal-options.
    self.registered_resources = {};
    self.input_acceser = None;
    self.frame = self.EvaluateFrame(frame);

  def GetUniqueIndex(self):
    self.element_index_counter += 1;
    return self.element_index_counter;

  def EvaluateFrame(self, frame):
    if frame.element_type == ElementType.TEXT:
      self.EvaluateText(frame);
      self.HandleOnClick(frame);
    elif frame.element_type in set([ElementType.DIV, ElementType.HORIZONTAL_DIV]):
      self.EvaluateDivHDiv(frame);
      self.HandleOnClick(frame);
    elif frame.element_type == ElementType.MENU:
      self.HandleOnClickForMenu(frame);
    elif frame.element_type in set([ElementType.BUTTON,
                                    ElementType.IMAGE]):
      self.HandleOnClick(frame);
    elif frame.element_type in set([ElementType.DROP_DOWN,
                                    ElementType.CHECK_BOX_LIST]):
      frame.element_id = self.GetUniqueIndex();
      self.HandleDropDown(frame);
      self.HandleOnChange(frame);
    elif frame.element_type in set([ElementType.TEXT_INPUT,
                                    ElementType.TEXT_AREA]):
      frame.element_id = self.GetUniqueIndex();
      self.HandleOnChange(frame);
    self.input_acceser = self.CreateInputAccesser(frame);
    return frame;

  def CreateInputAccesser(self, frame):
    output = [];
    def CreateInputAccesserHelper(frame, target):
      if (frame.element_type.IsInputElement()) and ("index" in frame):
          target.append((frame.index, frame.element_id));
      if frame.element_type.HaveChildren():
        if ("index" in frame):
          target.append((frame.index, []));
          new_target = target[-1][1];
        else:
          new_target = target;
        for i in frame.children:
          CreateInputAccesserHelper(i, new_target);
    CreateInputAccesserHelper(frame, output);
    return output;

  def GetChildrenList(self, x):
    if hasattr(x, "__iter__") and type(x) != str:
      output = [];
      for i in x:
        if i == None:
          continue;
        elif isinstance(i, FrontEndElement):
          output.append(i);
        else:
          output += self.GetChildrenList(i);
      return output;
    else:
      return [elements.Text(str(x))];

  def EvaluateDivHDiv(self, frame):
    children = self.GetChildrenList(frame.children);
    frame.update(
      children = list(self.EvaluateFrame(i) for i in children)
    );
    return frame;

  def EvaluateText(self, frame):
    if len(frame.children) == 1 and type(frame.children[0]) == str:
      frame.text_string = frame.children[0];
      frame.children = [];
    else:
      children = self.GetChildrenList(frame.children);
      assert (sum(((i.element_type == ElementType.TEXT) for i in children))
                 == len(children));
      frame.children = list(self.EvaluateFrame(i) for i in children);
    return frame;

  def HandleOnClickForMenu(self, frame):
    for i in range(len(frame.click_actions)):
      onclick_lambda = frame.click_actions[i][0];
      if onclick_lambda != None:
        onclick_id = self.GetUniqueIndex();
        self.registered_actions[onclick_id] = onclick_lambda;
        frame.click_actions[i] = [onclick_id, frame.click_actions[i][1]];
    return frame;

  def HandleOnChange(self, frame):
    if (frame.get("onchange") != None):
      frame.onchange_id = frame.element_id;
      self.registered_actions[frame.onchange_id] = frame.onchange;
    return frame;

  def HandleOnClick(self, frame):
    if (frame.get("onclick") != None):
      frame.element_id = frame.onclick_id = self.GetUniqueIndex();
      self.registered_actions[frame.onclick_id] = frame.onclick;
    return frame;

  def HandleDropDown():
    option_values = list((i[0] if type(i) == tuple else i) for i in frame.options)
    self.registered_resources[frame.unique_id] = dict(
      options = option_values
    );
    frame.options = list((index, str(option[1] if type(option) == tuple else option))
                            for index, option in enumerate(frame.options));
    if frame.allow_multiple:
      frame.value = none_default(frame.value, []);
      for index, value in enumerate(option_values):
        if (value in frame.value):
          frame.value_integer_list.append(index);
    else:
      for index, value in enumerate(option_values):
        if (value == frame.value):
          frame.value_integer = index;
    return frame;

class Configs:
  client_instance_timeout = 3600 # seconds.
  client_instance_cleaner_frequency = 60 # seconds

class ErrorCodes(IntEnum):
  CLIENT_INSTANCE_TIMEOUT = 1
  INCORRECT_SERVER_INSTANCE = 2
  INTERNAL_ERROR = 3
  SUCCESS = 4
  INVALID_ACTION = 5

class FrameServer:
  def __init__(self, cls, args=[], params={}):
    self.cls = cls;
    self.args = args;
    self.params = params;
    self.client_instances = dict();
    self.client_instance_id_counter = 1;
    self.server_instance_id = utils.GetEpochTimenow()*10000 + random.randint(1, 1000);
    self.lock = threading.Lock();

  def CreateClientInstance(self):
    instance_id = self.client_instance_id_counter;
    self.client_instance_id_counter += 1;
    self.client_instances[instance_id] = Object(
      client_instance = self.cls(*self.args, **self.params),
      instance_id = instance_id,
      current_frame = None,
      recent_active_timestamp = None,
      request_counter = 0
    );
    return instance_id;

  def ReloadFrame(self, instance_id):
    instance = self.client_instances[instance_id];
    raw_rendered = instance.client_instance.Render();
    instance.current_frame = Rendering(raw_rendered);
    instance.recent_active_timestamp = utils.GetEpochTimenow();
    return instance.current_frame.frame.Export();

  def HandleFirstTimeLoad(self):
    self.lock.acquire();
    client_instance_id = self.CreateClientInstance();
    output = Object(
      error = Object(error_code = ErrorCodes.SUCCESS.__str__()),
      data = self.ReloadFrame(client_instance_id),
      client_instance_id = client_instance_id,
      server_instance_id = self.server_instance_id,
    );
    self.lock.release();
    return output;

  def PopulateInputs(self, instance_id, inputs):
    output = Object();
    output_findall = Object();
    instance = self.client_instances[instance_id];
    def PopulateInputsHelper(node):
      if (type(node[1]) != list):
        output_findall[node[0]].append(inputs[node[1]]);
        return {node[0], inputs[node[1]]};
      else:
        output = {};
        for i in node[1]:
          output.update({node[0]: PopulateInputsHelper(i)});
        return output;
    return PopulateInputsHelper(instance.current_frame.input_acceser);

  def HandleActionEvent(self, input_data):
    self.lock.acquire();
    output = Object(error = Object(error_code = ErrorCodes.SUCCESS.__str__()));
    instance_id = input_data["client_instance_id"];
    if instance_id not in self.client_instances:
      output.error.error_code = ErrorCodes.CLIENT_INSTANCE_TIMEOUT.__str__();
    elif input_data["server_instance_id"] != self.server_instance_id:
      output.error.error_code = ErrorCodes.INCORRECT_SERVER_INSTANCE.__str__();
    else:
      instance = self.client_instances[instance_id];
      current_frame = instance.current_frame;
      if input_data.get("action_id") not in current_frame.registered_actions:
        output.error.error_code = ErrorCodes.INVALID_ACTION.__str__();
      else:
        instance.client_instance.inputs = self.PrepareInputs(input_data['inputs']);
        try:
          current_frame.registered_actions[input_data["action_id"]]();
          output.error.error_code = ErrorCodes.SUCCESS.__str__();
          output.data = self.ReloadFrame(instance_id);
        except Exception as e:
          error_trace = traceback.format_exc();
          print(error_trace);
          output.error.error_code = ErrorCodes.INTERNAL_ERROR.__str__();
    self.lock.release();
    return output;

  def InstanceCleaner(self):
    print("InstanceCleaner thread started");
    while True:
      time.sleep(Configs.client_instance_cleaner_frequency);
      self.lock.acquire();
      old_client_instances = [];
      for i,v in self.client_instances.items():
        if (utils.GetEpochTimenow() >
              Configs.client_instance_timeout + v.recent_active_timestamp):
          old_client_instances.append(i);
      list(self.client_instances.pop(i) for i in old_client_instances);
      print("[cleanup] deleted client_instances ", old_client_instances);
      self.lock.release();

  def Run(self, port):
    app = flask.Flask("webio");
    @app.route("/", methods = ["GET"])
    @flask_cors.cross_origin(supports_credentials = True)
    def v1_start():
      front_end_dir = os.path.join(os.path.dirname(__file__), 'front_end')
      html_page = read_file(front_end_dir + "/index.html");
      html_page = html_page.replace(
        '<!-- {inlined_css_here:template_arg_0} -->',
        "<style>" + read_file(front_end_dir + "/css/main.css")+"</style>")
      html_page = html_page.replace('tmp_frame_6703[1]',
                                    json.dumps(self.HandleFirstTimeLoad()));
      return html_page;

    @app.route("/v1/api", methods=["POST"])
    def v1_api():
      return flask.Response(
        response = json.dumps(self.HandleActionEvent(flask.request.json)),
        mimetype = "application/json"
      );
    cleaner_thread = threading.Thread(name = "cleaner_thread",
                                      target = self.InstanceCleaner);
    cleaner_thread.start();
    app.run(port = port, debug = False);
    cleaner_thread.join();



def Serve(cls, args=[], params={}, port = 5018):
  return FrameServer(cls, args, params).Run(port = port);



