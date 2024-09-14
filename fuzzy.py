import skfuzzy
from skfuzzy import control
import numpy as np
import matplotlib.pyplot as plt

tipo = control.Antecedent(np.arange(0, 100, 1), 'tipo')
qtde = control.Antecedent(np.arange(0, 10, 1), 'qtde')
sujeira = control.Antecedent(np.arange(0, 100, 1), 'sujeira')

tipo['fina'] = skfuzzy.trimf(tipo.universe, [-50, 0, 50])
tipo['grossa'] = skfuzzy.trimf(tipo.universe, [20, 50, 80])
tipo['jeans'] = skfuzzy.trimf(tipo.universe, [50, 100, 150])
tipo.view()

qtde['pouca'] = skfuzzy.trimf(qtde.universe, [-5, 0, 5])
qtde['normal'] = skfuzzy.trimf(qtde.universe, [2, 5, 8])
qtde['muita'] = skfuzzy.trimf(qtde.universe, [5, 10, 15])
qtde.view()

sujeira['pouca'] = skfuzzy.trimf(sujeira.universe, [-50, 0, 50])
sujeira['normal'] = skfuzzy.trimf(sujeira.universe, [20, 50, 80])
sujeira['muita'] = skfuzzy.trimf(sujeira.universe, [50, 100, 150])
sujeira.view()

lavagem = control.Consequent(np.arange(0, 50, 1), 'lavagem')
enxague = control.Consequent(np.arange(0, 60, 1), 'enxague')
giro = control.Consequent(np.arange(0, 180, 1), 'giro')

lavagem['curta'] = skfuzzy.trimf(lavagem.universe, [-20, 0, 20])
lavagem['normal'] = skfuzzy.trimf(lavagem.universe, [10, 25, 40])
lavagem['longa'] = skfuzzy.trimf(lavagem.universe, [35, 50, 50])
lavagem.view()

enxague['curtinho'] = skfuzzy.trimf(enxague.universe, [-12.5, 0, 12.5])
enxague['curto'] = skfuzzy.trimf(enxague.universe, [0, 12.5, 25])
enxague['normal'] = skfuzzy.trimf(enxague.universe, [15, 25, 35])
enxague['demoradinho'] = skfuzzy.trimf(enxague.universe, [25, 35, 45])
enxague['demorado'] = skfuzzy.trimf(enxague.universe, [40, 60, 80])
enxague.view()

giro['curtinho'] = skfuzzy.trimf(giro.universe, [0, 0, 40])
giro['curto'] = skfuzzy.trimf(giro.universe, [30, 52.5, 75])
giro['normal'] = skfuzzy.trimf(giro.universe, [50, 75, 100])
giro['demoradinho'] = skfuzzy.trimf(giro.universe, [75, 107.5, 140])
giro['demorado'] = skfuzzy.trimf(giro.universe, [120, 180, 480])
giro.view()

regra1 = control.Rule(qtde['muita'] & sujeira['muita'], enxague['demoradinho'])
regra2 = control.Rule(qtde['pouca'] & sujeira['pouca'], enxague['curtinho'])
regra3 = control.Rule(qtde['normal'] & sujeira['normal'], enxague['normal'])
regra4 = control.Rule(qtde['normal'] & sujeira['pouca'], enxague['curto'])
regra5 = control.Rule(qtde['muita'] & sujeira['normal'], enxague['demoradinho'])
regra6 = control.Rule(qtde['normal'] & sujeira['muita'], enxague['demorado'])
regra7 = control.Rule(qtde['muita'] & sujeira['pouca'], enxague['demoradinho'])
regra8 = control.Rule(qtde['pouca'] & sujeira['muita'], enxague['demoradinho'])

regra9 = control.Rule(qtde['pouca'] & sujeira['pouca'], lavagem['curta'])
regra10 = control.Rule(qtde['normal'] & sujeira['pouca'], lavagem['curta'])
regra11 = control.Rule(qtde['muita'] & sujeira['pouca'], lavagem['normal'])
regra12 = control.Rule(qtde['pouca'] & sujeira['normal'], lavagem['curta'])
regra13 = control.Rule(qtde['normal'] & sujeira['normal'], lavagem['normal'])
regra14 = control.Rule(qtde['muita'] & sujeira['normal'], lavagem['longa'])
regra15 = control.Rule(qtde['pouca'] & sujeira['muita'], lavagem['normal'])
regra16 = control.Rule(qtde['normal'] & sujeira['muita'], lavagem['longa'])
regra17 = control.Rule(qtde['muita'] & sujeira['muita'], lavagem['longa'])

regra18 = control.Rule(tipo['fina'] & qtde['pouca'], giro['curtinho'])
regra19 = control.Rule(tipo['jeans'] & qtde['muita'], giro['demorado'])
regra20 = control.Rule(tipo['fina'] & qtde['normal'], giro['curto'])
regra21 = control.Rule(tipo['grossa'] & qtde['normal'], giro['demoradinho'])
regra22 = control.Rule(tipo['grossa'] & qtde['pouca'], giro['normal'])
regra23 = control.Rule(tipo['grossa'] & qtde['muita'], giro['demoradinho'])
regra24 = control.Rule(tipo['fina'] & qtde['muita'], giro['normal'])
regra25 = control.Rule(tipo['jeans'] & qtde['normal'], giro['demoradinho'])
regra26 = control.Rule(tipo['jeans'] & qtde['pouca'], giro['normal'])

regras_enxague = control.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6, regra7, regra8])
regras_lavagem = control.ControlSystem([regra9, regra10, regra11, regra12, regra13, regra14, regra15, regra16, regra17])
regras_giro = control.ControlSystem([regra18, regra19, regra20, regra21, regra22, regra23, regra24, regra25, regra26])

resultado_enxague = control.ControlSystemSimulation(regras_enxague)
resultado_lavegem = control.ControlSystemSimulation(regras_lavagem)
resultado_giro = control.ControlSystemSimulation(regras_giro)

resultado_enxague.input['qtde'] = 2
resultado_enxague.input['sujeira'] = 25
resultado_enxague.compute()
print(resultado_enxague.output['enxague'])
enxague.view(resultado_enxague)

resultado_lavegem.input['qtde'] = 10
resultado_lavegem.input['sujeira'] = 25
resultado_lavegem.compute()
print(resultado_lavegem.output['lavagem'])
lavagem.view(resultado_lavegem)

resultado_giro.input['qtde'] = 12
resultado_giro.input['tipo'] = 80
resultado_giro.compute()
print(resultado_giro.output['giro'])
giro.view(resultado_giro)
