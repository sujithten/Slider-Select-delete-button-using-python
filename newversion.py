# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 17:18:21 2019

@author: Sujith Tenali
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 12:04:40 2019

@author: Sujith Tenali
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May 31 18:18:52 2019

@author: Sujith Tenali
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:55:16 2019

@author: Sujith Tenali
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 29 14:38:04 2019

@author: Sujith Tenali
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 28 12:29:22 2019

@author: Sujith Tenali
"""

import pandas as pd 
import numpy as np

# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
data = pd.read_csv("df_rhythmInfo_32748_1552798645150441.csv") 

epochTime = data['epochTime'] 
#epochTime_n_minus_1 = epochTime.shift(-1,axis = 0) 
data['epochTime_n_minus_1'] = epochTime.shift(+1,axis = 0) 
data= data.drop(columns="RRSec")
data['RRSec'] = ((data.epochTime - data.epochTime_n_minus_1)/1000000)
#data['RRSec'] = RRSec
#data['RRSec'] = data.RRSec.shift(+1,axis=0) 
data['RRSec_n_minus_1'] = data.RRSec.shift(+1,axis=0) 

data['RRSec_n_minus_2'] = data.RRSec.shift(+2,axis=0)
data['RRSec_n_plus_1'] = data.RRSec.shift(-1,axis=0)
data["RRSec_sum"] = data.RRSec_n_plus_1 + data.RRSec
data["RRSec_sum_check"] = data.RRSec_sum - data.RRSec_n_minus_1;
data['beatCharN'] = data['beatChar']
data['beatCharN2'] = data['beatChar']
data['beatCharN3'] = data['beatChar']
data['SerialNo2'] = data['SerialNo']
data['SerialNo3'] = data['SerialNo']
data.drop(['RowNumber', 'HRbpm','HRRateType','HRRhythm','PauseDuration','VentricularEctopics','SymptomID','SymptomName','symptomInputList','epochTime_n_minus_1',], axis=1)
data = data[['beatChar','SerialNo','epochTime','RRSec', 'RRSec_n_minus_1','RRSec_n_plus_1','beatCharN', 'beatCharN2','beatCharN3','SerialNo2','SerialNo3' ]]
data.set_index('beatChar', drop=True, append=False, inplace=True, verify_integrity=False)
#data['RRSec_n_minus_1'] = data.RRSec.shift(-1,axis=0)
green = data.loc["N"] 
red = data.loc["V"]
green = green[['epochTime','RRSec','RRSec_n_plus_1']] 
red = red[['epochTime','RRSec','RRSec_n_plus_1']]
#data.to_csv(r'C:\Users\Sujith Tenali\Desktop\datanew58.csv')
#red.to_csv(r'C:\Users\Sujith Tenali\Desktop\red56.csv')

import io
from bokeh.layouts import row, column
from bokeh.models.widgets import Slider, TextInput,Button
from bokeh.plotting import figure, output_file, show
from bokeh.models import LinearAxis, Range1d
from bokeh.resources import CDN
#from bokeh.palettes import Spectral4
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.models.callbacks import CustomJS
from jinja2 import Template
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.browser import view
from bokeh import events
# output to static HTML file
#output_file("Poincare3.html")
template = Template(
    '''<!DOCTYPE html>
        <html lang="en">
            <head>
            <script src="https://gmousse.github.io/dataframe-js/dist/dataframe.min.js"></script>
           
                <meta charset="utf-8">
                <title>Overview</title>
                {{ resources }}
                {{ script }}
                <style> 
                    .embed-wrapper {
                        display: flex;
                        justify-content: space-evenly;
                    }
                </style>
            </head>
            <body>
                <div>
                    {{ table }}
                </div>                    
                <div class="embed-wrapper">
                    {{ div }}
                </div>
            </body>
        </html>
        ''')

# # configure visual properties on a plot's figure attribute

p1 = figure(tools="pan,box_select,reset,xwheel_pan",x_range=(0.1,1.6),y_range=(0.1,1.6))

n=0
n=0.1

 
S1 = ColumnDataSource(data=data)
S2 = ColumnDataSource(data=dict(RRSec_n_plus_1=[],RRSec=[],epochTime=[],beatChar=[],SerialNo=[],SerialNo2=[],SerialNo3=[]))
S3 = ColumnDataSource(data=green)
S4 = ColumnDataSource(data=red)
S5 = ColumnDataSource(data=data)		   
font_name = "Gill Sans MT"

p1.title.text = "Poincare Plot"
p1.title.text_font_size = "50px"
p1.title.text_color = "#22ACE2"
p1.title.text_font = font_name
	   
p1.xaxis.axis_label = "RRn (seconds)"
p1.xaxis.axis_label_text_font_size = "25px"
# p1.xaxis.axis_label_text_color = "#22ACE2"
p1.xaxis.axis_label_text_font = font_name
p1.xaxis.major_label_text_font = font_name

p1.yaxis.axis_label = "RRn+1 (seconds)"
p1.yaxis.axis_label_text_font_size = "25px"
# p1.yaxis.axis_label_text_color = "#22ACE2"
p1.yaxis.axis_label_text_font = font_name
p1.yaxis.major_label_text_font = font_name

p1.circle(x = 'RRSec',y = 'RRSec_n_plus_1' ,source = S3, size=4, color="green", alpha=0.8, legend="N",muted_color="green", muted_alpha=0.2)
p1.circle(x = 'RRSec',y = 'RRSec_n_plus_1' ,source = S4, size=4, color="red", alpha=0.8 , legend="V", muted_color="red", muted_alpha=0.2)
p1.circle(x = 'RRSec',y = 'RRSec_n_plus_1' ,source = S2, size=4, color="blue", alpha=0.8,legend="noise", muted_color="blue", muted_alpha=0.2) 
# show the results
#select_tool = p1.select(dict(type=BoxSelectTool))[0]

S2.selected.js_on_change('indices', CustomJS(args=dict(S1=S1, S2=S2, S5=S5), code="""
    const inds = S2.selected.indices;
    var d = S2.data;
    var d2 = S1.data;
    var d5 = S5.data;

    if (inds.length == 0)
        return;

    
    for (var i = 0; i < inds.length; i++)
        {
        console.log(d['SerialNo2'][inds[i]]);
        console.log(d5['beatCharN3'][d['SerialNo2'][inds[i]]]);
        d5['SerialNo2'][d['SerialNo2'][inds[i]]] = 'NaN';
        } 

    
    S1.change.emit();
    S2.change.emit();
    S5.change.emit();
