def configuration():

    config = {
        'field': {
            'dimensions': {
                'width': 7
                'length': 10
            },
            'grass': {
                'colour': [0,0,0],
                'shininess': 0.5, # Maybe? other parameters like this you come across
                'blade_length': normal_distribution(0.06, 0.006),
                'blade_width': {
                  'base': 0.02,
                  'tip': 0.01
                },
                'angle': {
                    'roll': 0
                    'pitch': 0
                    'yaw': 0
                }
            },

            'lines': {
                'width': 0.06,

                'goal_zone': {
                   'depth': 0.6,
                   'width': 2.6
                },

                'goal_box': {
                    'length': 1,
                    'width': 5
                },

                'mark': {
                    'distance': 2.05,
                    'width': 0.1
                },

                'centre_circle': {
                    'radius': 0.78
                }
            }
        }
    }

    config.update({
        'goal': {
            'post': {
                'shape': 'RECTANGLE',
                'width': 0.10,
                'depth': 0.10
            },

            'position': [
                config['field']['lines'],
                config['field']['lines']
            ],

            'height': 1.8,
            'net': {
                'height': 1.0
            }
        }
    })

    config.update({
        'ball': {
            'position': [
                x,
                y,
                0
            ],

            'radius': 0.075
        }
    })

    config.update({
        'obstacles': None
    })

    # Lighting
    # Environment
    config.update({
        'scene': None
    })

    # Camera position/projection
    config.update({
        'camera': {
            'lens': {
                'projection': 'RECTILINEAR'
            },
            'position': [
            ],
            'rotation': [
            ]
        }
    })

    return config