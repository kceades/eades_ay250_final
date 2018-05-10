"""
Project: pubsne
Authors:
	kceades
"""

# imports from modules I wrote
import scraper
import snmc
import creator
import base
import pubnorm

# imports from standard modules
import os
import numpy as np
from flask import Flask,request,redirect,url_for,render_template,send_from_directory

UPLOAD_FOLDER = './pubcsv'

app = Flask(__name__,static_folder='./results')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.isdir(UPLOAD_FOLDER):
	os.makedirs(UPLOAD_FOLDER)

@app.route('/',methods=['GET'])
def index():
	""" Method to handle the home page routing. """
	return render_template('index.html')

@app.route('/uploadcsv', methods=['GET','POST'])
def uploadcsv():
	""" Method to handle the uploadcsv page routing. """
	if request.method == 'GET':
		return render_template('uploadcsv.html')
	else:
		file = request.files['file']
		try:
			if file.filename[-4:] == '.csv':
				path = os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
				file.save(path)
				return render_template('uploadcsv_success.html'\
					,file_name=file.filename)
			else:
				return render_template('uploadcsv_failure.html')
		except:
			return render_template('uploadcsv_failure.html')

@app.route('/datacreation',methods=['GET'])
def datacreation():
	""" Method to handle the datacreation routing. """
	return render_template('datacreation.html')

@app.route('/run_scraper',methods=['POST'])
def run_scraper():
	""" Method to handle running the scraper. """
	path = os.path.join(app.config['UPLOAD_FOLDER'],request.form['filename'])
	if not (os.path.isfile(path) and request.form['filename'][-4:]=='.csv'):
		return render_template('scraper_failure.html')
	else:
		print('Starting up the scraper: check here for progress.')
		scraper_object = scraper.Scraper()
		scraper_object.run(request.form['filename'])
		return render_template('scraper_success.html')

@app.route('/run_creator',methods=['POST'])
def run_creator():
	""" Method to handle running the data creator. """
	try:
		pars = snmc.Parameters()
		pars.re_start = int(request.form['wv_start'])
		pars.re_end = int(request.form['wv_end'])
		pars.re_step = int(request.form['wv_step'])
		pars.wvs = np.arange(pars.re_start,pars.re_end+pars.re_step,pars.re_step)\
			.astype(float)
		pars.num_points = len(pars.wvs)
		phase_start = int(request.form['phase_start'])
		phase_end = int(request.form['phase_end'])
		phase_step = int(request.form['phase_step'])
		pars.phases = np.arange(phase_start,phase_end+phase_step,phase_step)
		pars.num_phases = len(pars.phases)
		pars.day_cut = phase_step/2.0

		data_gen_object = creator.DataGenerator()
		data_gen_object.run_everything_individual('Public')
		
		norm_object = pubnorm.Normalizer()
		norm_object.rephase()
		return render_template('creator_success.html')
	except:
		return render_template('creator_failure.html')

@app.route('/base',methods=['POST'])
def base():
	""" Method for running the base script, which creates the images. """
	try:
		base.create_all_final_demo()
		return render_template('base_success.html')
	except:
		return render_template('base_failure.html')



@app.route('/viewing',methods=['GET'])
def viewing():
	""" Method to handle the viewing page. """
	return render_template('viewing.html')

@app.route('/view_model',methods=['POST'])
def view_model():
	""" Method to handle post requests to view the model components. """
	try:
		source = request.form['source']
		mode = request.form['mode']
		phase = request.form['phase']
		folder = './results/images_{}/{}/{}/comps/'.format(mode,source,phase)
		files = [folder + f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
		files = [f[10:] for f in files]
		files.sort(key=lambda x:int(x.split('_')[-1].split('.')[0]))
		return render_template('model_success.html',source=source,mode=mode,phase=phase,images=files)
	except:
		return render_template('model_failure.html')

@app.route('/view_var',methods=['POST'])
def view_var():
	""" Method to handle post requests to view the explained variance curves. """
	try:
		mode = request.form['mode']
		phase = request.form['phase']
		folder = './results/variance/{}/{}/'.format(mode,phase)
		files = [folder + f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
		files = [f[10:] for f in files]
		return render_template('var_success.html',mode=mode,phase=phase,images=files)
	except:
		return render_template('var_failure.html')

# @app.route('/view_gallery',methods=['POST'])
# def view_gallery():
# 	""" Method to handle post requests to view the gallery of fits. """
# 	try:
# 		source = request.form['source']
# 		mode = request.form['mode']
# 		phase = request.form['phase']
# 		folder = './results/images_{}/{}/{}/comps/'.format(mode,source,phase)
# 		files = [folder + f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
# 		files = [f[10:] for f in files]
# 		files.sort(key=lambda x:int(x.split('_')[-1].split('.')[0]))
# 		return render_template('model_success.html',source=source,mode=mode,phase=phase,images=files)
# 	except:
# 		return render_template('model_failure.html')


if __name__ == '__main__':
	app.run()