"""))

slider = Slider(start=0.0, end=0.5,value=0.0, step=0.1, title="noise%")

callback = CustomJS(args=dict(S1=S1,S2=S2,S5=S5), code="""
    
    var n = cb_obj.value;
    console.log(n);
    var data1 = S1.data;
    var data2 = S2.data;
    var data5 = S5.data;
    
    
    console.log(data1.RRSec.length);
    data2.RRSec_n_plus_1 = [];
          data2.RRSec = [];
          data2.epochTime = [];
          data2.beatChar = [];
          data2.SerialNo = [];
          data2.SerialNo2 = [];
          data2.SerialNo3 = [];
    for(var i = 0; i < data5.RRSec.length; i++)
    {
          data5['beatCharN'][i] = data5['beatCharN2'][i];
       if(Math.abs(data5.RRSec_n_plus_1[i] + data5.RRSec[i] - data5.RRSec_n_minus_1[i]) <= n)
       {
          data5['SerialNo'][i] = 'NaN';
          data2.RRSec_n_plus_1.push(data5['RRSec_n_plus_1'][i]);
          data2.RRSec.push(data5['RRSec'][i]);
          data2.epochTime.push(data5['epochTime'][i]); 
          data2.beatChar.push(data5['beatChar'][i]);
          data2.SerialNo.push(data5['SerialNo'][i]);
          data2.SerialNo2.push(data5['SerialNo2'][i]);
          data2.SerialNo3.push(data5['SerialNo3'][i]);
         }
    }
    S1.change.emit();
    S2.change.emit();
    S5.change.emit();
