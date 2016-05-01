#!/usr/bin/python
from FreshbooksPython import freshbooks
from GoogleVisualizationPython import gviz_api
from datetime import datetime, timedelta
import sys
import re

page_template = """
<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load("current", {packages:["timeline"]});
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {
        var container = document.getElementById('timeline1.0');
        var chart = new google.visualization.Timeline(container);
        var dataTable = new google.visualization.DataTable();
        %(jscode)s
        chart.draw(dataTable);
        var options = {
            title: 'Projects Timeline',
            // This line makes the entire category's tooltip active.
            focusTarget: 'category',
            // Use an HTML tooltip.
            tooltip: { isHtml: true }
          };
      }
    </script>
  </head>
  <body>
    <div id="timeline1.0" style="height: 800px;"></div>
  </body>
</html>
"""

def CreateCustomHtmlContent(projectPhase):
    retString = '<div> <table>';
    isGrey = True
    TaskList = projectPhase['taskDescription']
    for ii in xrange(len(TaskList)):
        task = TaskList[ii]
        isWeekDay = datetime.weekday(projectPhase['taskDate'][ii])
        timeSpent = projectPhase['taskHours'][ii]
        if task is not None:
            task = "[" + "{0:05.2f}".format(round(timeSpent,2)) + "] " + task
            if isGrey:
                if (isWeekDay==5) or (isWeekDay==6):
                    retString = retString + '<tr bgcolor="#D6D6D6"><td><font FACE="calibri" size=2 color="red">' + task + '</font></td></tr>'
                else:
                    retString = retString + '<tr bgcolor="#D6D6D6"><td><font FACE="calibri" size=2>' + task + '</font></td></tr>'
                isGrey = False
            else:
                if (isWeekDay==5) or (isWeekDay==6):
                    retString = retString + '<tr bgcolor="white"><td><font FACE="calibri" size=2 color="red">' + task + '</font></td></tr>'
                else:
                    retString = retString + '<tr bgcolor="white"><td><font FACE="calibri" size=2>' + task + '</font></td></tr>'
                isGrey = True
    retString = retString + '</table></div>'
    return retString;

def projectName(MyProjects, projectID):
    if projectID in MyProjects.keys():
        return MyProjects[projectID]
    else:
        return "Decommisioned Project"

def NotesParser(notes):
    if notes:
        return re.sub(r'[^a-zA-Z\d\s\.\?:]', '', notes)
    else:
        return None

def main():
    # Api key to request data
    freshbooks.setup(sys.argv[1], sys.argv[2])

    # Any project discontinuity greater than threshold gets broken down.
    discontinuityThresholdDelta = timedelta(days=5)

    # Pulling the data from freshbooks.
    vizData = []
    for time_entry in freshbooks.TimeEntry.list(get_all=True):
        vizData.append({'time_entry_id': time_entry.time_entry_id, 
                'project_id': time_entry.project_id,
                'task_id': time_entry.task_id,
                'hours': time_entry.hours,
                'date': time_entry.date,
                'notes': time_entry.notes})

    # Creating a project id and project name dictionary
    MyProjects = {}
    for project in freshbooks.Project.list(get_all=True):
        MyProjects[project.project_id] = project.name

    # Store projects in phases.
    MyProjectsInPhases = {}
    for time_entry in vizData:
        current_pid = time_entry['project_id']
        if current_pid in MyProjectsInPhases.keys():
            foundTask = False
            for tmpDict in MyProjectsInPhases[current_pid]:
                if (time_entry['date'] > (tmpDict['start']-discontinuityThresholdDelta)) and (time_entry['date'] < (tmpDict['end']+discontinuityThresholdDelta)):
                    tmpDict['taskDescription'].append(NotesParser(time_entry['notes']))
                    tmpDict['taskDate'].append(time_entry['date'])
                    tmpDict['taskHours'].append(time_entry['hours'])
                    # Adjust the start or end dates.
                    if (time_entry['date'] < tmpDict['start']):
                        tmpDict['start'] = time_entry['date']
                    elif (time_entry['date'] > tmpDict['end']):
                        tmpDict['end'] = time_entry['date']
                    foundTask = True
                    break
            if not foundTask:
                tmpDict = {}
                tmpDict['projectName'] = projectName(MyProjects, current_pid)
                tmpDict['start'] = time_entry['date']
                tmpDict['end'] = time_entry['date']
                tmpDict['taskDescription'] = []
                tmpDict['taskDate'] = []
                tmpDict['taskHours'] = []
                tmpDict['taskDescription'].append(NotesParser(time_entry['notes']))
                tmpDict['taskDate'].append(time_entry['date'])
                tmpDict['taskHours'].append(time_entry['hours'])
                MyProjectsInPhases[current_pid].append(tmpDict)
        else:
            MyProjectsInPhases[current_pid] = []
            tmpDict = {}
            tmpDict['projectName'] = projectName(MyProjects, current_pid)
            tmpDict['start'] = time_entry['date']
            tmpDict['end'] = time_entry['date']
            tmpDict['taskDescription'] = []
            tmpDict['taskDate'] = []
            tmpDict['taskHours'] = []
            tmpDict['taskDescription'].append(NotesParser(time_entry['notes']))
            tmpDict['taskDate'].append(time_entry['date'])
            tmpDict['taskHours'].append(time_entry['hours'])
            MyProjectsInPhases[current_pid].append(tmpDict)

    # Adding columns to dataTable
    description = {"projectId": ("string", "Project ID"),
             "projectName": ("string", "Project Name"),
             "description": ("string", "description", {'role':'tooltip', 'html':'true'}),
             "start": ("date", "Start"),
             "end": ("date", "End")}

    # Adding rows to dataTable
    data = []
    for tmp in MyProjectsInPhases.keys():
        for projectPhase in MyProjectsInPhases[tmp]:
            tmpRow = {}
            tmpRow['projectId'] = tmp
            tmpRow['projectName'] = projectPhase['projectName']
            tmpRow['description'] = CreateCustomHtmlContent(projectPhase)
            tmpRow['start'] = projectPhase['start']
            tmpRow['end'] = projectPhase['end']
            data.append(tmpRow)

    # Loading it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    # Creating a JavaScript code string
    jscode = data_table.ToJSCode("dataTable",columns_order=("projectId", "projectName", "description", "start", "end"))

    # Putting the JS code and JSon string into the template
    print page_template % vars()

if __name__ == "__main__":
    main()
