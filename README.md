### How to run the python script
* Clone this project to your local computer:
	> \>>> git clone _https://github.com/sriharshamadala/FreshbooksVizualization.git_
* update the submodules:
    > \>>> git submodule update --init --recursive
* Execute the python script by passing the domain name and the api key as the arguments.
    > \>>> python MyFreshbooks.py \<domain_name\> \<api_key\> > timeline.html
* Open _timeline.html_ in your browser to visulaize your freshbooks data.
* Hover over any project phase to see more details regarding that project.

#### Note:
* Tasks performed on weekends are highlighted in red.
* Each task description is preceeded by the number of hours spent on that particular task. The format is _hours_._minutes_. _Minutes are normalized to hundred.
