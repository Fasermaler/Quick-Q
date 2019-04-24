# CutQ Vision Class

The cutQ vision class deal with the computer vision aspect of CutQ. The class takes in video/live stream from a Raspberry Pi camera to detect aruco markers and calculate the prices of the drinks labelled with aruco markers. 

The vision class refers to 5 other custom class files and 2 external files. The 'config' file contains the user configuration parameters for easy editing while the 'prices.csv' file stores the price information required to link the aruco marker IDs to their respective drinks and price.

More information on the 5 custom classes will be made available below. Every class will have it's own unit test code below the class definition. All classes have been completely written but some have yet to complete their respective unit tests.

#### Running the vision class

The vision class takes in 3 console arguments:

1. `-v` or `--video`: this specifies the path of the video file. If not file is specified, the class will initialize the RPi camera and use live feed instead
2. `-i` or `--imshow`: this specifies whether to display the vision output on the monitor for display or debugging purposes. The default for this argument is `True`.
3. `-p` or `--prices`: this allows the user to define a custom price file. By default the file 'prices.csv' will be read

Examples:

-  `python cutQ_vision_class.py -v test.mp4 -i False` - will run the code on the file `test.mp4` and not show the vision output on the monitor
- `python cutQ_vision_class.py -imshow True -prices new_prices.csv` - will run the code through the RPi camera feed and use the file 'new_prices.csv' as the price file.

- `python cutQ_vision_class.py -h` - will display help on what the arguments do



*Note: `config_reader` is defunct because configuration reading functionality is now under `csv_reader`.*



##### Unit Test Progress

- `csv_reader` : Complete

- `price_calculator`: Complete

- `arg_parser`: Complete

- `aruco_detector`: Incomplete

- `video_reader`: Incomplete

- `picam_class`: Incomplete



##### To Do

- Quick Install Scripts
- Improved Vision Viewer
- Quick Startup Scripts

### csv_reader.py

This file contains the `csv_reader` class. 

##### Attributes

- `prices_ls`: Stores the price dictionary information in the format `{'id':(drinkname, price)}`

- `config_ls`: Stores the config file information in a dictionary

- `pi_height`, `pi_width`, `pi_fps` are attributes initialized only under the `get_config` subroutine and contain configuration information for the RPi Camera (height, width and fps of the camera)

Additionally, the class intializes 2 csv dialects under the `__init__` subroutine. The `prices` dialect is used when reading from the 'prices.csv' file while the `config` dialect is used when reading from the 'config.csv' file. This is because 'prices.csv' used a comma as it's delimiter while 'config.csv' uses a space as it's delimiter.

##### Methods

- `__init__(self)` initializes the class
- `get_prices(self, file='prices.csv')` loads the 'prices.csv' file. The user can also define a custom file path
- `print_prices(self)` prints the price list (now defunct)
- `get_config(self, file='config')` loads the 'config' file. The user can also define a custom file path. This method also initializes the `pi_height`, `pi_width`, `pi_fps` attributes.



### price_calculator

The price calculator class calculates the total price of drinks when given a list of IDs identified by the aruco detector.

##### Attributes

- `drinks_list` stores the list of drinks 
- `total_price` stores the total price of aforementioned list of drinks
- `old_ids` stores the list of IDs used when calculating the above 2 attributes
- `price_list` stores the price list as read by the csv_reader object, this attribute is set by the `set_price_list` method

These attributes are only reset by `reset_all` and every time the `calculate_price` method is called.

##### Methods

- `__init__(self, price_list)` Initializes the attributes and calls `set_price_list` to set the price list

- `set_price_list(self, price_list)`Set the price list 

- `calculate_price(self, ids)` Calculates the price from a list of IDs 

  - Resets `drinks_list`, `total_price` and `old_ids`
  - updates `old_ids` with the list of IDs given
  - converts the list of IDs to a list of drinks and stores it in `drinks_list`
  - calculates the cost of all the drinks using `price_list` and stores the information in `total_price`

  This method does not return any value, the attribute should be called directly.

- `add_item(self, ids)`This method allows more items to be added and the total price updated. It takes in a list of IDs of items **to be added**. Then it does the following:
  - Converts the list of IDs to drinks and appends the `drinks_list`
  - Calculates the prices of the new drinks and adds them to `total_price`
  - Extends the `old_ids` list with the new list
- `reset_all` resets `drinks_list`, `total_price` and `old_ids`



### arg_parser

`arg_parser` is the argument parsing wrapper for parsing console arguments given to the cutQ vision class. It uses the python `argparse` library.

