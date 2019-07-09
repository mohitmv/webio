


# fm = Frame(lambda: Button("Mohit"))

fm = Frame(lambda: 
	Hlist(
		Vlist(
			Text("Mohit", "  ", Text("Saini", onclick=lambda fm: print("Mohit")), onclick=lambda fm: print("Saini")), 
			align="middle", 
			height_1="400px", 
			# valign="middle", 
			border_width="1px", 
			onclick = lambda fm: print("Saini11")
		) for i in range(2)
	)
)



fm.run();
