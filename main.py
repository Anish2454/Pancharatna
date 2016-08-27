#! /usr/bin/python
import cgi
import cgitb
import json

cgitb.enable()

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'Washington D.C',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

HTML_HEADER = 'Content-type: text/html\n\n'

Top_HTML = '''
<html>
<head>
<title>2016 Democratic Primary</title>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<link href='https://fonts.googleapis.com/css?family=Playfair+Display' rel='stylesheet' type='text/css'>
</head>
<body>
<style>
.nav{
	border:1px solid #ccc;
    border-width:1px 0;
    list-style:none;
    margin:0;
    padding:0;
    text-align:center;
}
.nav li{
    display:inline;
}
.nav a{
    display:inline-block;
    padding:10px;
    color: black;
    text-decoration: none;
    font-size: 17px;
    line-height: 26px;
    font-family: "Playfair Display", serif;}

.nav a:hover {
  font-size: 30px;}

#caucus {
  font-size: 17px;
  font-family: "Playfair Display", serif;
}

footer {
    width: 100%;
}


</style>
<ul class = "nav">
  <li><a href="http://marge.stuy.edu/~anish.shenoy/Final_Project/main.py">Home</a></li>
  <li><a href="https://www.washingtonpost.com/graphics/politics/2016-election/primaries/schedule/">Primary Dates</a></li>
  <li><a href="https://votesmart.org/education/presidential-primary#.V1NTW7grKUk">Information on Primaries</a></li>

</ul>
'''

Bottom_HTML = '''
<footer class = "nav">
    <center><p style="font-size: 15px;"> All Data on this site was provided by RealClearPolitics. Delegate totals are subject to change. Page Created By Anish Shenoy and Kevin Boodram.</p></center>
</footer></body></html> '''

def convertListToJs(list):
    finalString = "["
    for i in list:
        finalString += "'" + str(i) + "', "
    finalString += "]"
    return finalString

def openFile(filename):
    f = open(filename, "rU")
    s = f.read()
    f.close()
    return s

def organize():
    s = openFile("demdata.csv")
    stateByState = s.split("\n")
    lst = [i.split(",") for i in stateByState]
    keys = lst[0]
    mD = {}
    for i in lst[1:-1]:
       d = {}
       for n in range(len(keys)):
           if n < len(i):
               d[keys[n]] = i[n]
           else:
               d[keys[n]] = ""
       if d["Bernie Delegates"] != "" and d["Clinton Delegates"] != "":
           if max(int(d["Bernie Delegates"]), int(d["Clinton Delegates"])) == int(d["Bernie Delegates"]):
               d["Winner"] = "Bernie"
           else:
               d["Winner"] = "Clinton"
       else:
           d["Winner"] = "None"
       if i[0] in us_state_abbrev:
           mD[us_state_abbrev.get(i[0], "")] = d
       else:
           mD[i[0]] = d

    return mD

def locationsAndValues(masterDict):
    winnerDict = {"Bernie":0, "Clinton":1, "None":0.5}
    locations =[]
    values = []
    for i in masterDict:
        if len(i) == 2:
            if "Winner" in masterDict[i]:
                locations.append(i)
                values.append(winnerDict[masterDict[i]["Winner"]])
    return [locations, values]

