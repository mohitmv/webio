	var elms = new (function(){
		this.text = function(a) {
			return {type: "text", id: "5_227", html: a, onclick: null};
		}
	})();



	var Button = {
		"type": "button", 
		"id": "6_125", // that means 6th frame re-loading, and 125th button.
		// "label": "Submit App", 
		"label": null, 
		"theme": "default", 
		"icon": "more_vert", 
		// "icon": null, 
		"onclick": "api_call", 
	}

	var Image = {
		type: "image", 
		id: "5_223", 
		src: "images/saini.jpg", 
		width: "auto", 
		height: "auto", 
		opacity: 0.6945678, 
		rounded: true
	};

	var Text = {
		type: "text", 
		html: "<a href='Saini Ji' >Mohit Saini</a> Jai Ho Dada ki.. <span style='font-size: 30px; color: blue;' >Jai Mata Di</span> <br> New tab..... Wow... Acha hun...", 
		onclick: null
	};

	var Icon = {
		type: "icon", 
		icon: "arrow_forward", 
		font_size: "90px", 

	}


	var text_input = {
		type: "input", 
		input_type: "text", 
		label: "What is your password?", 
		default_value: "Jai Mata Di"
	}
	var textarea_input = {
		type: "input", 
		input_type: "textarea", 
		label: "What is your password? Ji", 
		default_rows: 4, 
		default_value: "Jai Mata Di"
	}
	var dropdown_input = {
		id: "125_87", 
		type: "input", 
		input_type: "checkbox", 
		label: "", 
		options: ["Agree to terms and conditions", "sdsdd", "sdhskshk shd s ds", "sj hskdshdks hd kds kdh"], 
		default_value: 2, 
		allow_multiple: true
	}

	var Menu = {
		type: "menu", 
		icon: "menu", 
		click_actions: [["null", "Report Abuse"], [null, "TA Validated"]]
	}

	var Hlist = {
		type: "vlist", 
		height: ["auto", "auto", "auto", "auto"], 
		border_width: "5px", 
		children: [
			elms.text("Saini Ji"), 
			Menu, 
			{
				type: "hlist", 
				width: ["auto", "40%", "auto"], 
				children: [elms.text("uytr"), elms.text("A<br><a href='fghj' >Click here</a> <br>to download video"), elms.text("oooop")], 
				border_width: "15px", 
				border_color: "blue", 
				valign: "middle", 
				// bgcolor: "#ccc",
				padding: "0px"
			}, 
			{
				type: "vlist", 
				height: ["auto", "auto", "auto"], 
				border_width: "5px", 
				border_color: "yellow", 
				align: "center",
				children: [elms.text(111), elms.text(222), elms.text(9876545678)]
			}
		]
	}




