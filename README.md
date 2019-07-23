Welcome to webio
===================

WebIO enables you to design the complex web interfaces without getting into HTML, CSS, JS, AngularJs, Ajax,
API handling, Server management, nodejs etc...

The web interface built by webio doesn't look pixel-perfect but it's good enough to support all the desired interaction.

Web interfaces which don't require pixel-perfect graphics like: admin panels, internal dashboard, server monitoring page, application's intenal control, jenkins website, etc.. can be built on webio.

webio offers a simple set of web elements to be included in your backend code ( C++ , Python or Java), which internally
build a fully functional web interface as desired. Once webio is integrated in program, it does everything to support backend API handling, as well as auto-generate the front-end of desired web-interface.
webio is extremely easy to use, having a 3-pager user manual.

How to use webio in python3 ?
----------

[Demo-1](https://github.com/mohitmv/webio/blob/master/docs/demo/tabs_and_card.md) : Navbar with 4 tabs, each having cards and option to add more cards.

[Demo-2](https://github.com/mohitmv/webio/blob/master/docs/demo/file_system_ui.md) : GUI of linux file system

**Syntax**

```python
import webio
class MyWebsite:
  def Render(self):
    return webio.Text("Hello World");

webio.Serve(MyWebsite, port = 5003);
```

To create a web interface using webio-python, you need to create a python-class, having `Render` method. This class, known as named serving-class can be served with `webio.Serve` method. Run this hello_world python script (python3) and desired web interface is served on `http://<IP>:<PORT>` ( ex: `http://127.0.0.1:5002`) url. Everytime a user opens the url in a new tab, a new object of `MyWebsite` class will be created to serve that perticular instance.

Serving-class can have static variable to maintain the persistent state across different instances of web interface. ( To store global information ex: comments, posts, etc..). Similarly serving-class can have non-static variables to maintain and manipulation of current state of an instance of web-interface. Ex: variable `current_tab` is non-static variable, since it's specific to an instance of web-interface.

**Frame Rendering and state**

webio supports various front-end elements to help you design the GUI. Render function is used for building the current frame of web-interfac. A frame is the tree-like-combination of front-end elements, programmatically built by `Render` function. Current frame is built using current state. Whenever current state is changed, current frame is recalculated and rerendered on front-end.

```python
from webio import Serve, VDiv, Button

class MyWebsite:
  def __init__(self):
    self.num =  2;
  def Render(self):
    frame = VDiv(); 
    for i in range(self.num):
      frame << Button("Button-" + str(i),
                      onclick = lambda: self.__dict__.update(num = 1+self.num));
    return frame;

Serve(MyWebsite, port = 5004);
```
![alt text](https://i.imgur.com/2WwVRv4.gif "webio demo variable buttons")

In this example: value of `self.num` is incremented whenever user click on Button. Which cause re-calculation of current frame and re-rendering of front-end elements displayed. Note that re-rendering doesn't reload the entire front-end. In the process of re-rendering, differences from previous frame are updated in current frame to reflect the minimum change in front-end.


webio reference
----------
[webio reference for python3](https://github.com/mohitmv/webio/blob/master/docs/reference.md)


How to install webio in python3 ?
----------
`sudo pip3.6 install git+https://github.com/mohitmv/webio.git`

or

`sudo pip3.6 install git+https://github.com/mohitmv/webio.git@v1.0.0`

How to uninstall webio in python3 ?
----------
`sudo pip3.6 uninstall webio`

