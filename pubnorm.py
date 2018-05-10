"""
Project: pubsne
Authors:
	kceades
"""

# imports from files I wrote
import snmc
import snetools
import tools
import creator

# imports from standard packages
import pickle
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
import os



class Normalizer(object):
	"""
	Normalizer class that will read in the public supernova data and the
	analysis models that have been created and then use it to rephase the sne
	and test for r_v variations.
	"""
	def __init__(self,load_on_start=True):
		"""
		Constructor

		:load_on_start: (bool) whether or not to load the data when the object
						is first instantiated
		"""
		self.data_dir = os.getcwd() + '/pickleddata'

		if load_on_start:
			self.load_data()

	def load_data(self):
		"""
		Loads the public supernovas and the analysis models into our class.
		"""
		models_name = os.path.join(self.data_dir,'Public_Objects.p')
		models_file = open(models_name,'rb')
		self.models = pickle.load(models_file)
		models_file.close()

		sne_name = os.path.join(self.data_dir,'Public_Novas_Phase.p')
		sne_file = open(sne_name,'rb')
		self.novas = pickle.load(sne_file)
		sne_file.close()

	def rephase(self):
		"""
		Rephases the supernovae based on using the non-outliers to the models
		built to train machine learning regressors and then use those regressors
		to re-fit the outliers for new phases. These new phases are then used to
		build up a new dataset and train new models.
		"""
		training = []
		training_phases = []
		phases = [phase for phase in self.novas]
		for phase in phases:
			outliers = snetools.find_outliers(self.novas[phase],'dust_flux'\
				,self.models['emFA'][phase],1.0)
			training.extend([self.group_bins(spec.signal['dust_flux']) for \
				spec in self.novas[phase] if spec.key not in outliers])
			training_phases.extend([spec.phase for spec in self.novas[phase] \
				if spec.key not in outliers])

		forest = RandomForestRegressor(n_estimators=100)
		forest.fit(training,training_phases)
		net = MLPRegressor()
		net.fit(training,training_phases)

		phase_pairs = []
		final_novas = {phase:[] for phase in self.novas}
		for phase in self.novas:
			outliers = snetools.find_outliers(self.novas[phase],'dust_flux'\
				,self.models['emFA'][phase],1.0)
			for spec in self.novas[phase]:
				if spec.key in outliers:
					grouped = self.group_bins(spec.signal['dust_flux'])
					pred1 = forest.predict([grouped])[0]
					pred2 = net.predict([grouped])[0]
					new_phase = tools.closest_match((pred1+pred2)/2,phases)
					final_novas[new_phase].append(spec)
				else:
					final_novas[phase].append(spec)

		self.create_new_data(final_novas)

	def create_new_data(self,phase_dict):
		"""
		Creates a new data set that is stored for use based on the new phase
		dictionary created in the self.rephase method

		:phase_dict: (dict) output of the self.rephase method
		"""
		sne_name = os.path.join(self.data_dir,'Public_Novas_Phase_FIXED.p')
		sne_file = open(sne_name,'wb')
		pickle.dump(phase_dict,sne_file)
		sne_file.close()

		pars = creator.Parameters()
		a_dict = {mode:{phase:None for phase in pars.phases} for mode in \
			pars.model_modes}
		coeff_dict = {mode:{phase:None for phase in pars.phases} for mode in \
			pars.model_modes}
		for mode in pars.model_modes:
			for phase in pars.phases:
				a_obj,coeffs = snetools.create_model(phase_dict[phase]\
					,'dust_flux',mode,pars.num_components,pars.reject_sigma)
				a_dict[mode][phase] = a_obj
				coeff_dict[mode][phase] = coeffs

		obj_name = os.path.join(self.data_dir,'Public_Objects_FIXED.p')
		obj_file = open(obj_name,'wb')
		pickle.dump(a_dict,obj_file)
		obj_file.close()

		coeff_name = os.path.join(self.data_dir,'Public_Coeffs_FIXED.p')
		coeff_file = open(coeff_name,'wb')
		pickle.dump(coeff_dict,coeff_file)
		coeff_file.close()

	def group_bins(self,signal,grouping=20):
		"""
		Groups the signal into a smaller number of features to be used with
		the machine learning algorithms.

		:signal: (np array) fluxes of the input signal
		:grouping: (int) the number of bins to group together

		:returns: (np array) rebinned signal
		"""
		return [sum(signal[i:i+20]) for i in range(0,len(signal),20)]

if __name__=='__main__':
	n = Normalizer(False)