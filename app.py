from flask import Flask, render_template, request
import requests
import pickle
import jsonify

app = Flask(__name__, static_url_path='/static', static_folder="static")
model = pickle.load(open('random_forest_regressor_model.pkl', 'rb'))

@app.route('/', methods=['GET'])
def Home():
	return render_template('index.html')


# standard_to = StandardScaler()
@app.route('/predict', methods=['POST'])
def predict():
	if request.method == 'POST':
		Symboling = int(request.form['Symboling'])
		Car_Length = float(request.form['Car_Length'])
		Car_Width = float(request.form['Car_Width'])
		Curbweight = float(request.form['curbweight'])
		Engine_Size = int(request.form['enginesize'])
		Bore_Ratio = float(request.form['boreratio'])
		Horse_Power = float(request.form['horsepower'])
		City_Mpg = float(request.form['citympg'])
		Highway_Mpg = float(request.form['highwaympg'])
		
		fueltype_gas = request.form['fueltype_gas']
		if fueltype_gas=='Gas':
			fueltype_gas = 1
		else:
			fueltype_gas = 0

		aspiration_turbo = request.form['aspiration_turbo']
		if aspiration_turbo == "Turbo":
			aspiration_turbo = 1
		else:
			aspiration_turbo = 0

		carbody_hardtop = 0
		carbody_hatchback = 0
		carbody_sedan = 0
		carbody_wagon = 0

		carbody_types = request.form['carbody_types']
		if carbody_types == 'Hardtop':
			carbody_hardtop = 1
		elif carbody_types == 'HatchBack':
			carbody_hatchback = 1
		elif carbody_types == 'Sedan':
			carbody_sedan = 1
		elif carbody_types == 'Wagon':
			carbody_wagon = 1
		else: # means it is Convertible
			pass

		
		enginetype_ohcv = 0  
		enginetype_ohc = 0 
		enginetype_l=0 
		enginetype_rotor=0 
		enginetype_ohcf=0 
		enginetype_dohcv=0

		enginetype_select = request.form['enginetype_select']
		if enginetype_select=="dohcv":
			enginetype_dohcv=1
		elif enginetype_select=="l":
			enginetype_l=1
		elif enginetype_select=="ohc":
			enginetype_ohc=1
		elif enginetype_select=="ohcf":
			enginetype_ohcf=1
		elif enginetype_select=="ohcv":
			enginetype_ohcv=1
		elif enginetype_select=="rotor":
			enginetype_rotor=1
		else: 				# enginetype_dohc = 1 means all other type are 0
			pass


		# cylindernumber_eight = 1 means all the other are 0
		cylindernumber_five = 0
		cylindernumber_four = 0
		cylindernumber_six = 0
		cylindernumber_three = 0
		cylindernumber_twelve = 0
		cylindernumber_two = 0

		cylindernumber_select = int(request.form['cylindernumber_select'])
		if cylindernumber_select==2:
			cylindernumber_two=1
		elif cylindernumber_select==3:
			cylindernumber_three=1
		elif cylindernumber_select==4:
			cylindernumber_four=1
		elif cylindernumber_select==6:
			cylindernumber_six=1
		elif cylindernumber_select==12:
			cylindernumber_twelve=1
		else:
			pass


		doornumber_two = 0
		doornumber = request.form['doornumber']
		if doornumber=="Two":
			doornumber_two=1
		else:
			pass # means doornumber_four=1

		enginelocation_rear =0
		enginelocation = request.form['enginelocation']
		if enginelocation == "rear":
			enginelocation_rear=1
		else:
			pass # means enginelocation_front=1


		drivewheel_fwd =0
		drivewheel_rwd =0
		drivewheel = request.form['drivewheel']
		if drivewheel=="fwd":
			drivewheel_fwd=1
		elif drivewheel=="rwd":
			drivewheel_rwd=1
		else:
			pass #this means drivewheel_4wd=1

		fuelsystem_2bbl =0
		fuelsystem_4bbl=0
		fuelsystem_mfi=0
		fuelsystem_idi=0
		fuelsystem_mpfi=0
		fuelsystem_spdi=0
		fuelsystem_spfi=0
		fuelsystem_select = request.form["fuelsystem_select"]
		if fuelsystem_select=="2bbl":
			fuelsystem_2bbl=1
		elif fuelsystem_select=="4bbl":
			fuelsystem_4bbl=1
		elif fuelsystem_select=="mfi":
			fuelsystem_mfi=1
		elif fuelsystem_select=="idi":
			fuelsystem_idi=1
		elif fuelsystem_select=="mpfi":
			fuelsystem_mpfi=1
		elif fuelsystem_select=="spdi":
			fuelsystem_spdi=1
		elif fuelsystem_select=="spfi":
			fuelsystem_spfi=1
		else:
			pass  # this means fuelsystem_1bbl =1



		prediction = model.predict([[Symboling, Car_Length, Car_Width, Curbweight, Engine_Size,
       Bore_Ratio, Horse_Power, City_Mpg, Highway_Mpg, fueltype_gas, aspiration_turbo, 
       doornumber_two, carbody_hardtop, carbody_hatchback, carbody_sedan, carbody_wagon, 
       drivewheel_fwd,drivewheel_rwd, enginelocation_rear, enginetype_dohcv,
       enginetype_l, enginetype_ohc, enginetype_ohcf, enginetype_ohcv, enginetype_rotor, 
       cylindernumber_five, cylindernumber_four, cylindernumber_six, cylindernumber_three, 
       cylindernumber_twelve, cylindernumber_two, fuelsystem_2bbl, fuelsystem_4bbl,
       fuelsystem_idi, fuelsystem_mfi, fuelsystem_mpfi,fuelsystem_spdi, fuelsystem_spfi]])

		output = round(prediction[0], 2)
		if output<0:
			return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
		else:
			return render_template('index.html',prediction_text="You Can Sell The Car at Rs {}".format(output))

	else:
		return render_template('index.html')

if __name__ == "__main__":
	app.run(debug=True)