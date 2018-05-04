def table_frame(dict_data, title=None):
	return Vlist(
		[Hlist(title)]
		 if title != None else 
		[], 
		(
			Hlist(i, dict_data[i], border_width="1px") for i in dict_data
		)
	);




state = Object(
	assignments = [
		dict(
			name = "Rohit Saini", 
			marks = [None, None, None], 
			is_closed = False, 
		), 
		dict(
			name = "Pulkit Meena", 
			marks = [None, None, None], 
			is_closed = False, 
		), 
		dict(
			name = "Mansi Verma", 
			marks = [None, None, None], 
			is_closed = False, 
		), 
		dict(
			name = "Vikash Jain", 
			marks = [None, None, None], 
			is_closed = False, 
		)
	], 
	rubrik = [
		dict(
			title = "Comments in code", 
			sections = [
				dict(
					title = "Comments on functions", 
					possible_marks = [0, 50, 100, 200], 
					hint = "Have he done this this drama.....give 50 marks.."
				), 
				dict(
					title = "Comments inside functions", 
					possible_marks = [0, 51, 101, 201], 
					hint = "Have he done this this drama.....give 5 marks.."
				), 
				dict(
					title = "Comments under functions", 
					possible_marks = [0, 56, 106, 206], 
					hint = "Have he done this this drama.....give 2 marks.."
				)
			]
		), 
		dict(
			title = "Easily understandable code", 
			sections = [
				dict(
					title = "Simple variable names", 
					possible_marks = [0, 500, 1000, 2000], 
					hint = "Have he done this this drama.....give 50 marks.."
				), 
				dict(
					title = "Should not have been used any optimasation logic", 
					possible_marks = [0, 510, 1010, 2010], 
					hint = "Have he done this this drama.....give 5 marks.."
				), 
				dict(
					title = "Should not use lambda functions", 
					possible_marks = [0, 560, 1060, 2060], 
					hint = "Have he done this this drama.....give 2 marks.."
				)
			]
		), 
		dict(
			title = "Assignment Understanding", 
			sections = [
				dict(
					title = "Isme to sbke full de dena... vrna bche royenge", 
					possible_marks = [0, 5000, 10000, 20000], 
					hint = "Have he done this this drama.....give 50 marks.."
				)
			]
		)
	], 
	page = "index", 
	args = {}
);

def nav(state, page, args={}):
	state.page = page;
	state.args = args;


def nav1(state, page=None, args={}):
	state.page = none_default(page, state.page);
	state.args.update(args);


def list_index_value(l):
	return list((i, l[i]) for i in range(len(l)));


def save_marks_feedback(fm):
	state = fm.params['state'];
	state.assignments[state.args['index']]['marks'][state.args['section']] = list((fm['rubric_'+str(i)]['comment'], fm['rubric_'+str(i)]['marks']) for i in range(len(state.rubrik[state.args['section']])));


fm = Frame(lambda state: 
	dict(index = lambda: Vlist(
			Hlist(
				Text("Welcome Nikhil Kumar"), 
				None, 
				table_frame({
					"Total": len(state.assignments), 
					"Closed": sum(i["is_closed"] for i in state.assignments), 
					"Opened": sum(not(i["is_closed"]) for i in state.assignments), 
				}, "Overall Statistics")
			), 
			Vlist(
				Text("<span style='font-size: 18px;' >Assignment Grading Queue</span>"), 
				Hlist(
					(
						Button(
							i[0], 
							onclick = Bind(
								lambda fm, i: 
								nav(state, 
									"list_assignment", 
									{"type": i}
								), i
							)
						) for i in [("All", "all"), ("Open", "open"), ("Closed", "closed")]
					), 
					None, 
					width_4 = "70%"
				)
			), 
		),
		list_assignment = lambda: Vlist(
			Text("<span style='font-size: 18px;' >Assignment Grading Queue</span>" + " - "+state.page), 
			Hlist("<b>Name</b>", "<b>Grade</b>"), 
			(
				Hlist(
					i['name'], 
					"---", 
					onclick = Bind(lambda fm,j: nav(state, "grade", {"index": j, "section": 0, "type": state.args['type']}), j)
				) 
				for j, i in list_index_value(state.assignments) if 
				(
					state.args['type'] == "all"
					 or 
					(i['is_closed'] == (state.args['type']=="closed"))
				)
			)

		), 
		grade = lambda: Vlist(
			Hlist(
				Button("Back", onclick = lambda fm: 
					nav(
						state, 
						"list_assignment", 
						{"type": state.args['type']}
					)
				), 
				"Name = " + state.assignments[state.args['index']]['name']
			), 
			Hlist(
				"Grading Rubric"
			), 
			Hlist(
				Vlist(
					(
						Hlist(
							i['title'],
							"--/--", 
							width_2 = "300px", 
							onclick = Bind(lambda fm, j: nav1(state, args={"section": j}), j) 
						) for j, i in list_index_value(state.rubrik)
					), 
					border_width = "1px"
				), 
				Vlist(
					(Vlist(
						Hlist(
							i['title'], 
							Hlist(
								"Marks", 
								Input("", options = i['possible_marks'], index="marks", **({} if (state.assignments[state.args['index']]['marks'][state.args['section']] == None) else {"default_value": int(state.assignments[state.args['index']]['marks'][state.args['section']][][1])})), 
								i['possible_marks'][-1]
							), 
							width_2 = "200px"
						), 
						i['hint'], 
						Input("Feedback", input_type="textarea", index="comment"), 
						index = "rubric_"+str(j)
					) for j,i in list_index_value(state.rubrik[state.args['section']]['sections'])), 
					Button("Save", onclick = save_marks_feedback ), 
					border_width="1px"
				), 
				width_1 = "40%"
			)
		)
	)[state.page]()
, state=state);


