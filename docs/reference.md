
- icon: icon name of google's material icon. ex: "menu"
- disabled: True|False

VDiv
------------

VDiv is used for rendering the front-end elements in vertical alignment.



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
 - **id**: identifier of this input box. ex: "name", "email" etc.
           if present, it can be accessed by `self.inputs[id]` i.e. `self.inputs["email"]`

Sample use cases:

```python TextInput("Your Name") ```

```python TextInput("Your Name", value="120") ```



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

Sample use cases:

```python TextArea("Your Blog") ```

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
 - **id**: identifier of this dropdown. ex: "age_group". if present, it can be accessed by `self.inputs[id]` i.e. `self.inputs["age_group"]`.

Sample use cases:

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
