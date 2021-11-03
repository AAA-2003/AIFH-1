
#Normalized value limts
n_limit = {'h':1, 'l':-1}
#Observation limits
data_limit = {'h':4000, 'l':100}

n_range  = n_limit['h']-n_limit['l']
data_range = data_limit['h'] - data_limit['l']

def normalize(inp):
    n_out = (inp-data_limit['l'])*float(n_range) / data_range + n_limit['l']
    return n_out

def denormalize(inp):
    n_out = (inp - n_limit['l'])*float(data_range)/n_range + data_limit['l']
    n_out = float(data_limit['l']-data_limit['h'])*inp - (n_limit['h']*data_limit['l']) + (data_limit['h']*n_limit['l'])
    return n_out/(n_limit['l'] - n_limit['h'])


print normalize(2050)
print denormalize(0)