
# [START gae_python38_app]

from flask import Flask, render_template, request

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

def take_home_2020(incometxt):
    """A function to calculate take home pay based on salary earned, tax year is 2020"""
    
    income = int(incometxt)
    #Define the income bands
    pa = 12500 # Yearly personal allowance
    higher = 50000
    inter = 100000
    no_pa = 125000
    additional = 150000
    #PA reduces by £1 for every £2 over £100,000, we must account for this
    new_pa = pa - ((income - inter) / 2 )
    ni_1 = 792 #This is monthly
    ni_2 = 4167 #This is monthly
    
    #current tax rates
    basic_tax = 0.2
    higher_tax = 0.4
    additional_tax = 0.45
    ni_tax_1 = 0.12
    ni_tax_2 = 0.02
    
    if income <= pa:
        inc_tax = 0
    elif income > pa and income <= higher:
        inc_tax = round((income - pa) * basic_tax,2)
    elif income > higher and income <= inter:
        inc_tax = round(((income - higher) * higher_tax) + ((higher - pa) * basic_tax),2)
    elif income > inter and income <= no_pa:
        inc_tax = round(((income - additional) * additional_tax) + ((additional - higher + new_pa) * higher_tax) + ((higher - new_pa) * basic_tax),2)
    else:
        inc_tax = round(((income - additional) * additional_tax) + ((additional - higher + pa) * higher_tax) + ((higher-pa) * basic_tax),2)
    taxable = '{:,.2f}'.format(income - inc_tax)
    
    #Calculate National Insurance
    monthly = income / 12
    
    if monthly < ni_1:
        ni = 0
    elif monthly >= ni_1 and monthly < ni_2:
        ni = round((monthly-ni_1) * ni_tax_1,2)
    else:
        ni = round(((monthly - ni_2) * ni_tax_2) + (((ni_2 - ni_1) * ni_tax_1)),2)
      
    #Some final calcualtions for output
    ni = round(ni * 12,2)
    take = round(income - inc_tax - ni,2)
    monthly_take = '{:,.2f}'.format(take / 12)

    if income <= pa:
        taxable = 0
    elif income > pa and income <= inter:
        taxable = '{:,.2f}'.format(income - pa)
    elif income <= no_pa:
        taxable = '{:,.2f}'.format(income - new_pa)
    else:
        taxable = '{:,.2f}'.format(income)
       
    
    #Print statements used prior to HTML
    # print("Your taxable income is £{0:,.2f}".format(taxable))
    # print("Your income tax is £{0:,.2f}".format(inc_tax))
    # print("Your NI contribution is £{0:,.2f}".format(ni))
    # print("Your take home pay is £{0:,.2f}".format(take))
    # print("Your monthly take is £{0:,.2f}".format(monthly_take))

    #Change the remaining variables into strings with the correct format
    inc_tax = '{:,.2f}'.format(inc_tax)
    ni = '{:,.2f}'.format(ni)
    take = '{:,.2f}'.format(take)
    income = '{:,.2f}'.format(income)

    #Create dictionary of output variables to be found with HTML
    calculations = dict()
    calculations['taxable'] = taxable
    calculations['inc_tax'] = inc_tax
    calculations['ni'] = ni
    calculations['take'] = take
    calculations['monthly_take'] = monthly_take
    calculations['income'] = income

    return calculations

@app.route('/', methods=['GET', 'POST'])
def hello(name=None):
	thome = None
	if request.method == 'POST':
		income = request.form.get('income')
		thome = take_home_2020(income)
		print(thome)
		#print(request.form['income'])
	return render_template('index.html', name=name, thome=thome)




if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python38_app]
