Front-end Elements
=======================

Front-end elements are used in `Render` method to create current frame of web interface. A frame is nothing but combination of front-end elements in tree like structure.
These front-end elements can be divided into 2 catogeries

**Atomic Elements** - elements, which are used for rendering an atomic entity on front-end. ex: icon, button, text-area, text etc. These elements work as leaf node in frame-tree.

**Combining Elements** - elements, which are used for combining other front-end elements. ex: HDiv (Horizontal-Division), VDiv (vertical division), etc.. These elements work as intermediate node in frame-tree.

Example:

```
VDiv(
  Button("Click Me"),
  Text("Hello"),
  HDiv(
    Button("Click-1"),
    Button("Click-2"),
    VDiv(
      Button("Click-3"),
      Text("Some text below Click-3")
    )
  )
)
```
Demo: https://i.imgur.com/xRUdDdw.png

In this frame, VDiv is used for creating vertical divison. VDiv displays the child elements in vertical list. HDiv is used for creating horizontal division. HDiv displays the child elements in horizontal list. By default HDiv allocates equal width to each of it's children from available width. However in case of VDiv, height is allocated as much as used.


Button
--------

It's used for rendering a labeled button.

Fixed parameters:
 - **label_string**: label of the button. ex: "Submit", "Click Me"

