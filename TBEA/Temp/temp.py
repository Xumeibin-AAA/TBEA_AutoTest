import requests

s = requests.session()
p = {'username':'tbea_guest1','password':'123456'}
h= {'Cookie':'JSESSIONID=D3BA8C37D7D083FF33B50568C8FE99AF'}
v = s.post('http://trial.tbeayun.com/tbea_be/trialController/listTrial',headers = h)
print(v.text)
