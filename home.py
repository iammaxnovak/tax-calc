def take_home_2020(income):
    """A function to calculate take home pay based on salary earned, tax year is 2020"""
    
    #Define the income bands
    pa = 12500 # Yearly personal allowance
    higher = 50000
    inter = 100000
    additional = 150000
    ni_1 = 792 #This is monthly
    ni_2 = 4167#This is monthly
    
    #current tax rates
    basic_tax = 0.2
    higher_tax = 0.4
    additional_tax = 0.45
    ni_tax_1 = 0.12
    ni_tax_2 = 0.02
    
    #PA reduces by £1 for every £2 over £100,000, we must account for this
    if income > inter and income <= additional:
        reduction = (inter - income) / 2
        new_pa = pa = reduction
    
    #Calculate taxable income
    if income <= pa:
        inc_tax = 0
    elif income > pa and income <= higher:
        inc_tax = round((income - pa) * basic_tax,2)
    elif income > higher and income <= additional:
        inc_tax = round(((income - higher) * higher_tax) + ((higher - pa) * basic_tax),2)
    elif income > inter and income <= additional:
        inc_tax = round(((income - additional) * additional_tax) + ((additional - higher + new_pa) * higher_tax) + ((higher - new_pa) * basic_tax),2)
    else:
        inc_tax = round(((income - additional) * additional_tax) + ((additional - higher + pa) * higher_tax) + ((higher-pa) * basic_tax),2)
    taxable = income - inc_tax
    
    #Calculate National Insurance
    monthly = income / 12
    
    if monthly < ni_1:
        ni = 0
    elif monthly >= ni_1 and monthly < ni_2:
        ni = round((monthly-ni_1) * ni_tax_1,2)
    else:
        ni = round(((monthly - ni_2) * ni_tax_2) + (((ni_2 - ni_1) * ni_tax_1)),2)
      
    #Some final calcualtions
    ni = round(ni * 12,2)
    take = round(income - inc_tax - ni,2)
    monthly_take = round(take / 12, 2)
    
    print("You're taxable income is £{}".format(taxable))
    print("You're income tax is £{}".format(inc_tax))
    print("You're NI contribution is £{}".format(ni))
    print("You're take home pay is £{}".format(take))
    print("You're monthly take is £{}".format(monthly_take))