Optional parameters:
 - **icon**: icon name of [google's material](https://material.io/tools/icons) icon. ex: "menu".
        if present an icon will be attached along with label of button.
 - **disabled**: True|False. if a button is disabled, user won't be able to click on it.
 - **color_theme**: "back_in_white"| "blue"
 - **onclick**: lambda function to be executed whenever user click on this button.

Possible use:
```Python
Button("Submit")
Button("Click Me", onclick = lambda: self.set_current_tab(4))
```

IconButton
--------

It's used for rendering a icon-button.

Fixed params:
 - **icon**: icon name of [google's material](https://material.io/tools/icons) icon. ex: "arrow_right".

Optional params:
 - **disabled**: True|False. if a button is disabled, user won't be able to click on it.
 - **onclick**: lambda function to be executed whenever user click on this button.
 - **font_size**: font size with pixel unit. ex: "26px".
 - **label_string**: A hint-string to be displayed when user hover on this icon. ex: "Jump to Previous Page"


TextInput
------------
It's used for rendering a input box, where user can type a string.

Fixed params:
 - **label_string**: label of the input box. ex: "First Name", "Email", "Password"

Optional params:
 - **disabled**: True|False. if a TextInput box is disabled, user won't be able to type anything.
 - **onchange**: lambda function to be executed whenever user edit (type something or delete something) on this input box.
 - **value**: default value to be present in rendered input box. ex: "123"
 - **id**: identifier of this input box. ex: "name", "email" etc. if present, it can be accessed by `self.inputs[id]` i.e. `self.inputs["email"]`

Possible use:

```python
TextInput("Your Name")
```
```python
TextInput("Your Name", value="120")
```



TextArea
------------
It's used for rendering multiline input box, where user can type a paragraph.

Fixed params:
 - **label_string**: label of the input box. ex: "First Name", "Email", "Password"

Optional params:
 - **disabled**: True|False. if a TextArea is disabled, user won't be able to type anything.
 - **onchange**: lambda function to be executed whenever user edit (type something or delete something) on this input box.
 - **value**: default value to be present in rendered input box. ex: "123"
 - **default_rows** : number of rows by default. ex: 5
 - **id**: identifier of this input box. ex: "blog_content" etc. if present, it can be accessed by `self.inputs[id]` i.e. `self.inputs["blog_content"]`

Possible use:

```python
TextArea("Your Blog")
```

```python
TextArea("Your Blog", value = self.blogs[blog_id].content,
                      default_rows = 5)
```


DropDown
------------
It's used for creating a dropdown, so that a user can choose one of many options provided.

Fixed params:

 - **label_string**: label of the input box. ex: "First Name", "Email", "Password".

 - **options**: list of options to choose from. It can be one of two formats.
    - list of non-tuple objects. All the `option` objects must be convertiable to string. In this format `str(option)` will be displayed at front-end and `self.inputs[dropdown_id]` will return the python-object (original object without string conversion).
    - list of 2-sized tuple. second element of tuple must be convertiable to string. In this format, `str(option.second)` will be displayed as dropdown option to front-end and `self.inputs[dropdown_id]` will return the `option.first` python object (corrosponding to selected option).

Optional params:
 - **disabled** : True|False. if a DropDown is disabled, user won't be able to choose any option.

 - **allow_multiple** : True|False. if true, user can choose multiple options.

 - **value** : default value to be presented in rendered dropdown. In case of `allow_multiple=True`, value should be list of default-selected options.

 - **onchange**: lambda function to be executed whenever a option is chosen/modified.

 - **id**: identifier of this dropdown. ex: "age_group". if present, it can be accessed by `self.inputs[id]` i.e. `self.inputs["age_group"]`.

Possible use:

```python
DropDown("Age Group", options=[(enum.MID_AGE, "20-30 years"),
                               (enum.UPPER_AGE, "30+ years")],
                      id = "age_group",
                      value = enum.MID_AGE)

DropDown("Your Favorite Fruits", options=[(enum.Mango, "Mango"),
                                          (enum.Banana, "Banana"),
                                          (enum.Apple, "Apple")],
                                 id = "fav_fruits",
                                 allow_multiple = True,
                                 value = [enum.Mango, enum.Apple])

DropDown("Your Favorite Year", options=[1994, 1995, 1996],
                               id = "fav_year",
                               value = 1995)
```


Menu
---------
It's used for creating a menu of options. Each option in menu can trigger some action.

Fixed params:
 - **options** : List of 2-sized tuple. First element of tuple should be convertiable to string, which will be displayed as option. Second element of tuple should either be None or a lambda function. If a user click on any option, corrosponding lambda function will be executed.

Optional params:
 - **disabled** : True|False. if Menu is disabled, user won't be able to choose any option.
 - **icon** : [default: "menu"] icon name of [google's material](https://material.io/tools/icons) icon. ex: "menu". if present a different icon will be used for menu.
 - **font_size** : font size with pixel unit. ex: "26px". (size of menu icon)

Possible use:

```python
Menu(options = [
                ["Delete", lambda: os.system("rm -rf " + self.current_dir)],
                ["Copy", Action(self.CopyMove, i, True)],
                ["Move", Action(self.CopyMove, i, False)],
               ],
     icon = "more_vert");
```

VSpace
-------
It's used for creating dummy vertical space.

Fixed params:

 - **size**: space size with pixel unit. ex: "20px".

Possible use:

```python
VSpace("20px")
```



Text
-----------
It's used for displaying text. It can have child Text elements, to control the text style and linking in a sub section.

Fixed params: variable arguments, each of them can be either Text element or string.

Possible use:

`Text("Once upon a time, there was a ", Text("lion", color = "red"), "which jumped from a big mountain named ", Text("Super Star Mountain", link = "http://www.super_mountain.com"), ". But the lion didn't die")`




VDiv
------------
VDiv(Vertical Divison) is used for rendering the vertically aligned front-end elements.

Fixed params: variable arguments, each of them should be front-end element. These arguments are called child elements. A `VDiv` element can be children of another `VDiv` or `HDiv` element to suppport complete mix and match.

- `VDiv` support `<<` operator for adding more children to an `VDiv` element.

Possible use:

```python
VDiv(
  Button("Click Me"),
  Text("Hello"),
  HDiv(
    Button("Click-1"),
    Button("Click-2"),
    VDiv(
      Button("Click-3"),
      Text("Some text below Click-3")
    )
  )
)
```

-----------------------------------------

```python
frame = VDiv(
          Button("Click Me"),
        );
frame << Text("Hello");
hdiv = HDiv();
hdiv << Button("Click-1");
hdiv << Button("Click-2");
hdiv << VDiv(
          Button("Click-3"),
          Text("Some text below Click-3")
        );
frame << hdiv;
```
https://i.imgur.com/xRUdDdw.png

HDiv
------------
HDiv( Horizontal divisin) is used for rendering the horizontally aligned front-end elements. Each child element is allocated same width by default.

Possible use:

```python
HDiv(
  Button("Click-1"),
  Button("Click-2"),
  VDiv(
    Button("Click-3"),
    Text("Some text below Click-3")
  )
)
```


Additional Details
=======================

Action Handlers
--------

`onclick` or `onchange` methods expects a action handler, which has to be lambda function or any other callable python object, expecting 0 input argument. These lambda-function should not refer to temporary variables (ex: loop iterator variable etc.), because these action handlers will be executed outside the scope of `Render` method and python's lambda function doesn't capture the refered variable by value.

Solution is: use custom functors instead of python's lambda function. 


**webio.Action** is a functor, which expects a lambda method, followed by arbetery number of arguments, followed by arbetery number of labeled-arguments.. It returns a callable object, which internally calls the underlying lambda method. This functor captures the provided arguments by value to be used when required.


```python
# Wrong Way
for i in range(3):
  j = i*100;
  frame << Button("Print("+str(i)+")", onclick = lambda: print(i, j))
```

onclick for the button, should be used with help of Action functor. In this example: i,j are temporary. `lambda: print(i,j)` doesn't capture the current value of i and j.

```python
# Correct Way
for i in range(3):
  j = i*100;
  frame << Button("Print("+str(i)+")", onclick = Action(lambda i, j: print(i, j), i, j))
```

However in this object `Action(lambda i,j: print(i, j), i, j)`, i and j are captured by value and lambda-function is not dependent on current value of i and j.

--------------

Possible implementation of `webio.Action`
```python
class Action:
  def __init__(self, main_lambda, *args, **params):
    self.main_lambda = main_lambda;
    self.args = args;
    self.params = params;
  def __call__(self, *x):
    return self.main_lambda(*x, *self.args, **self.params);
```


Google's Material Icons
--------
[google's material](https://material.io/tools/icons) icons are interally imported by webio. If you want to use any icon, just search for suitable icon and use the icon name. ex: "menu", "more_vert" etc.


webio.Serve
--------
**webio.Serve** : is used for serving python web-interface class as web-server on a specified port.

`Serve(web-interface-class, args=(), params={}, port=5001)`

If constructor of the web-interface class require some parameter, then those parameters must be passed to Serve method, so that whenever a new instance of web-interface is requested, webio can create a new object of web-interface-class with given parameters.




Exception and Error Messages
--------------
**exceptions**
1. **CLIENT_INSTANCE_TIMEOUT** - Everytime web interface is opened in url, a new instance of web-interface-class is created. Life cycle of the instance object (of web-interface-class) is fundamentally responsible for what is being rendered on the front-end. if a client doesn't do any activity for more than 3600 seconds, then instance object is destroyed at backend. Once backend doesn't own the instance object for a front-end instance, it will give CLIENT_INSTANCE_TIMEOUT error. In this situation client has to refresh the page (i.e. create a new instance and proceed).

2. **INCORRECT_SERVER_INSTANCE** - Whenever backend server is executed (i.e. python webio script), it is attached with a unique id. If server is restarted, it can't serve the client, which was instanted by different backend server. In such situation, client will face INCORRECT_SERVER_INSTANCE. In this situation, client has to refresh the page.

3. **INTERNAL_ERROR** - It occures whenever action handlers (ex: onclick, onchange) fails with exception.

4. **SUCCESS**

5. **INVALID_ACTION** - It won't occure unless webio's front-end is fiddled.

6. **INCOMPLETE_INPUT_VALUES** - It won't occure unless webio's front-end is fiddled.