""")
slider = Slider(start=0.0, end=0.5,value=0.0, step=0.1, title="noise%", callback = callback)
slider.js_on_change('value', callback)
callback.args["slider"] = slider

callback2 = CustomJS(args=dict(S1=S1,S2=S2,S3=S3,S4=S4,S5=S5), code = """
                     
                     var data1 = S1.data;
                     var data2 = S2.data;
                     var data3 = S3.data;
                     var data4 = S4.data;
                     var data5 = S5.data;
                    
                     
                           data2.RRSec_n_plus_1 = [];
                           data2.RRSec = [];
                           data2.epochTime = [];
                           data2.beatChar = [];
                           data2.SerialNo = [];
                           data2.SerialNo2 = [];
                           data2.SerialNo3 = [];
                     
                     
                     data3.RRSec_n_plus_1 = [];
                     data3.RRSec = [];
                     data3.epochTime = [];
                     data3.beatChar = [];
                     
                     
                     
                     data4.RRSec_n_plus_1 = [];
                     data4.RRSec = [];
                     data4.epochTime = [];
                     data4.beatChar = [];
                     
                     
                        data5.RRSec = [];
                        data5.epochTime = [];
                        data5.beatChar = [];
                        data5.beatCharN = [];
                        data5.beatCharN2 = [];
                        data5.beatCharN3 = [];
                        data5.SerialNo2 = [];
                        data5.SerialNo3 = [];
                        data5.RRSec_n_plus_1 = [];
                        data5.RRSec_n_minus_1 = [];
                     
                    
                     for(var i=0; i < data5.SerialNo.length; i++)
                     {
                        if(data5.SerialNo[i] != 'NaN')
                        {
                        data5.RRSec.push(data1.RRSec[data5.SerialNo[i]]);
                        data5.epochTime.push(data1.epochTime[data5.SerialNo[i]]);
                        data5.beatChar.push(data1.beatChar[data5.SerialNo[i]]);
                        data5.beatCharN.push(data1.beatCharN[data5.SerialNo[i]]);
                        data5.beatCharN2.push(data1.beatCharN2[data5.SerialNo[i]]);
                        data5.beatCharN3.push(data1.beatCharN3[data5.SerialNo[i]]);
                        data5.SerialNo3.push(data1.SerialNo3[data5.SerialNo[i]]);
                        }
                     }
                        
                        
                        for( var i = 0; i < data5.SerialNo.length; i++)
                        { 
                        if ( data5.SerialNo[i] === 'NaN') 
                           {
                          data5.SerialNo.splice(i, 1);
                           i--;
                            }
                        }
                        
                        
                        
                       for(var i =0; i < data5.RRSec.length; i++)
                       {
                         data5.SerialNo2[i] = i;
                       }
                        
                    
                       for(var i =0; i < data5.RRSec.length-1; i++)
                       {
                        data5.RRSec_n_plus_1[i] = data5.RRSec[i+1];
                       
                       }
                       
                       for(var i =1; i < data5.RRSec.length; i++)
                       {
                        data5.RRSec_n_minus_1[i] = data5.RRSec[i-1];
                       
                       }
                       
                        data5.RRSec_n_minus_1[0] = 'NaN';                       
                        data5.RRSec_n_plus_1.push('NaN');
                        
                        console.log(data5.SerialNo.length);
                        console.log(data5.RRSec.length);
                       
                        
                      for(var i = 0; i < data5.RRSec.length; i++)
                      {
                        
                         if(data5.beatChar[i]=='V')
                        {
                        data4.RRSec_n_plus_1.push(data5.RRSec_n_plus_1[i]);
                        data4.epochTime.push(data5.epochTime[i]);
                        data4.beatChar.push(data5.beatChar[i]);
                        
                        data4.RRSec.push(data5.RRSec[i]);
                        }
                        
                        if(data5.beatChar[i]=='N')
                        {
                        data3.RRSec_n_plus_1.push(data5.RRSec_n_plus_1[i]);
                        data3.epochTime.push(data5.epochTime[i]);
                        data3.beatChar.push(data5.beatChar[i]);
                        
                        data3.RRSec.push(data5.RRSec[i]);
                        }
                      }
                        
                        
                       
                     
                        
                     
                     
                     
                    S3.change.emit();
                    S4.change.emit();
                    S2.change.emit();
                    S5.change.emit();
                     
                     """)



button = Button(label="Delete entire noise (can't be undone)", button_type="success",callback = callback2)
button.js_on_event(events.ButtonClick, )


callback3 = CustomJS(args=dict(S1=S1,S2=S2,S3=S3,S4=S4,S5=S5,s = slider), code = """
                     
                     var data1 = S1.data;
                     var data2 = S2.data;
                     var data3 = S3.data;
                     var data4 = S4.data;
                     var data5 = S5.data;
                    
                     
                           data2.RRSec_n_plus_1 = [];
                           data2.RRSec = [];
                           data2.epochTime = [];
                           data2.beatChar = [];
                           data2.SerialNo = [];
                           data2.SerialNo2 = [];
                           data2.SerialNo3 = [];
                     
                     data3.RRSec_n_plus_1 = [];
                     data3.RRSec = [];
                     data3.epochTime = [];
                     data3.beatChar = [];
                    
                     
                     
                     data4.RRSec_n_plus_1 = [];
                     data4.RRSec = [];
                     data4.epochTime = [];
                     data4.beatChar = [];
                     
                     
                        data5.RRSec = [];
                        data5.epochTime = [];
                        data5.beatChar = [];
                        data5.beatCharN = [];
                        data5.beatCharN2 = [];
                        data5.beatCharN3 = [];
                        data5.SerialNo = [];
                        data5.RRSec_n_minus_1 = [];
                        data5.RRSec_n_plus_1 = [];
                     
                     
                     
                     for(var i=0; i < data5.SerialNo2.length; i++)
                     {
                        if(data5.SerialNo2[i] != 'NaN')
                        {
                        //console.log(data1.RRSec[data5.SerialNo3[data5.SerialNo2[i]]]);
                        data5.RRSec.push(data1.RRSec[data5.SerialNo3[data5.SerialNo2[i]]]);
                        data5.epochTime.push(data1.epochTime[data5.SerialNo3[data5.SerialNo2[i]]]);
                        data5.beatChar.push(data1.beatChar[data5.SerialNo3[data5.SerialNo2[i]]]);
                        data5.beatCharN.push(data1.beatCharN[data5.SerialNo3[data5.SerialNo2[i]]]);
                        data5.beatCharN2.push(data1.beatCharN2[data5.SerialNo3[data5.SerialNo2[i]]]);
                        data5.beatCharN3.push(data1.beatCharN3[data5.SerialNo3[data5.SerialNo2[i]]]);
                        data5.SerialNo.push(data1.SerialNo3[data5.SerialNo3[data5.SerialNo2[i]]]);
                        }
                     }
                        
                        data5.SerialNo3 = [];
                        data5.SerialNo2 = [];
                        
                       for( var i = 0; i < data5.RRSec.length; i++)
                        { 
                          data5.SerialNo2[i] = i;
                        }
                           
                         
                            
                           for( var i = 0; i < data5.SerialNo2.length; i++)
                           {
                            data5.SerialNo3.push(data5.SerialNo[i]);
                           }
                           
                           
                           
                           
                        console.log(data5.SerialNo2.length);
                        console.log(data5.RRSec.length);
                        
                    
                       for(var i =0; i < data5.RRSec.length-1; i++)
                       {
                        data5.RRSec_n_plus_1[i] = data5.RRSec[i+1];
                       
                       }
                       
                        for(var i =1; i < data5.RRSec.length; i++)
                       {
                        data5.RRSec_n_minus_1[i] = data5.RRSec[i-1];
                       
                       }
                       
                        data5.RRSec_n_minus_1[0] = 'NaN';                       
                        data5.RRSec_n_plus_1.push('NaN');
                        
                        
                        
                        
                      for(var i = 0; i < data5.RRSec.length; i++)
                      {
                        
                         if(data5.beatChar[i]=='V')
                        {
                        data4.RRSec_n_plus_1.push(data5.RRSec_n_plus_1[i]);
                        data4.epochTime.push(data5.epochTime[i]);
                        data4.beatChar.push(data5.beatChar[i]);
                        data4.RRSec.push(data5.RRSec[i]);
                        }
                        
                        if(data5.beatChar[i]=='N')
                        {
                        data3.RRSec_n_plus_1.push(data5.RRSec_n_plus_1[i]);
                        data3.epochTime.push(data5.epochTime[i]);
                        data3.beatChar.push(data5.beatChar[i]);
                        
                        data3.RRSec.push(data5.RRSec[i]);
                        }
                      }
                        
                        n = s.value;
                        console.log(n);
                        
                        for(var i = 0; i < data5.RRSec.length; i++)
                        {
                         data5['beatCharN'][i] = data5['beatCharN2'][i];
                         if(Math.abs(data5.RRSec_n_plus_1[i] + data5.RRSec[i] - data5.RRSec_n_minus_1[i]) <= n)
                         {
                           data5['SerialNo'][i] = 'NaN';
                           data2.RRSec_n_plus_1.push(data5['RRSec_n_plus_1'][i]);
                           data2.RRSec.push(data5['RRSec'][i]);
                           data2.epochTime.push(data5['epochTime'][i]); 
                           data2.beatChar.push(data5['beatChar'][i]);
                           data2.SerialNo.push(data5['SerialNo'][i]);
                           data2.SerialNo2.push(data5['SerialNo2'][i]);
                           data2.SerialNo3.push(data5['SerialNo3'][i]);
                          }
                         }
                        
                       
                     
                        
                     
                     
                     
                    S3.change.emit();
                    S4.change.emit();
                    S2.change.emit();
                    S5.change.emit();
                     
                     """)
button2 = Button(label="Delete Selected (can't be undone)", button_type="success",callback = callback3)
button.js_on_event(events.ButtonClick, )

#slider.js_on_change('value', callback)   
p1.legend.location = "top_right"
p1.legend.click_policy="hide"
layout = row(p1,column(slider,button,button2))
script, div = components(layout)
resources = INLINE.render()
filename = 'embed_multiple.html'
    
html = template.render(resources=resources,
                       script=script,
                        div=div)

with io.open(filename, mode='w', encoding='utf-8') as f:
    f.write(html)

view(filename)


#show(layout)


