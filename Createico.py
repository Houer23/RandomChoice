import base64

with open('favicon3.ico', 'rb') as reader:
	ico_bin = reader.read()
ico_base64 = base64.b64encode(ico_bin)
with open('ico.py', 'wt') as fp:
	fp.write(f'ico = {ico_base64}')