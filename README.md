### README

 <li>One visualization must include some quantitative data</li>


[Viz 1](http://info-4602-5602.github.io/project-1-mozilla-5602_project1_julia_jessica_jack_mike/sankey/sankey-savviness.html)

[Viz 2](http://info-4602-5602.github.io/project-1-mozilla-5602_project1_julia_jessica_jack_mike/map_n_pie/world-wide-feelings.html)

<h2>Is Ignorance Bliss?: How technological savviness shapes feelings about a more connected future</h2>

<h2>Introduction</h2>
In August 2017, Mozilla published a survey that aimed to take stock of the globe’s attitudes toward a more connected future. As more and more connected devices are invented, purchased, and added to the world-wide network, many different opinions, emotions and perspectives have arisen, especially concerning privacy and security. One interesting question is how technological savviness may influence feelings and attitudes toward a more connected future, or in other words: is ignorance bliss? 
This connection was the central focus of this investigation in which we designed two interactive visualizations to illustrate data from Mozilla’s survey, publically available on their website. These visual tools allow a user to explore insights into the ways fearful or excited feelings and technological savviness may be connected and how they vary across the globe.

</h2>Team Roles: </h2>
Mike: Designer/coder

Jack: Designer/coder
Reorganized and reformatted dataset into more efficient format for parsing and generating plots
Wrote code for holoviews Sankey plot, including custom Bokeh colormap and tooltip.
Produced several iterations of the Sankey plot.
Organized holoviews-generated html files to be hosted on github.io for ease of viewing.

Jess: Designer/writer
Sketched three prototype visualizations
Modeled several iterations of maps with pie charts in Tableau
Wrote and edited content for Readme
Gave feedback on iterations of visualizations

Julia: Designer/writer
Sketched out three prototype visualizations.
Modeled a map visualization in Tableau 
Gave feedback on iterations of visualizations
Wrote and edited content for Readme


</h2>Design Process:</h2>
After reviewing the dataset and article, we decided upon a research question: does someone’s technological savviness influence their feelings and attitudes towards the future of a connected world? We then identified some tasks that a potential user of the visualizations would use to explore this research question.
We individually brainstormed two to three visualizations on paper, ranging from safe and realistic concepts to ambitious ones. 
We came together as a group to discuss our visualizations and picked three that we thought might be best for our objective and given our limitations.  We also identified Bokeh as both a powerful and straightforward platform to construct our visualization designs.
We prototyped these visualizations, with Jack working on a Sankey visualization, Mike working on a ridge plot, and Julia and Jess testing a variety of map visualizations in Tableau. 
Discussing our prototypes, we decided to pursue the Sankey and map visualizations. We felt that both the Sankey plot and the map visualization provided for more interactivity than the ridge plot and therefore would generate more insights between multiple attributes. 
Julia and Jess wrote out specific details describing the attributes and interactive features that needed to be represented in these two visualizations, and Jack and Mike worked on further developing the code for them in Bokeh. 
We met to discuss progress on the visualizations and made adjustments to design elements. At this meeting we also continued to work on a more thorough written representation of what each visualization incorporates.
Jack and Mike finalized the visualizations while Jess and Julia updated visualizations descriptions and other information to be included in the Readme document.

</h2>Sankey Visualization</h2>
Attributes: Our Sankey visualization incorporates both categorical and quantitative attributes to examine how technological savviness may affect people’s feelings regarding connectivity in the future. To do this, we compared participant’s self-declared category of technological savviness to their responses to the question: “Thinking about a future in which so much of your world is connected to the internet leaves you feeling:”  and also what participants rank as their highest priority when purchasing a new device. Technological savviness is represented by a sequential color ramp of blues, with darker shades representing more savviness. The number of responses is represented by the width of the bands. A wider band indicates a larger amount of responses from that technological savviness category for that response. Technological savviness is an ordinal attribute, future feelings and purchase considerations are categorical attributes, and the number of responses is a quantitative attribute.
Interactivity: Users can hover over a specific band to get more information in a tooltip box, which displays the percentage of people in that technological savviness category that chose that specific response. Hovering also darkens the band and makes it pop out against the context of the rest. The user can use a drop-down menu to toggle the right side column from the future feeling responses to the considerations that participants prioritize when purchasing a new connected device. 
Perceptual Concepts: Our design leverages the perceptual mechanisms of both gists and Gestalt principles. By linking the size of bands with the percentage of respondents, users can make ensemble judgements about the data upon first glance. For example, they may be able to discern that a majority of respondents fell into two tech savviness categories: “Technically Savvy” and “Average User”. The Gestalt phenomena of similarity is present in our use of color categorization for each tech savviness level. This lends itself to the task of discovering how respondents of a specific tech savviness level answered the question represented in the right column. Users can easily see which color corresponds to the level they are interested in and hover over each band to get more information about specific responses.


</h2>Map Visualization</h2>
Attributes: The map visualization utilizes geospatial data to allow users to explore the potential relationships between technological savviness and feelings about the future of connectivity, as well as how those metrics vary across the globe. The primary data of focus of this visualization are participants’ responses to the question: “Thinking about a future in which so much of your world is connected to the internet leaves you feeling:” Countries are filled with a shade of orange illustrating the percent of the participants who responded that they were “scared as hell”. Those outliers with percentages above 20% were colored the same shade at 20% to maintain the visual contrast of the majority of the data range. An accompanying pie chart illustrates the ratio of all responses to this question for that country hovered over. This pie chart will display if there is a complete set of data provided for that country for that question. The five responses are illustrated as wedges of different colors, set from green as positive outlooks to red as fearful ones. The colors for technological savviness match those in the Sankey visualization. Additionally, the user can toggle the pie chart to display that country’s ratio of participants’ technological savviness categories. Technological savviness is an ordinal attribute, future feelings are categorical attributes, country is a geospatial attribute, and the number of participants and responses are quantitative attributes.  
Interactivity: Hovering over a country will display the percentage of participants “scared as hell” and the country name. It will also update the pie chart, if sufficient data exist for that country. Hovering over a pie chart slice will show the number of participants in a tooltip box. Users can toggle the pie chart data to illustrate technological savviness categories or future feelings. This feature lets the user hover over countries of certain fear levels and see the breakdown of all of the responses, or the technological savviness profile of that country in the pie chart.
Perceptual Concepts: This map utilizes a color scheme to fill countries for fear percentage in a way that allows a viewer to get the gist of where there is relatively more or less fear about a connected future, with higher fear areas contrasting dark against the lighter shades and the white background. In this way those countries also pop out at first glance and bring the viewer’s attention to those areas of interest to then interact with and learn more about. The pie chart’s divergent color scheme for feelings uses semantic color associations of greens being positive, yellow being cautious, and red being alarming. 
