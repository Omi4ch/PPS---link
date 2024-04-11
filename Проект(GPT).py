import g4f

def SSILKI ():
	response = g4f.ChatCompletion.create(
	    model=g4f.models.gpt_35_turbo,
	    messages=[{"role":"user","content":a}],
	    stream=True,
	)
	print (response)

a = str(input())
SSILKI(a)


