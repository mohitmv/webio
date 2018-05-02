


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



