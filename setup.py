from setuptools import setup

setup(
  name = 'webio',
  version = '1.0.0',
  url = 'https://github.com/mohitmv/webio',
  author = 'Mohit Saini',
  author_email = 'mohitsaini1196@gmail.com',
  description = 'Tool for building complex web interfaces easily',
  long_description = 'WebIO enables you to design the complex web interfaces without getting into HTML, CSS, JS, AngularJs, Ajax, API handling, Server management, nodejs etc.. crap.',
  packages = ["webio"],
  package_data={'': ['front_end/index.html', 'front_end/css/main.css']},
  include_package_data=True,
  install_requires = ['flask_cors', 'flask'],
  extras_require = {}, 
  classifiers=[
    'Programming Language :: Python :: 3',
  ],
  entry_points={},
)

