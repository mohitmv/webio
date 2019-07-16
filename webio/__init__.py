
import flask, flask_cors, re, json, os, webio.elements

from webio.elements import ElementType, FrontEndElement, HList, VList, Button,\
													 Text

import webio.utils

from enum import IntEnum

def none_default(a, b):
  return (b if a == None else a);

def soft_update(a,b):
  for i in b:
    if i not in a:
      a[i] = b[i];
  return a;

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
    self.registered_actions = {}; # dict(action_id => action_lambda)
    self.registered_resources = {}; # element_id => Data
    self.frame = self.EvaluateFrame(frame);

  def GetUniqueIndex(self):
  	self.element_index_counter += 1;
  	return self.element_index_counter;

  def EvaluateFrame(self, frame):
    if frame.element_type == ElementType.TEXT:
      self.EvaluateText(frame);
      self.HandleOnClick(frame);
    elif frame.element_type in set([ElementType.VLIST, ElementType.HLIST]):
      self.EvaluateHListVList(frame);
      self.HandleOnClick(frame);
    elif frame.element_type == ElementType.MENU:
      self.HandleOnClickForMenu(frame);
    elif frame.element_type in set([ElementType.BUTTON,
                                    ElementType.IMAGE]):
      self.HandleOnClick(frame);
    elif frame.element_type == ElementType.DROP_DOWN:
      frame.element_id = self.GetUniqueIndex();
      self.HandleDropDown(frame);
    elif frame.element_type in set([ElementType.TEXT_INPUT,
                                    ElementType.TEXT_AREA]):
      frame.element_id = self.GetUniqueIndex();
      self.HandleOnChange(frame);
    return frame;

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

  def EvaluateHListVList(self, frame):
    width_or_height = ("width" if frame.element_type == ElementType.HLIST
                               else 'height');
    children = self.GetChildrenList(frame.children);
    if width_or_height not in frame:
      frame[width_or_height] = ["auto"]*len(children);
    for i in list(frame.keys()):
      if (i != width_or_height) and (i.split("_")[0] == width_or_height):
        frame[width_or_height][int(i.split("_")[1])-1] = frame[i];
        frame.pop(i);
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
    assert(False, "ToDo(Mohit): Implement HandleOnChange");


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

class FrameServer:
  class ErrorCodes(IntEnum):
    CLIENT_INSTANCE_TIMEOUT = 1
    INCORRECT_SERVER_INSTANCE = 2
    INTERNAL_ERROR = 3

  def __init__(self, cls, args=[], params={}):
    self.cls = cls;
    self.args = args;
    self.params = params;
    self.client_instances = dict();
    self.client_instance_id_counter = 1;
    self.server_instance_id = utils.GetEpochTimenow()*10000 + random.randint(1, 1000);

  def CreateClientInstance(self):
    instance_id = self.client_instance_id_counter;
    self.client_instance_id_counter += 1;
    self.client_instances[instance_id] = dict(
      client_instance = self.cls(*self.args, **self.params),
      instance_id = instance_id,
      current_frame = None,
      recent_active_timestamp = utils.GetEpochTimenow()
    );
    return instance_id;

  def ReloadFrame(self, instance_id):
  	instance = self.client_instances[instance_id];
    raw_rendered = instance.client_instance.Render();
    instance.current_frame = Rendering(raw_rendered);
    return instance.current_frame.Export();

  def HandleEvent(self, input_data):
  	if input_data.get("action_id") in self.current_frame.registered_actions:
  		self.website_instance.inputs = None;
  		self.current_frame.registered_actions[input_data["action_id"]]();
  		return self.ReloadFrame();

  def Run(self, port):
    app = flask.Flask("webio");
    @app.route("/", methods = ["GET"])
    @flask_cors.cross_origin(supports_credentials = True)
    def v1_start():
      instance_id = CreateInstance();
      front_end_dir = os.path.join(os.path.dirname(__file__), 'front_end')
      html_page = read_file(front_end_dir + "/index.html");
      html_page = html_page.replace(
        '<!-- {inlined_css_here:template_arg_0} -->',
        "<style>" + read_file(front_end_dir + "/css/main.css")+"</style>")
      html_page = html_page.replace('tmp_frame_6703[1]',
                                    json.dumps(self.ReloadFrame()));
      return html_page;

    @app.route("/v1/api", methods=["POST"])
    def v1_api():
      return flask.Response(
      	response = json.dumps(self.HandleEvent(flask.request.json)),
      	mimetype = "application/json"
      );
    app.run(port = port, debug = True);


def Serve(cls, args=[], params={}, port = 5018):
  return FrameServer(cls, args, params).Run(port = port);








