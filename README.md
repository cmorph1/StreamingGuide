# StreamingGuide
A way to search your streaming sites and find the film you are looking for

The 2 python files StreamGuideApp and StreamGuideProgram are used to build a GUI and search the 3 streaming services (Amazon, Now TV & Netflix). 

StreamGuideProgram handles the heavy work, searching the sites and returning strings (ideally 10 different options), however sometimes the streaming services don' allow for this.

StreamGuideApp provides the UI and uses instances of the classes created in StreamGuideProgram to return the links based on what a user inputs as a search, as well as taking in the users login information.
