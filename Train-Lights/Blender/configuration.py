def configuration():

	config = {
		'background': {
			'style' :  # Rectangle, Circle, RecCir, Square
			'orientation' : #Vertical/Horizontal
			'border_size' :
			'thickness' :
			'colour' : {
				'diffuse' : [R, G, B]	# Fixed?
	 			'reflection1' : [R, G, B]	# Fixed?
	 			'reflection2' : [R, G, B]	# Fixed?
				'glossy' : [R, G, B]	# Fixed?
				}
		}
		'lights' : {
			'number_total' :
			'light' : ([[R, G, B, 'blank'],
						 [R, G, B, 'off'],
						 [R, G, B, 'on'],
						 [R, G, B, 'blank'],
						 [R, G, B, 'blank'],
						 [R, G, B, 'blank']])
			'light_can_depth' :
			'spacing_between_cans' :
			'light_can_radius' :
			'light_can_wall_thickness' :
			'can_hood_length' :
		}
	}
	return config