state = Object(posts = []);
# state.posts.append(dict(title="11", body="876", module="88899"));

def delete_from_list(l, index):
	print(l, index);
	return l[:index]+l[index+1:];



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


fm2 = Frame(lambda: 
	Vlist(
		(
			Hlist("Mohit - "+str(i), onclick=lambda fm: print(fm)) for i in range(10)
		), 
		border_width="1px"
	)
);



fm2.run();

