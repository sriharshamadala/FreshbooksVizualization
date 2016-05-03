Clone this project to your local computer at a desired location:  
```shell
$ git clone https://github.com/sriharshamadala/FreshbooksVizualization.git
$ cd FreshbooksVizualization
```

### How to run the python script: Method 1
We have two submodules, one for the freshbooks API and the other for google visualization API. To update them:  
```shell
$ git submodule update --init --recursive
```
since the freshbooks API does not have \_\_init\_\_.py it cannot be imported as a module. Hence create an empty \_\_init\_\_.py file inside the submodule using any choice of your editor. Make sure this file is created, otherwise you will see an import error.
```shell
$ vim FreshbooksPython/__init__.py
```
Execute our main python script by passing the \<api\_url\> (e\.g\. company\_name\.freshbooks.com) and the \<authentication\_token\> as the arguments. You can find them in your freshbooks website under _profile_:
```shell
$ python MyFreshbooks.py api_url auth_token > timeline.html
```
Open _timeline.html_ in your browser to visulaize your freshbooks data. Hover over any project to see more details.

### How to run the python script: Method 2
Execute the shell script setup.sh, which basically does everything in Method 1.
```shell
$ setup.sh api_url auth_token timeline.html
```
If the shell script fails to generate the output follow Method 1.

#### Note:
* Tasks performed on weekends are highlighted in red.
* Each task description is preceeded by the number of hours spent on that particular task. The format is _hours_._minutes_. _minutes_ are normalized to 100.

For any issues with executing the script or feature requests please create an issue here.