def displayMap(masterDict):
    locationsValues = locationsAndValues(masterDict)
    js = '''
    var chartDiv = document.getElementById('chart-div');
    var data = [{
    type: "choropleth",
    locations: ''' + convertListToJs(locationsValues[0]) + "," + '''
    locationmode: "USA-states",
    colorscale: [[0,"rgb(102, 187, 106)"], [1,"rgb(21, 101, 192)"]],
    showscale: false,
    hoverinfo: "location",
    z: ''' + convertListToJs(locationsValues[1]) + ''',
    marker: {
    line: {
    width: 2,
    color: "white"
    }
    }
    }];
    var layout = {
    autosize: false,
    margin: {
        t: 1
    },
    width: window.innerWidth/2,
    height: window.innerHeight - 200,
    geo: {
      scope: "usa",
      showlakes: false,
      lakecolor: 'cyan'
    },
    font: {
       family: 'Playfair Display, serif',
       size: 24,
       color: "Black",
       bold: true
       }
    };
    Plotly.plot(chartDiv, data, layout);

    chartDiv.on("plotly_click", function(data){
    window.open("main.py?state=" + data.points[0].location);
    });
    '''
    print('<center><div id="header"><h1>The 2016 Democratic Primaries</h1><p>With the upcoming elections predicted to be one of the most influential elections in history, it is imperative that we have some of the most informed voters. This map is updated daily with results from the democratic primaries; <b>click on a state</b> for more information on how that state voted.</p></div></center>')
    style = '''
    <style>
    #header {
        position: relative;
    }
    h1{
        font-family: "Playfair Display", serif;
        font-size: 50px;
        color: "black";
        text-decoration: underline;
    }
    p {
        width: 1250px;
        font-size: 23px;
    }
      .my-legend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-family: "Playfair Display", serif;
    font-weight: bold;
    font-size: 90%;
    }
  .my-legend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .my-legend .legend-scale ul li {
    font-size: 80%;
    font-family: "Playfair Display", serif;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .my-legend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
    #legend, #chart-div {
        display: inline-block;
    }
    #legend{
        float: right;
        position: relative;
        margin-top: 15%;
    }
    #chartLegend{
        display: flex;
        margin-left: 25%;
    }
    </style>
    '''
    print('<center><div id="chartLegend">')
    print('<div id="chart-div"></div>')
    legend = '''
    <div id = "legend" class='my-legend'>
    <div class='legend-title'>Legend</div>
    <div class='legend-scale'>
    <ul class='legend-labels'>
    <li><span style='background:rgb(102, 187, 106);'></span>Bernie Sanders</li>
    <li><span style='background:rgb(21, 101, 192);'></span>Hillary Clinton</li>
    <li><span style='background:rgb(62, 144, 149);'></span>TBD</li>
    </ul>
    </div>
    </div> '''
    print(legend)
    print('</div></center>')
    print(style)
    print("<script>")
    print(js)
    print("</script>")

def plotDelgateGraph(bernieDel, clintonDel, state, divName):
    js = '''
    var trace1 = {
        x: ''' + convertListToJs([bernieDel]) + "," + '''
        y: ["Sanders"],
        name: "Bernie Sanders ",
        orientation: 'h',
        type: 'bar',
        marker: {
            color: 'rgba(102, 187, 106, .5)',
            width: 1
        }
    };

    var trace2 = {
        x: ''' + convertListToJs([clintonDel]) +',' + '''
        y: ["Clinton"],
        name: 'Hillary Cinton ',
        orientation: 'h',
        type: 'bar',
        marker: {
            color: "rgba(21, 101, 192, 0.5)",
            width: 1
        }
    };

    var data = [trace1, trace2];

    var layout = {
        title: 'The ''' + states[state] + ''' Delegate Count',
        width: (window.innerwidth / 2),
        height: 350,
        font: {
           family: 'Playfair Display, serif',
           size: 20,
           color: 666
           }
    };

    Plotly.newPlot("''' + divName + '''", data, layout);
    '''
    return js

def plotDelgatePie(bernieDel, clintonDel, state, divName):
    values = [bernieDel, clintonDel]
    js = '''
    var data = [{
      values: ''' + convertListToJs(values) + ',' + '''
      labels: ['Bernie Sanders ', 'Hillary Clinton '],
      type: 'pie',
      marker :{
        colors: ['rgba(102, 187, 106, .5)', 'rgba(21, 101, 192, 0.5)']
        }
    }];

    var layout = {
     title: 'The ''' + states[state] + ''' Delegate Count by %',
     height: 350,
     width: (window.innerwidth / 2),
     font: {
        family: 'Playfair Display, serif',
        size: 20,
        color: "Black"
        },
    };
    Plotly.newPlot(''' + "'" + divName + "'" + ''', data, layout);
    '''
    return js

def plotVoteGraph(bernieVotes, clintonVotes, state, divName):
    js = '''
    var trace1 = {
        x: ''' + convertListToJs([bernieVotes]) + "," + '''
        y: ["Sanders"],
        name: "Bernie Sanders ",
        orientation: 'h',
        type: 'bar',
        marker: {
            color: 'rgba(102, 187, 106, .5)',
            width: 1        }
    };

    var trace2 = {
        x: ''' + convertListToJs([clintonVotes]) +',' + '''
        y: ["Clinton"],
        name: 'Hillary Cinton ',
        orientation: 'h',
        type: 'bar',
        marker: {
            color: "rgba(21, 101, 192, 0.5)",
            width: 1
        }
    };

    var data = [trace1, trace2];

    var layout = {
        title: 'The ''' + states[state] + ''' Popular Vote',
        width: (window.innerwidth / 2),
        height: 350,
        font: {
           family: 'Playfair Display, serif',
           size: 20,
           color: 666
           }
    };

    Plotly.newPlot("''' + divName + '''", data, layout);
    '''
    return js

