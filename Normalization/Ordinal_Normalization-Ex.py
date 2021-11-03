data_vals = {"Kindergarten":0, "First_Grade":1, "Second_Grade":2, "Third_Grade":3}
n_limit = {"h":1, "l":-1}
n_width = n_limit["h"] - n_limit["l"]

data_rev_key = {}
for x in data_vals.keys():
    data_rev_key[data_vals[x]] = x

def normalize (inp):
    n_out = float(n_width * data_vals[inp])/len(data_vals) + n_limit["l"]
    return n_out

def denormalize (inp):
    n_out = float(len(data_vals) * (inp - n_limit['l']))/n_width
    n_out = int(n_out)
    return n_out, data_rev_key[n_out]

print normalize("First_Grade")
print denormalize(-0.5)