fm.run();










#---------------------------------------------------------------------------------













# fm1.run();



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







fm = Frame(lambda:
	Vlist(
		Hlist(
			Vlist1(
				Input("Name ?"), 
				Input("Email ID ?"), 
				Input("Password ?"), 
				Input("Type of profile", options=["Teacher", "Student"]), 
			), 
			Button("Saini889990000"), 
			Button("Saini Ji"), 
		), 
		Vlist(
			Button1("Mohits"), 
			Button("iiiooo")
		)
	)
);

fm1 = Frame(lambda:
	Vlist(
		Button1("Mohits", onclick=button_onclick), 
		Button("iiiooo", onclick=lambda fm: print(fm)), 
		Input("Name", default_value="Jai Mata Di", input_type="textarea", index="mohitS"), 
		Menu("thumb_up", click_actions=[(lambda fm: print(888, fm), "Saini"), (None, "Mohit")]), 
		Hlist(
			Input("Are you ok ?", 
				options=[([33, 44], "No"), ([3434, 343434], "Yes"), ([323232323, 333], "Han Ji")], 
				input_type = "checkbox",
				default_value = 3
			), 
			None, 
			width_1 = "30%"
		), 
	)
);



i = InputState(
	("list", None, {
		0: ("list", None, {
			0: ("input", "name", "Mohit"), 
			1: ("input", None, "Vikash Ji")
		}), 
		2: ("list", None, {
			4: ("input", "saini", [33, 44, 55, 66])
		})
	})
);




# print(fm);


# a = fm.frame_lambda();

# # print(a);

# self = fm;

# self.element_index_counter = 0;
# self.registered_onclicks = {};
# self.registered_resources = {};


# b = fm.solve_frame(a);

# print(b);




	# align = left|right|middle, 
	# valign = top|bottom|middle, 
	# padding = Size_Unit_Numeric , 
	# bgcolor = Colors, 
	# border_width = Size_Unit_Numeric, 
	# border_color = Colors, 
	# *children = List-of-Io



# py2web = Py2web()





	def element_constructor(element, activate_validity_checker=False):
		height_or_width = ('height' if element == 'vlist' else 'width');
		default_params = Object(
			image = Object(
				width = "auto", 
				height = "auto", 
				opacity = 1, 
				rounded = True, 
			), 
			text = Object(
				onclick = None, 
			), 
			icon = Object(
				font_size = "16px", 
			), 
			button = Object(
				label = None, 
				theme = "default", 
				icon = None, 
				onclick = None, 
			), 
			input = Object(
				input_type = "text", 
				allow_multiple = False, 
				allow_search = False, 
				label = "", 
				options = [], 
			)
		);
		def hv_list_constructor_1(*children, **params): #Assert: valid inputs.
			output = Object(frontend = {"type": element, "children": children}, backend = {});
			basic_attrs = set(["align", "valign", "padding", "bgcolor", "border_width", "border_color"]);
			size_array = params[height_or_width] if (height_or_width in params) else ["auto"]*len(children);
			for i in params:
				underscore_split = i.split("_", 1);
				if(underscore_split[0] == height_or_width):
					size_array[int(underscore_split[1])-1] = params[i];
				elif i in basic_attrs:
					output.frontend[i] = params[i];
			return output;

		def hv_list_constructor_2(*children, **params): # Not completed yet.
			is_valid_input = True;
			basic_attrs = set(["align", "valign", "padding", "bgcolor", "border_width", "border_color"]);
			size_array = params[height_or_width] if (height_or_width in params) else ["auto"]*len(children);
			if len(size_array) != len(children):
				is_valid_input = False;
			for i in params:
				underscore_split = i.split("_", 1);
				if(underscore_split[0] == height_or_width):
					if(underscore_split[1].isdigit() and (1 <= int(underscore_split[1]) <= len(children))):
						size_array[int(underscore_split[1])-1] = params[i];
					else:
						is_valid_input = False;
						break;
			#Some more to do.... Stopped this part for a while...

		def icon_constructor_1(icon, **params):
			attrs = default_params[element];
			attrs

		def atomic_io_constructor_1(*children, **params): #Assert: valid input.
			output = Object(frontend = {"type": element}, backend = {});
			output.update(default_params[element]);
			output.update(params);


		def atomic_io_constructor_2(*children, **params): #Yet to design.
			pass


			pass