##### Attributes

- `parser` this is the argparse object for parsing system console arguments. The description provided is 'Detects drinks in a video stream'
- `video_path` stores the video path information when obtained.
- `imshow` stores the information of whether the user wants vision to be shown on screen
- `price_path` stores information on the path of the price file

##### Methods

- `def __init__(self, default_video=None, default_imshow=True, default_prices='prices.csv')` this is the initialization method. It allows the defaults for the argparser to be defined. It also initializes the `video_path`, `imshow` and `price_path` variables.
- `parse_arguments(self)` does the actual argument parsing. It then assigns the arguments parsed to `video_path`, `imshow` and `price_path`  accordingly.

### aruco_detector

This class initializes the aruco dictionary and identifies any aruco markers in a frame that it is provided. It will return a list of aruco IDs from the identified markers. The class uses the `cv2`, `numpy` and `cv2.aruco` libraries.



##### Attributes

- `aruco_dict` dictionary of aruco markers
- `parameters` aruco detection parameters
- `font` font to be used when drawing text over the frame



##### Methods

- `__init__(self, aruco_format=6)` The initialization function takes in an optional argument `aruco_format`. This determines the size of aruco markers being used (4, 5 or 6). The default is 6. The `aruco_dict` will be generated accordingly. The `parameters` will also be created using the `aruco.DetectorParameters_create()` method from the cv2 aruco library.
- `return_aruco_ids(self, frame, full_color=True)`This method returns a list of coordinates for the aruco markers (`corners`) and a list of IDs (`ids`). It takes in the `frame` to be processed and the optional argument `full_color` which determines if the frame is full color or single_channel. This is important as the frame has to undergo conversion if it is full color. 
- `draw_markers(self, frame, corners, ids, text=None, id_flag=False, text_flag=False)` This draws the markers as well as any other optional information specified (by default all disabled).
  - `frame` the frame to be drawn on
  - `ids` the list of IDs to draw on the frame
  - `text` the list of text to be drawn on the frame. The intention is for text to be a list of drink labels for the respective aruco markers.
  - `id_flag` whether IDs should be drawn (default, `False`)
  - `id_flag` whether text should be drawn (default, `False`)

### video_reader

Video reader reads from a video file and updates an internal attribute `frame` which can then be pulled by the cutQ vision class directly to get the latest frame. The `video_reader` class has similar attributes to the `picam_class` so as to allow the cutQ vision class to easily interface with either classes using the same code.

The `video_reader` class uses the `cv2` and `numpy` libraries. The `thread` library is only imported for unit testing. The intention is for the `video_reader` class to be multithreaded in the cutQ vision class.

##### Attributes

- `frame` current active frame
- `cap` opencv capture object
- `terminate` termination flag required to close the capture loop when multithreaded
- `video` path of the video to be read

##### Methods

- `__init__(self, video)` Initializes the attributes and assigns the `video` path to the attribute `video`
- `read_video(self)` Starts the capture object with the video path and runs indefinitely, updating the `frame` attribute with the next video frame. Will display "[Error] Unable to open video stream or file" if it runs into an issue
- `def __call__(self)` magic method that calls the `read_video` method. 



### pi_cam

The `pi_cam` class has many similar interfaces to the `video_reader` class as they are meant to be interchangeable within the cutQ vision class itself. It uses the `picamera`, `picamera.array` ,`time`and `PIL`libraries. 

The `thread` library is imported only for multithreaded unit testing.

##### Attributes

- `camera` the RPI camera object
- `camera.resolution` sets the camera resolution
- `camera.framerate` sets the camera framerate in FPS
- `rawCapture` sets the RPi camera rawCapture object
- `frame` current active frame (similar to `video_reader`)
- `terminate` termination flag for multithreading (similar to `video_reader`)

##### Methods

- `__init__(self, h=240, w=426, fps=32)`Initializes the RPi camera object with the parameters given (h - height, w - width, fps - framerate). In the cutQ vision class, the params from the config file will be passed to this method
- `get_single_frame(self)` Gets a single frame (defunct, only used for testing)
- `flush_buffer_single(self, flush_count=5)` Gets a single frame after flushing the frame buffer. The `flush_count` determines how many frames get flushed. The `flush_count` can range from 1 (no flush) to 10, with a default of 5. Too much flush at low framerates will adversely affect detection performance.
- `get_frame_continuous(self, flush_count=5)` same as the previous method but gets frame continuously. The exit condition for this method is the `terminate` flag as it the primary method used for multithreading in the cutQ vision class.