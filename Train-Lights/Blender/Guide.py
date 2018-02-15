# Style
Background_style = # Rectangle, Circle, RecCir, Square
	Colour/Roughness etc = 
	Background thickness = 
	
	if Rectangle
		Max_lights[] = (4, 3) # Fixed size maximum lights on style

		Number_of_blanks =
		Number_of_lights =
		Light()
		Blank()

		Vertical or Horizontal =
		Background border top = 
		Background border bottom = 
		Background border sides = 
		Create_background()
		Place_Lights()


	if Circle
		Max_lights =  # Fixed size maximum lights on style
		Number_of_lights =
		Number_of_blanks =

		Light()
		Blank()

		Vertical or Horizontal =
		Background border =

		Create_background()
		Place_Lights()


	if RecCir
		Max_lights[] = (4, 3) # Fixed size maximum lights on style
		Number_of_lights =
		Number_of_blanks =

		Light()
		Blank()

		Background border top = 
		Background border bottom = 
		Background border sides = 

		Create_background()
		Place_Lights()

	if Square # 5 lights dice face pattern
		Number_of_lights =
		Number_of_blanks =

		Light()
		Blank()

		Background border =

		Create_background()
		Place_Lights()

Light()
	Light can depth =
	Spacing between cans =
	Light can radius =
	Light can wall thickness =
	- ON/OFF
		Colour = 

Blank()


