
import flask, flask_cors, re, json, os

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

class Element:
	def __init__(self, io_element_type, args, params):
		self.io_element_type = io_element_type;
		self.args = args;
		self.params = params;
	def __repr__(self):
		return str(("Element", self.io_element_type, self.args, self.params));

def CoreElementsConfigs():
	elements = ["image", "text", "icon", "button", "input", "menu", "vlist", "hlist"];
	default_params = dict(
		image = dict(
			src = None,	
			width = "auto",
			height = "auto", 
			opacity = 1, 
			rounded = True, 
		), 
		text = dict(
			text = "",
			onclick_id = None,
		), 
		icon = dict(
			icon = "",
			font_size = "16px",
		),
		button = dict(
			label = None, 
			theme = "default",
			icon = None, 
			onclick_id = None, 
		), 
		input = dict(
			input_type = "text",
			allow_multiple = False,
			allow_search = False, 
			label = "",
			options = [],
			default_rows = 5,
		), 
		menu = dict(
			click_actions = []
		), 
		vlist = dict(
			onclick_id = None
		),
		hlist = dict(
			onclick_id = None
		)
	);
	return dict(elements = elements, default_params = default_params);


class ElementBuilder:
	def __init__(self, io_element, *args, **default_params):
		if (type(io_element) == ElementBuilder):
			self.io_element_type = io_element.io_element_type;
			self.args = io_element.args + args;
			self.default_params = io_element.default_params;
			self.default_params.update(default_params);
		else:
			self.io_element_type = io_element;
			self.args = args;
			self.default_params = default_params;

	def __call__(self, *args, **params):
		new_params = dict(self.default_params);
		new_params.update(params);
		return Element(self.io_element_type, args, new_params);

class InputState:
	def __init__(self, input_tree):
		self.input_tree = input_tree;
		self.input_list = [];
		self.indexed_input_subtree = {};

		def flatten_input(input_tree):
			if input_tree[1] != None and (input_tree[1] not in self.indexed_input_subtree):
				self.indexed_input_subtree[input_tree[1]] = input_tree;
			if input_tree[0] == "list":
				return dict((i, flatten_input(input_tree[2][i])) for i in sorted(input_tree[2].keys())); 
			else:
				self.input_list.append(input_tree[2]);
				return input_tree[2];
		self.inputs = flatten_input(input_tree);

	def __getitem__(self, i):
		if type(i) == int:
			return self.input_list[i];
		elif type(i) == str:
			if self.indexed_input_subtree[i][0] == "list":
				return InputState(self.indexed_input_subtree[i]);
			else:
				return self.indexed_input_subtree[i][2];

	def __repr__(self):
		return str(self.inputs);

class Action:
	def __init__(self, main_lambda, *args, **params):
		self.main_lambda = main_lambda;
		self.args = args;
		self.params = params;
	def __call__(self, *x):
		return self.main_lambda(*x, *self.args, **self.params);

