
import flask, flask_cors

import re, json


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

def list_iter(l):
	return ((i, l[i]) for i in range(len(l)))


class Object(dict):
	def __init__(self, initial_value={}, **kwargs):
		self.__dict__ = self;
		dict.__init__(self, initial_value, **kwargs);



class ElementState:
	def __init__(self, io_element_type, args, params):
		self.io_element_type = io_element_type;
		self.args = args;
		self.params = params;

	def __repr__(self):
		return str(("ElementState", self.io_element_type, self.args, self.params));


class Element:
	def __init__(self, io_element_type, **default_params):
		self.io_element_type = io_element_type;
		self.default_params = default_params;

	def set_default_params(self, **new_default_params):
		new_element = Element(self.io_element_type, **self.default_params);
		new_element.default_params.update(new_default_params);
		return new_element;

	def __call__(self, *args, **params):
		params1 = dict(self.default_params);
		params1.update(params);
		return ElementState(self.io_element_type, args, params1);



class Py2web:
	def __init__(self):
		pass


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


class Onclick:
	def __init__(self, click_lambda, *args, **params):
		self.click_lambda = click_lambda;
		self.args = args;
		self.params = params;

	def __call__(self, fm):
		return self.click_lambda(fm, *self.args, **self.params);



class Frame:
	def __init__(self, frame_lambda, *state_args, **state_params):
		self.frame_lambda = frame_lambda;
		self.state_args = state_args;
		self.state_params = state_params;
		self.default_params = dict(
			image = dict(
				width = "auto", 
				height = "auto", 
				opacity = 1, 
				rounded = True, 
			), 
			text = dict(
				onclick_id = None, 
			), 
			icon = dict(
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
			vlist = {},
			hlist = {}
		);

	def get_unique_index(self):
		self.element_index_counter += 1;
		return str(self.element_index_counter);


	def run(self):
		app = flask.Flask("py2web");

		@app.route("/v1/start", methods=["GET"])
		@flask_cors.cross_origin(supports_credentials=True)
		def v1_start():
			html_page = read_file("index.html");
			html_page = html_page.replace('<link rel="stylesheet" type="text/css" href="css/main.css?reload=', 'link_style_72378');
			html_page = re.sub('link_style_72378[0-9]+\">', '<style>'+read_file("css/main.css")+'</style>', html_page);
			html_page = html_page.replace('tmp_frame_6703[1]', json.dumps(self.reload_frame()));
			return html_page;#This part will be replaced by string--- Content of index.html.

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



		pass

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
					options = list((i[0] if type(i) == tuple else i) for i in self.registered_resources[frame['id']]);
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
					if type(i) == ElementState or i == None:
						output.append(i);
					else:
						output += get_children_list(i);
				return output;
			else:
				return [Element("text")(str(x))]

		frame.params["type"] = frame.io_element_type;
		if frame.io_element_type in ["vlist", "hlist"]:
			width_or_height = ("width" if frame.io_element_type == 'hlist' else 'height');
			children = get_children_list(frame.args);
			if width_or_height not in frame.params:
				frame.params[width_or_height] = ["auto"]*len(children);
			for i in list(frame.params.keys()):
				if (i != width_or_height) and (i.split("_")[0] == width_or_height):
					frame.params[width_or_height][int(i.split("_")[1])-1] = frame.params[i];
					frame.params.pop(i);
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
					self.registered_resources[frame.params['id']] = frame.params['options'];
					frame.params['options'] = list((i[1] if type(i) == tuple else i) for i in frame.params['options']);
					if "input_type" not in frame.params:
						frame.params['input_type'] = "dropdown";


			if frame.io_element_type in ["button", "text"] and (frame.params.get("onclick") != None):
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
		if frame.io_element_type == 'input' and ('default_value' not in frame.params):
			default_value = (
				"" 
				 if frame.params['input_type'] in ["text", "textarea"] else 
				(
					([]
					 if frame.params['allow_multiple'] else 
					1
					)
					 if frame.params['input_type'] in ['dropdown', 'checkbox'] else
					None
				)
			);
			frame.params['default_value'] = default_value;

		return frame.params;








Vlist = Element("vlist", border_width="0px", padding="5px");
Vlist1 = Vlist.set_default_params(border_width="0px");
Hlist = Element("hlist", border_width="0px", padding="5px");
Button = Element("button");
Input = Element("input");
Menu = Element("menu");
Text = Element("text");

Button1 = Button.set_default_params(theme="black_in_white");




state = Object(posts = []);
# state.posts.append(dict(title="11", body="876", module="88899"));

def delete_from_list(l, index):
	print(l, index);
	return l[:index]+l[index+1:];




onclicks = Object(



);


def inc_likes(fm, p):
	p['likes'] += 1;

def dec_likes(fm, p):
	p['likes'] -= 1;

def comment(fm, i, p):
	p['comments'].append(dict(content = fm['post_'+str(i)]['comment']));



fm1 = Frame(lambda state:
	Hlist(
		Vlist(
			Text("Ask your question"), 
			Input("Title"), 
			Input("Detailed Question", input_type="textarea"), 
			Hlist(
				Input("Module", options=["Module1", "Module2"]), 
				Button("Submit", onclick=lambda fm: 
					fm.state.posts.append(
						dict(title=fm[0], body=fm[1], module=fm[2], likes=0, comments=[])
					)
				)
			)
		), 
		Vlist(
			[
				Vlist(
					Hlist(
						"<b>"+p['title']+"</b>", 
						Menu("keyboard_arrow_down", 
							click_actions=[
								( Onclick(
									lambda fm, i: 
										fm.state.update(
											posts=delete_from_list(fm.state.posts, i)
										), i
									), "Remove"
								), 
								(None, "Report Spam To this")
							]
						), 
						width_2 = "30px"
					), 
					Text(
						"<br>Body = {body}<br>------<br>Module: {module}".format(**p)
					), 
					Hlist(
						Button(icon="thumb_up", onclick=Onclick(inc_likes , p)), 
						Button(icon="thumb_down", onclick=Onclick(dec_likes , p)), 
						Text(p['likes']), 
						None, 
						width_3 = "60%"
					), 
					Hlist(
						Input("Comment", index="comment", input_type="textarea", default_rows=3), 
						Button("Comment", onclick=Onclick(comment, i, p)), 
						width_2 = "20%"
					), 
					Vlist((i['content'] for i in p['comments']), border_width="1px"), 
					index = "post_"+str(i)
				) for i,p in list_iter(state.posts)
			], index = "abc", border_width = "1px"
		), 
		None, 
		width_3 = "30px"
	), 
	state = state
);



fm1.run();



# def get_children_list(x):
# 	output=[];
# 	for i in x:
# 		if type(i) == ElementState or i == None:
# 			output.append(i);
# 		else:
# 			output += get_children_list(i);
# 	return output;

# fm1 = Frame(lambda: Vlist(
# 	list(
# 		Vlist(
# 			i['title'], i['body'], "Module = "+i['module']
# 			, border="1px"
# 		) for i in posts
# 	), index = "abc"
# ));

# fm1.element_index_counter = 1;
# posts.append(dict(title="11", body="876", module="88899"));


# a = fm1.frame_lambda()




# print(a);
# fm1.solve_frame(a);




# print(get_children_list((Vlist(list(Button("Mohit") for i in range(2)), index="abc"), )));




