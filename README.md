# eades_ay250_final
Final Project for the AY250 Class

The first commit that isn't just the initialization of the REPO (so the second commit) is the one with all the previous work I had done on this project before the final project. All commits passed that point will be new commits with the code I wrote for the final project.

# IMPORTANT NOTE

Trying to start up the app, download all the data and run the processing scripts would take on the order of an hour or so if no issues arise. Just an FYI before I continue here.

# PubSNE Project Description

The basic idea behind the overall research project is to develop a model of supernova spectra as a function of phase (days since explosion) that minimizes the variance between supernovae. This model could be taken further to use in simulating synthetic spectra, getting estimates of the Hubble constant, looking for R_V variations in public supernovae, and in the shiny lights better constraining parameters of the universe.

Granted, there is still a lot of work to do on it and it is still in a pretty rough state at the moment.

# Current PubSNE Project Status

While there is a lot of work to be done, here is the general idea of what has been done.

1. A scraper function that reads in public domain supernovae data from sne.space, an online repository where astronomers in theory upload their data.
2. A basic data cleaning and processing pipeline: to be honest, the data from sne.space is all over the map. Some of it is gorgeous and others is horrible. I've seen my fair share of zero vectors in the repository. Also, you can try to do things like only select data that has been host subtracted, deredshifted, normalized, and in standard units...and you will still find spectra that vary over roughly 30 orders of magnitude in signal strength with clear signs of not being processed whatsoever beyond being converted into a spectrum in the first place. So my mini-pipeline tries to normalize and standardize the spectra to have some measure of coherence, as well as to remove some of the effects that are still there.
3. Using sci-kit learn tools to build a model of essentially eigenvectors using either Expectation Maximization Factor Analysis or Principle Component Analysis. The results of the this model are what are the most useful in future projects that will use this data, as explained a bit more below.
4. Running some analysis on how well the models do in explaining variance, how close the residual is to white noise, and how well the models fit given individual supernovae. Lots of graphs.

# Final Project (for AY250) Description

For the final project, I wanted to write a Flask app to make it easier for someone novice to the project or to coding to manipulate parameters and look at the results. I also wanted to add in a machine learning component with predicting phases of supernova given a spectrum (specifically to use that to re-phase the public supernova that I suspect are at the wrong phases).

For the screencapture, I am including screenshots of the website in the repository. If that isn't sufficient, please let me know about a meeting. The screencaptures I included were:
1. The index page
2. The upload CSV page
3. The run scripts page
4. The view results page
5. An example of one of the error pages (specifically when no csv is selected)
6. An example of one of the success pages (specifically after running creator.py on the run scripts page)
7. The results of one of the explained variance queries (note that they all do really well because the model is trained on the data that it is being applied to: see the disclaimers)
8. The results of one of the view components queries
9. One of the gallery pages (that is currently not accessible via the site, but is created when the scripts are run and can be pulled up by going to the directory as detailed on the site)
10. One of my old explained variance curves showing how things get interesting when public models are compared to Factory models and the two are used to fit each other's data (also not accessible via the site, nor created when running these scripts explicitly since I didn't upload the factory data or tool scripts)

# Status

I did manage to create a working Flask app with some nice features to it, but there remains work to be done. Most glaringly, I didn't get the gallery page to work yet (my base script creates hard-coded html files, which I was trying to convert to a form Flask likes and succeeded in some cases but not for the gallery yet).

On the machine learning side, all the data that is under the source name of "Public_FIXED" when you create the data uses some sklearn tools. Namely, the (airquotes) fixed nomenclature means that it was rephased. So I took the supernova with their quoted phases coming out of sne.space, created a model, took the outliers and rephased them, then created new models with the re-binned supernovae. This isn't everything that I wanted to do with the machine learning, but it's a start. Also, as noted below in the disclaimers, the really interesting part comes in testing this machine learned "phaser" on outside datasets such as the "Factory" data (my group's dataset), but I'm not allowed to release that data for now.

Overall, I'm fairly pleased with how the site turned out, especially given the endless problems I ran into converting my code into something I could link up with a Flask app in a reasonable fashion. Converting the code took quite a bit of time even though at the end of the day it probably doesn't look like much.

# Important Disclaimer(s)

First and foremost, the data is TOO LARGE to run in a reasonable amount of time for a website. The website was really just meant to make things easier to work with and change, but when running the scraper or the base scripts for example, the page will lock up for a significant amount of time (on the order of tens of minutes). So be warned. If you want, you could download a smaller CSV file from sne.space (where all the data here was obtained) and input it to the system to play around with things.

Second, a lot of the code may look unnecessary or overworked, but that is likely due to me leaving out the "Factory" dataset, which is private to my research group. Therefore, the site isn't really that impressive as is since it doesn't do the cross comparisons. An example of this would be looking at residuals and explained variance curves when a model is trained with the Factory data and applied to the public data. This in particular is super valuable because it gives evidence as to whether the Factory data set has a good enough representation of the feature space of supernovae.

Lastly, I have tried a lot of different techniques on the public dataset, but it still is quite all-over-the place with some showing clear signs of host contamination, some showing possible mis-calculated redshifts, and others being clearly quoted at the wrong phase. These are just a few of the issues I dealt with in working with this data, and despite my varied and numerous attempts, signs of these linger, very strongly in some cases.

# Using the Flask App

The steps to doing so are as follows:

1. Clone or fork this repository
2. cd to the folder where it is forked
3. Open a Python terminal and run the "pubapp.py" script.
4. Go to the localhost in a browser as directed in the terminal
5. Follow the directions on the site, basically walking through it in order of the links from left to right on the navigation bar. On the "run scripts" page, be sure to follow the order of running the scripts from the first one on the page to the third.