class Frame:
	def __init__(self, frame_lambda, *state_args, **state_params):
		self.frame_lambda = frame_lambda;
		self.state_args = state_args;
		self.state_params = state_params;
		self.default_params = CoreElementsConfigs()['default_params'];
	def get_unique_index(self):
		self.element_index_counter += 1;
		return str(self.element_index_counter);

	def run(self):
		app = flask.Flask("webio");

		@app.route("/v1/start", methods=["GET"])
		@flask_cors.cross_origin(supports_credentials=True)
		def v1_start():
			front_end_dir = os.path.join(os.path.dirname(__file__), 'front_end')
			html_page = read_file(front_end_dir + "/index.html");
			html_page = html_page.replace(
				'<!-- {inlined_css_here:template_arg_0} -->',
				"<style>" + read_file(front_end_dir + "/css/main.css")+"</style>")
			html_page = html_page.replace('tmp_frame_6703[1]',
																		json.dumps(self.reload_frame()));
			return html_page;

		@app.route("/v1/api", methods=["POST"])
		def v1_api():
			input_data = flask.request.json;
			if input_data.get("onclick_id") in self.registered_onclicks:
				frame = self.create_input_state(input_data['inputs']);
				frame.__dict__.update(self.state_params);
				frame.args = self.state_args;
				frame.params = self.state_params;
				self.registered_onclicks[input_data["onclick_id"]](frame);
			return flask.Response(response=json.dumps(self.reload_frame()), mimetype="application/json");

		app.run(port=5018, debug = True);

	def reload_frame(self):
		new_frame = self.frame_lambda(*self.state_args, **self.state_params);
		self.element_index_counter = 0;
		self.registered_onclicks = {}; # onclick_id => lambda 
		self.registered_resources = {}; # element_id => Data ( Json )
		self.solved_frame = self.solve_frame(new_frame);
		return self.solved_frame;

	def create_input_state(self, inputs):
		def input_state_creater(frame):
			if frame['type'] in ['vlist', 'hlist']:
				output = {};
				for i in range(len(frame['children'])):
					child_input = input_state_creater(frame['children'][i]);
					if child_input[0] == 'input' or child_input[2] != {}:
						output[i] = child_input;
				return ('list', frame.get("index"), output);
			elif frame['type'] == 'input':
				input_value = inputs[frame['id']];
				if frame["input_type"] in ['checkbox', 'dropdown']:
					options = self.registered_resources[frame['id']]['options'];
					if frame["allow_multiple"]:
						input_value = list(options[i-1] for i in input_value);
					else:
						input_value = options[input_value-1];
				return ('input', frame.get('index'), input_value);
			else:
				return ('list', None, {});
		return InputState(input_state_creater(self.solved_frame));




	def solve_frame(self, frame):
		if frame == None:
			return {"type": "null"};

		def get_children_list(x):
			if hasattr(x, "__iter__") and type(x) != str:
				output=[];
				for i in x:
					if type(i) == Element or i == None:
						output.append(i);
					else:
						output += get_children_list(i);
				return output;
			else:
				return [ElementBuilder("text")(str(x))]

		frame.params["type"] = frame.io_element_type;
		if frame.io_element_type == 'text':
			if len(frame.args) == 1 and type(frame.args[0]) == str:
				frame.params['text'] = frame.args[0];
				frame.params['children'] = [];
			else:
				children = get_children_list(frame.args);
				assert sum((i==None or i.io_element_type == 'text') for i in children) == len(children);
				frame.params['children'] = list(self.solve_frame(i) for i in children);
		elif frame.io_element_type in ["vlist", "hlist"]:
			width_or_height = ("width" if frame.io_element_type == 'hlist' else 'height');
			children = get_children_list(frame.args);
			if width_or_height not in frame.params:
				frame.params[width_or_height] = ["auto"]*len(children);
			for i in list(frame.params.keys()):
				if (i != width_or_height) and (i.split("_")[0] == width_or_height):
					frame.params[width_or_height][int(i.split("_")[1])-1] = frame.params[i];
					frame.params.pop(i);
			if frame.params.get("onclick") != None:
				unique_index = frame.params["id"] = self.get_unique_index();
				self.registered_onclicks[unique_index] = frame.params["onclick"];
			frame.params.update(
				children = list(self.solve_frame(i) for i in children)
			);
		else:
			main_arg = dict(
				image = "src", 
				text = "html", 
				button = "label", 
				icon = "icon", 
				input = "label", 
				menu = "icon", 
			);
			if len(frame.args) > 0:
				frame.params.update({main_arg[frame.io_element_type]: frame.args[0]});
			if frame.io_element_type == "input":
				frame.params['id'] = self.get_unique_index();
				if ("options" in frame.params):
					self.registered_resources[frame.params['id']] = {
						"io_element_type": frame.io_element_type, 
						"options": list((i[0] if type(i) == tuple else i) for i in frame.params['options'])
					};
					frame.params['options'] = list(str(i[1] if type(i) == tuple else i) for i in frame.params['options']);
					if "input_type" not in frame.params:
						frame.params['input_type'] = "dropdown";


		if frame.io_element_type in ["button", "text", "vlist", "hlist"] and (frame.params.get("onclick") != None):
				frame.params["onclick_id"] = button_index = self.get_unique_index();
				self.registered_onclicks[button_index] = frame.params["onclick"];
				frame.params.pop('onclick');
		if frame.io_element_type == "menu" and ('click_actions' in frame.params):
			menu_index = self.get_unique_index();
			for i in range(len(frame.params['click_actions'])):
				onclick_lambda = frame.params['click_actions'][i][0];
				if onclick_lambda != None:
					onclick_id = menu_index+"_"+str(i+1);
					self.registered_onclicks[onclick_id] = onclick_lambda;
					frame.params['click_actions'][i] = [onclick_id, frame.params['click_actions'][i][1]];

		soft_update(frame.params, self.default_params[frame.io_element_type]);
		if frame.io_element_type == 'input':
			if frame.params['input_type'] in ['text', 'textarea']:
				frame.params['default_value'] = frame.params.get("default_value", "");
			elif frame.params['input_type'] in ['dropdown', 'checkbox']:
				if 'default_value_index' in frame.params:
					if not frame.params['allow_multiple']:
						frame.params['default_value'] = frame.params['default_value_index']+1;
					else:
						frame.params['default_value'] = list(i+1 for i in frame.params['default_value_index']);
					frame.params.pop('default_value_index');
				elif 'default_value' in frame.params:
					if not frame.params['allow_multiple']:
						frame.params['default_value'] = list(i[0]+1 for i in enumerate(frame.params['options']) if i[1]==frame.params['default_value'])[0]; #Assert : len(list) > 0 for valid default_value.
					else:
						frame.params['default_value'] = list(i[0]+1 for i in enumerate(frame.params['options']) if i[1] in frame.params['default_value']);
				else:
					frame.params['default_value'] = ([] if frame.params['allow_multiple'] else 1);
		return frame.params;


VList = ElementBuilder("vlist", border_width = "0px");
HList = ElementBuilder("hlist", border_width="0px");
Button = ElementBuilder("button", theme = "black_in_white");
Input = ElementBuilder("input");
Menu = ElementBuilder("menu");
Text = ElementBuilder("text");
