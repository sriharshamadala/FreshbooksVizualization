### How to run the python script
Clone this project to your local computer:  
```shell
$ git clone https://github.com/sriharshamadala/FreshbooksVizualization.git
```
We have two submodules, one for the freshbooks API and the other for google visualization API. To update them:  
```shell
$ git submodule update --init --recursive
```
Execute our main python script by passing the <domain name> and the <api key> as the arguments. You can find them in your freshbooks website under _profile_:
```shell
$ python MyFreshbooks.py "domain name" "api key" > timeline.html
```
Open _timeline.html_ in your browser to visulaize your freshbooks data. Hover over any project to see more details.

#### Note:
* Tasks performed on weekends are highlighted in red.
* Each task description is preceeded by the number of hours spent on that particular task. The format is _hours_._minutes_. _minutes_ are normalized to 100.
