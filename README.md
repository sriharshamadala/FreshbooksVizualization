### How to run the python script: Method 1
Clone this project to your local computer:  
```shell
$ git clone https://github.com/sriharshamadala/FreshbooksVizualization.git
```
We have two submodules, one for the freshbooks API and the other for google visualization API. To update them:  
```shell
$ cd FreshbooksVizualization
$ git submodule update --init --recursive
```
since the freshbooks API does not have \_\_init\_\_.py it cannot be imported as a module. Hence create an empty \_\_init\_\_.py file inside the submodule using any choice of your editor. 
```shell
$ vim FreshbooksPython/__init__.py
```
Execute our main python script by passing the \<domain\_name\> and the \<api\_key\> as the arguments. You can find them in your freshbooks website under _profile_:
```shell
$ python MyFreshbooks.py domain_name api_key > timeline.html
```
Open _timeline.html_ in your browser to visulaize your freshbooks data. Hover over any project to see more details.

### How to run the python script: Method 2
Execute the shell script setup.sh, which basically does everything in Method 1.
```shell
$ setup.sh domain_name api_key timeline.html
```

#### Note:
* Tasks performed on weekends are highlighted in red.
* Each task description is preceeded by the number of hours spent on that particular task. The format is _hours_._minutes_. _minutes_ are normalized to 100.

For any issues with executing the script or feature requests please create an issue here.
