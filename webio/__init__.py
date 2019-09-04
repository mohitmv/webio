import flask, flask_cors, re, json, os, webio.elements, random, threading, time

from webio.elements import ElementType, FrontEndElement, Div, HDiv, Button
from webio.elements import Text, TextArea, Image, DropDown, CheckBoxList
from webio.elements import CheckBox, Toggle, Menu, Icon, TitleText, TextInput
from webio.elements import HTabs, Tab, VSpace, Card, VDiv, InlinedDiv
from webio.elements import IconButton

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
  def __init__(self, initial_value = {}, **kwargs):
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
    frame.element_id = self.GetUniqueIndex();
    if frame.element_type == ElementType.TEXT:
      self.EvaluateText(frame);
      self.HandleOnClick(frame);
    elif frame.element_type.IsDiv():
      self.EvaluateDivTab(frame);
      self.HandleOnClick(frame);
    elif frame.element_type in set([ElementType.HORIZONTAL_TABS]):
      self.EvaluateDivTab(frame);
    elif frame.element_type == ElementType.MENU:
      self.HandleOnClickForMenu(frame);
    elif frame.element_type in set([ElementType.BUTTON,
                                    ElementType.ICON_BUTTON,
                                    ElementType.IMAGE,
                                    ElementType.TAB]):
      self.HandleOnClick(frame);
    elif frame.element_type in set([ElementType.DROP_DOWN,
                                    ElementType.CHECK_BOX_LIST]):
      self.HandleDropDown(frame);
      self.HandleOnChange(frame);
    elif frame.element_type in set([ElementType.TEXT_INPUT,
                                    ElementType.TEXT_AREA]):
      self.HandleOnChange(frame);
    self.input_acceser = self.CreateInputAccesser(frame);
    return frame;

  def CreateInputAccesser(self, frame):
    output = [];
    def CreateInputAccesserHelper(frame, target):
      if (frame.element_type.IsInputElement()) and ("id" in frame):
          target.append((frame.id, frame.element_id));
      if frame.element_type.HaveChildren():
        if ("id" in frame):
          target.append((frame.id, []));
          new_target = target[-1][1];
        else:
          new_target = target;
        for i in frame.children:
          CreateInputAccesserHelper(i, new_target);
    CreateInputAccesserHelper(frame, output);
    return output;

  def CreateInputValue(self, element_id, front_end_value):
    if (element_id in self.registered_resources):
      element = self.registered_resources[element_id].element;
      option = self.registered_resources[element_id].options;
      if (element.element_type in set([ElementType.DROP_DOWN,
                                       ElementType.CHECK_BOX_LIST])):
        if element.allow_multiple:
          front_end_value = set(front_end_value);
          return list(v for i,v in enumurate(options) if i in front_end_value);
        else:
          return options[front_end_value];
    return front_end_value;

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
      return [elements.Text(str(x).replace("\n", "<br>"))];

  def EvaluateDivTab(self, frame):
    children = self.GetChildrenList(frame.children);
    frame.update(
      children = list(self.EvaluateFrame(i) for i in children)
    );
    return frame;

  def EvaluateText(self, frame):
    if len(frame.children) == 1 and type(frame.children[0]) == str:
      frame.text_string = frame.children[0].replace("\n", "<br>");
      frame.children = [];
    else:
      children = self.GetChildrenList(frame.children);
      assert (sum(((i.element_type == ElementType.TEXT) for i in children))
                 == len(children));
      frame.children = list(self.EvaluateFrame(i) for i in children);
    return frame;

  def HandleOnClickForMenu(self, frame):
    for i in range(len(frame.options)):
      onclick_lambda = frame.options[i][1];
      if onclick_lambda != None:
        onclick_id = self.GetUniqueIndex();
        self.registered_actions[onclick_id] = onclick_lambda;
        frame.options[i] = [frame.options[i][0], onclick_id];
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

  def HandleDropDown(self, frame):
    option_values = list((i[0] if type(i) == tuple else i) for i in frame.options)
    self.registered_resources[frame.element_id] = dict(
      element = frame,
      options = option_values
    );
    frame.options = list((str(option[1] if type(option) == tuple else option))
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
  INCOMPLETE_INPUT_VALUES = 6
  def String(self):
    return self.__str__().split(".")[-1];

class FrameServer:
  def __init__(self, cls, args=[], params={}):
    self.cls = cls;
    self.args = args;
    self.params = params;
    self.client_instances = dict();
    self.client_instance_id_counter = 1;
    self.server_instance_id = utils.GetEpochTimenow()*10000 + random.randint(1, 1000);
    self.last_instance_clean_timestamp = None;

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
    client_instance_id = self.CreateClientInstance();
    output = Object(
      error = Object(error_code = ErrorCodes.SUCCESS.String()),
      frame = self.ReloadFrame(client_instance_id),
      client_instance_id = client_instance_id,
      server_instance_id = self.server_instance_id,
    );
    return output;

  def PopulateInputs(self, instance_id, inputs):
    inputs = dict((int(k), v) for k,v in inputs.items());
    output_findall = Object();
    instance = self.client_instances[instance_id];
    def PopulateInputsHelper(nodes):
      output = Object();
      for node in nodes:
        if (type(node[1]) != list):
          input_value = instance.current_frame.CreateInputValue(node[1],
                                                                inputs[node[1]]);
          if node[0] not in output_findall:
            output_findall[node[0]] = [];
          output_findall[node[0]].append(input_value);
          output.update({node[0]: input_value});
        else:
          output.update({node[0]: PopulateInputsHelper(node[1])});
      return output;
    output = PopulateInputsHelper(instance.current_frame.input_acceser);
    instance.client_instance.inputs = output;
    instance.client_instance.all_inputs = output_findall;

  def HandleActionEvent(self, input_data):
    output = Object(error = Object(error_code = ErrorCodes.SUCCESS.String()));
    instance_id = input_data["client_instance_id"];
    if input_data["server_instance_id"] != self.server_instance_id:
      output.error.error_code = ErrorCodes.INCORRECT_SERVER_INSTANCE.String();
    elif instance_id not in self.client_instances:
      output.error.error_code = ErrorCodes.CLIENT_INSTANCE_TIMEOUT.String();
    else:
      instance = self.client_instances[instance_id];
      current_frame = instance.current_frame;
      if input_data.get("action_id") not in current_frame.registered_actions:
        output.error.error_code = ErrorCodes.INVALID_ACTION.String();
      else:
        try:
          self.PopulateInputs(instance_id, input_data.get('inputs', {}));
          current_frame.registered_actions[input_data["action_id"]]();
          output.error.error_code = ErrorCodes.SUCCESS.String();
          output.frame = self.ReloadFrame(instance_id);
        except Exception as e:
          error_trace = traceback.format_exc();
          print(error_trace);
          output.error.error_code = ErrorCodes.INTERNAL_ERROR.String();
    return output;

  def CleanupOldInstancesIfRequired(self):
    timenow = utils.GetEpochTimenow();
    if (timenow > self.last_instance_clean_timestamp
                  + Configs.client_instance_cleaner_frequency):
      old_client_instances = [];
      for i,v in self.client_instances.items():
        if (utils.GetEpochTimenow() >
              Configs.client_instance_timeout + v.recent_active_timestamp):
          old_client_instances.append(i);
      list(self.client_instances.pop(i) for i in old_client_instances);
      print("[cleanup] deleted client_instances ", old_client_instances);
      self.last_instance_clean_timestamp = timenow;

  def Run(self, port):
    self.last_instance_clean_timestamp = utils.GetEpochTimenow();
    app = flask.Flask("webio");
    @app.route("/", methods = ["GET"])
    @flask_cors.cross_origin(supports_credentials = True)
    def v1_start():
      self.CleanupOldInstancesIfRequired();
      front_end_dir = os.path.join(os.path.dirname(__file__), 'front_end')
      html_page = read_file(front_end_dir + "/index.html");
      html_page = html_page.replace(
        '<!-- {inlined_css_here:template_arg_0} -->',
        "<style>" + read_file(front_end_dir + "/css/main.css")+"</style>")
      html_page = html_page.replace('tmp_frame_6703[1]',
                                    json.dumps(self.HandleFirstTimeLoad()));
      return html_page;

    @app.route("/v1/start", methods=["POST"])
    def v1_start_json():
      return flask.Response(
        response = json.dumps(self.HandleFirstTimeLoad()),
        mimetype = "application/json"
      );

    @app.route("/v1/action", methods=["POST"])
    def v1_action():
      return flask.Response(
        response = json.dumps(self.HandleActionEvent(flask.request.json)),
        mimetype = "application/json"
      );

    app.run(port = port, debug = True);

def Serve(cls, args=[], params={}, port = 5018):
  return FrameServer(cls, args, params).Run(port = port);