def plotVotePieChart(bernieVotes, clintonVotes, state, divName):
    values = [bernieVotes, clintonVotes]
    js = '''
    var data = [{
      values: ''' + convertListToJs(values) + ',' + '''
      labels: ['Bernie Sanders ', 'Hillary Clinton '],
      type: 'pie',
      marker :{
        colors: ['rgba(102, 187, 106, .5)', 'rgba(21, 101, 192, 0.5)']
        }
    }];

    var layout = {
     title: 'The ''' + states[state] + ''' Popular Vote by %',
     height: 350,
     width: (window.innerwidth / 2),
     font: {
        family: 'Playfair Display, serif',
        size: 20,
        color: "Black"
        },
    };
    Plotly.newPlot(''' + "'" + divName + "'" + ''', data, layout);
    '''
    return js

def stateNotVoted(state, stateInfo):
    print('<center><h2> The ' + states[state] + " Democratic " + stateInfo["Poll Type"]+'</h2><center>')
    print("<center><p>" + states[state] + " has not voted yet and will be voting on " + stateInfo["Date"] + ". Stay tuned for detailed results.</p></center>")
    style = '''
    <style>
    h1 {
        font-family: 'Playfair Display', serif;
        padding: 25px;
        text-decoration: underline;
    }
    p {
        font-family: 'Playfair Display', serif;
        font-size: 30px;
    }
    h2 {
       font-size:500%;
       font-family: 'Playfair Display', serif;
    }
    </style>
    '''
    print(style)


def displayStatePage(state, masterDict):
    if state in masterDict:
        stateInfo = masterDict[state]
        if stateInfo["Bernie Delegates"] != "" and stateInfo["Clinton Delegates"] != "":
            print('<center><h2> The ' + states[state] + " Democratic " + stateInfo["Poll Type"]+'</h2><center>')
            print('<center><div id="delegate-div">')
            print('<center><h1> The Delegate Count </h1><center>')
            print('''<p><font size='4px' face= 'Playfair Display'>When a presidential candidate wins a state primary they are awarded with a certain number of "delegates". <br> The number of delegates awarded to the candidate is proportional to how well the candidate does <br> in the state's election and the total number of delegates given to the state by the Democratic Party. <br> A candidate needs 2,383 delegates to win the election. </font></p>''')
            print('<div id="delegate-horiz"></div>')
            print('<div id="delegate-pie"></div>')
            print('</div></center>')

            print('<center><div id="pop-div">')
            print('<center><h1> The Popular Vote </h1><center>')
            style = '''
            <style>
            #delegate-pie, #delegate-horiz, #pop-pie, #pop-horiz {
            display: inline-block;
            }
            h1 {
             font-family: 'Playfair Display', serif;
             padding: 25px;
             text-decoration: underline;
             }
             h2 {
            font-size:500%;
            font-family: 'Playfair Display', serif;
            padding: 10px;
            }
            </style>
            '''
            print(style)
            print('''<p><font size='4px' face= 'Playfair Display'>The popular vote is the raw number of people who voted for either candidate. In the Democratic Primary, <br> the total number of delegates a state awards to candidates is proportional to the popular vote. </font></p>''')
            print('<div id="pop-horiz"></div>')
            print('<div id="pop-pie"></div>')
            print('</div></center>')
            bernieDel = int(stateInfo["Bernie Delegates"])
            clintonDel = int(stateInfo["Clinton Delegates"])
            print("<script>")
            print(plotDelgateGraph(bernieDel, clintonDel, state, "delegate-horiz"))
            print(plotDelgatePie(bernieDel, clintonDel, state, "delegate-pie"))
            print("</script>")
            if stateInfo["Bernie Votes"] != "" and stateInfo["Clinton Votes"] != "":
                bernieVotes = int(stateInfo["Bernie Votes"])
                clintonVotes = int(stateInfo["Clinton Votes"])
                print("<script>")
                print(plotVoteGraph(bernieVotes, clintonVotes, state, "pop-horiz"))
                print(plotVotePieChart(bernieVotes, clintonVotes, state, "pop-pie"))
                print("</script>")
            else:
                print('<div id="caucus">' + states[state] + ' holds caucuses as opposed to primaries which means that instead of everysingle individual casting their ballot, voters meet and discuss who they want to nominate.<br> This means that there is no raw popular vote for this state. <br> <br> <br></div>')
        else:
            stateNotVoted(state, stateInfo)

def main():
    masterDict = organize()
    print(HTML_HEADER)
    print(Top_HTML)
    elements = cgi.FieldStorage()
    keys = elements.keys()
    if "state" in keys:
        displayStatePage(str(elements.getvalue("state")), masterDict)
    else:
        displayMap(masterDict)
    print(Bottom_HTML)

main()
