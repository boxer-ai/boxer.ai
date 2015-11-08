This hack uses cortical.io to analyze Yelp's academic dataset.

This requires a cortical.io API key which you can get for free at http://www.cortical.io and Yelp's academic dataset which you can get here: https://www.yelp.com/academic_dataset.

Put your cortical.io API key in a file named "cortical.io.key"

Download and unzip Yelp's academic dataset so you have a file named "yelp_academic_dataset.json"

Running:

python hack.py

will analyze the reviews of 100 randomly chosen users.  Each review is passed to cortical.io's API to get an SDR and then the SDR is sent back to cortical.io for a list of terms related to that SDR.  The first term for each SDR is used to build a dictionary of terms.

Checkout Artem's hack to determine the new information a user review contributes to a business's cortical.io finger print here:

http://nbviewer.ipython.org/url/artem.avdacev.com/stuff/yelp_data_numenta.ipynb

or look at the file yelp_data_numenta.ipynb.webarchive


