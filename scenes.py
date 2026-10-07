# -*- coding: utf-8 -*-
# Roteiro + estrutura visual do vídeo "Tacógrafo – Integração Tóliman 2026"
# Cada cena tem "beats": narr = texto da narração (ElevenLabs), show = itens que aparecem naquele trecho.

MODULES = ["O disco", "Preenchimento", "Inserir no drive", "Deveres", "Entrega e reposição"]

SCENES = [
  dict(id="abertura", layout="cover", title="Treinamento de Integração", sub="Tacógrafo para Motoristas · 2026",
       beats=[
         dict(narr="Olá, motorista! Seja bem-vindo ao treinamento de integração da Tóliman Transportes, do Grupo Dínamo."),
         dict(narr="Hoje você vai entender como funciona o tacógrafo e como usar corretamente o disco de tacógrafo no seu dia a dia."),
       ]),

  dict(id="agenda", layout="content", module=None, chip="Introdução", title="O que você vai aprender",
       panel=("5", "temas neste treinamento"),
       items=[
         dict(t="num", n="1", text="O que é o disco de tacógrafo"),
         dict(t="num", n="2", text="Como preencher o disco"),
         dict(t="num", n="3", text="Como inserir o disco no drive"),
         dict(t="num", n="4", text="Seus deveres como motorista"),
         dict(t="num", n="5", text="Entrega, devolução e reposição"),
       ],
       beats=[
         dict(narr="Neste treinamento, vamos passar por cinco temas.", show=[]),
         dict(narr="Primeiro: o que é o disco de tacógrafo e como ele funciona.", show=[0]),
         dict(narr="Depois, como preencher o disco corretamente.", show=[1]),
         dict(narr="Em seguida, como inserir o disco no drive do veículo, evitando avarias.", show=[2]),
         dict(narr="Também vamos falar sobre os seus deveres como motorista.", show=[3]),
         dict(narr="E, por fim, como funciona a entrega, a devolução e a reposição dos discos.", show=[4]),
       ]),

  dict(id="definicao", layout="content", module=0, title="O que é o disco de tacógrafo",
       img="velocimetro.jpg",
       items=[
         dict(t="check", text="Registra a velocidade do veículo em tempo real"),
         dict(t="check", text="Gráfico inalterável: velocidade × horário"),
         dict(t="check", text="1 jogo = 7 discos = 7 dias"),
         dict(t="warn", text="À 00:00 o drive troca sozinho para o disco do dia seguinte"),
       ],
       beats=[
         dict(narr="O disco de tacógrafo é a ferramenta que registra, em tempo real, a velocidade atingida pelo veículo.", show=[0]),
         dict(narr="O funcionamento é simples: por meio de um gráfico, ele marca, de forma inalterável, qual era a velocidade do veículo em cada horário do dia.", show=[1]),
         dict(narr="Cada jogo de disco tem sete folhas, uma para cada dia. Ou seja, um jogo dura sete dias.", show=[2]),
         dict(narr="E atenção: depois das vinte e quatro horas, à meia-noite, o drive troca automaticamente para o disco do dia seguinte.", show=[3]),
       ]),

  dict(id="preenchimento1", layout="content", module=1, title="Preenchimento do disco",
       img="disco.jpg", grid=True,
       items=[
         dict(t="head", text="1ª folha do jogo: preenchimento completo"),
         dict(t="field", n="1", text="Nome e sobrenome"),
         dict(t="field", n="2", text="Nome e sobrenome (2º motorista)"),
         dict(t="field", n="3", text="Destino"),
         dict(t="field", n="4", text="Data da viagem"),
         dict(t="field", n="5", text="Placa do veículo"),
         dict(t="field", n="6", text="Quilometragem de saída"),
         dict(t="field", n="7", text="Quilometragem de chegada"),
       ],
       beats=[
         dict(narr="Agora, vamos ao preenchimento. A primeira folha do jogo deve ser preenchida por completo, com sete informações.", show=[0]),
         dict(narr="Nome e sobrenome do motorista. Nome e sobrenome do segundo motorista, quando houver. Destino. Data da viagem. Placa do veículo. Quilometragem de saída. E quilometragem de chegada.",
              show=[1, 2, 3, 4, 5, 6, 7], spread=True),
       ]),

  dict(id="preenchimento2", layout="content", module=1, title="Assinatura em todas as folhas",
       panel=("7 de 7", "folhas assinadas em cada jogo"),
       items=[
         dict(t="check", text="Demais folhas: NOME e SOBRENOME"),
         dict(t="check", text="Assine TODAS as 7 folhas do jogo"),
         dict(t="check", text="Folgas também são assinadas: comprovam que o veículo ficou parado"),
         dict(t="warn", text="Disco sem preenchimento = risco de multa na fiscalização"),
       ],
       beats=[
         dict(narr="Nas demais folhas do jogo, basta colocar o seu nome e sobrenome.", show=[0]),
         dict(narr="E muito importante: o motorista deve assinar todas as sete folhas do jogo.", show=[1]),
         dict(narr="Isso vale também para as folhas dos dias de folga no fim de semana. A sua assinatura comprova que você estava de folga e que o veículo ficou parado.", show=[2]),
         dict(narr="Lembre-se: em uma parada policial, se o disco não estiver preenchido, você pode ser responsabilizado e multado.", show=[3]),
       ]),

  dict(id="inserir", layout="content", module=2, title="Como inserir o disco no drive",
       img="drive.png",
       items=[
         dict(t="num", n="1", text="Horário do drive igual ao do rastreador"),
         dict(t="num", n="2", text="Drive limpo e em boas condições"),
         dict(t="num", n="3", text="Encaixe o disco com cuidado, na hora exata"),
         dict(t="check", text="Evite amassar, riscar ou avariar o disco"),
         dict(t="warn", text="Disco com rasura ou avaria? Avise o RH (Carlos) e a Manutenção (Ewerton)"),
       ],
       beats=[
         dict(narr="Vamos ver agora como inserir o disco no drive.", show=[]),
         dict(narr="Antes de tudo, confira se o horário do drive está igual ao horário do rastreador, ou seja, do tablet ou computador de bordo.", show=[0]),
         dict(narr="Ao apertar o botão para abrir o drive, verifique se ele está limpo e em boas condições.", show=[1]),
         dict(narr="Insira o disco com cuidado, ajustando para que ele fique exatamente na hora marcada pelo drive e pelo rastreador.", show=[2]),
         dict(narr="Fique atento para evitar qualquer avaria no disco.", show=[3]),
         dict(narr="E se, ao retirar o jogo depois dos sete dias, algum disco estiver rasurado ou avariado, comunique imediatamente o RH, com o Carlos, e a manutenção, com o Ewerton.", show=[4]),
       ]),

  dict(id="lei", layout="content", module=3, title="Tacógrafo é obrigatório por lei",
       panel=("Art. 105", "Código de Trânsito Brasileiro · Resoluções CONTRAN 14/98 e 87/99"),
       items=[
         dict(t="warn", text="Proibido dirigir sem o disco no drive"),
         dict(t="check", text="Antes de sair: disco no drive + jogos para a semana toda"),
         dict(t="check", text="Confira se o disco e o drive estão funcionando bem"),
         dict(t="check", text="Drive com defeito? Manutenção (pelo RV) + RH/GTP (WhatsApp do setor)"),
       ],
       beats=[
         dict(narr="O tacógrafo é obrigatório por lei, conforme o artigo cento e cinco do Código de Trânsito Brasileiro e as resoluções catorze, de noventa e oito, e oitenta e sete, de noventa e nove, do Contran.", show=[]),
         dict(narr="Por isso, é proibido conduzir o veículo sem o disco de tacógrafo.", show=[0]),
         dict(narr="Antes de iniciar a viagem, é sua responsabilidade conferir se o disco está colocado no drive, e se há jogos suficientes para toda a sua jornada semanal.", show=[1]),
         dict(narr="Confira também se o disco e o drive estão funcionando bem.", show=[2]),
         dict(narr="Se o drive apresentar qualquer problema, avise na hora a manutenção, pelo RV, e o RH e GTP, pelo WhatsApp do setor.", show=[3]),
       ]),

  dict(id="placa", layout="content", module=3, title="Placa certa e troca de motorista",
       img="caminhao.png",
       items=[
         dict(t="warn", text="Use somente disco da placa do veículo que você conduz"),
         dict(t="check", text="Assumiu a viagem de outro motorista? Continue o mesmo jogo até a 7ª folha"),
         dict(t="check", text="Cada motorista preenche e assina os dias que dirigiu"),
         dict(t="check", text="Na sua 1ª folha: nome, data, km de saída e chegada, destino e placa"),
       ],
       beats=[
         dict(narr="Nunca use um disco que pertença a outra placa. O disco é sempre do veículo que você está conduzindo.", show=[0]),
         dict(narr="Se você der continuidade a uma viagem iniciada por outro motorista, não troque o jogo: continue usando o mesmo, até completar as sete folhas.", show=[1]),
         dict(narr="Cada motorista preenche e assina as folhas referentes aos dias em que dirigiu.", show=[2]),
         dict(narr="Na folha do dia em que você começou a dirigir, coloque seu nome e sobrenome, a data, a quilometragem de saída e de chegada, o destino e a placa do veículo.", show=[3]),
       ]),

  dict(id="sequencia", layout="content", module=3, title="Use os conjuntos na sequência",
       img="verso.png", caption="Verso da última folha: nº do conjunto no carimbo",
       items=[
         dict(t="check", text="Cada caixa tem 10 conjuntos numerados"),
         dict(t="check", text="Nº do conjunto: no carimbo, no verso da última folha"),
         dict(t="flow", steps=["1", "2", "3", "…", "10"]),
         dict(t="check", text="Sequência certa = controle em dia, sem disco em atraso"),
         dict(t="warn", text="Ao devolver o conjunto 9, devolva também a caixa"),
       ],
       beats=[
         dict(narr="Cada caixa deixada no seu veículo tem dez conjuntos, e cada conjunto é numerado.", show=[0]),
         dict(narr="Antes de colocar o disco no drive, confira o número do conjunto. Ele fica no carimbo, no verso da última folha do jogo.", show=[1]),
         dict(narr="Use sempre na ordem: primeiro o conjunto um, depois o dois, o três, e assim por diante, até o dez.", show=[2]),
         dict(narr="Respeitar a sequência mantém o nosso controle em dia, e evita que apareçam discos em atraso no seu nome.", show=[3]),
         dict(narr="E, ao devolver o conjunto nove, entregue na portaria também a caixa em que você recebeu os dez conjuntos.", show=[4]),
       ]),

  dict(id="entrega", layout="content", module=4, title="Entrega dos discos usados",
       img="lista.jpg",
       items=[
         dict(t="check", text="Entrega na portaria da Tóliman, em Machado"),
         dict(t="check", text="Veículo na Dínamo Machado → porteiro da Dínamo", sub="Pátio da antiga Ferracini → porteiro da Tóliman Machado"),
         dict(t="check", text="Início da semana: entregue o jogo preenchido, datado e assinado"),
         dict(t="check", text="O porteiro registra na lista de placas e você assina"),
       ],
       beats=[
         dict(narr="Agora, a entrega dos discos usados. Toda entrega de disco deve ser feita na portaria da Tóliman, em Machado.", show=[0]),
         dict(narr="Se o veículo estiver na Dínamo Machado, entregue ao porteiro da Dínamo. Se estiver no pátio da antiga Ferracini, entregue ao porteiro da Tóliman Machado.", show=[1]),
         dict(narr="Ao iniciar a sua nova semana de trabalho, no domingo ou no dia em que começar a sua jornada, entregue o jogo usado, devidamente preenchido, datado e assinado.", show=[2]),
         dict(narr="Na portaria existe uma lista com todas as placas. O porteiro registra a entrega do disco, e você assina confirmando o registro.", show=[3]),
       ]),

  dict(id="reposicao", layout="content", module=4, title="Reposição de discos",
       panel=("10", "jogos virgens sempre no seu veículo"),
       items=[
         dict(t="check", text="Reposição é responsabilidade da Tóliman Transportes"),
         dict(t="check", text="RH/GTP repõe aos sábados, completando 10 jogos"),
         dict(t="check", text="Procure em todos os compartimentos antes de pedir"),
         dict(t="flow", label="Sem disco? Peça a:", steps=["RH/GTP · Emerson ou Larissa", "Logística", "Manutenção"]),
       ],
       beats=[
         dict(narr="A reposição das caixas de disco de tacógrafo é responsabilidade da Tóliman Transportes.", show=[0]),
         dict(narr="O setor de RH e GTP, no controle de jornada, faz a reposição padrão aos sábados, completando sempre dez jogos virgens no seu veículo.", show=[1]),
         dict(narr="Antes de pedir uma caixa nova, procure bem em todos os compartimentos do veículo.", show=[2]),
         dict(narr="Se realmente estiver sem disco, peça ao RH e GTP, com o Emerson ou a Larissa. Na ausência deles, peça à Logística e, por último, à Manutenção da Tóliman, em Machado.", show=[3]),
       ]),

  dict(id="resumo", layout="content", module=None, chip="Resumo", title="Antes de cada viagem, confira",
       panel=("✓", "checklist do motorista"),
       items=[
         dict(t="check", text="Horário do drive igual ao do rastreador"),
         dict(t="check", text="Disco da placa certa, encaixado na hora exata"),
         dict(t="check", text="1ª folha completa e as 7 folhas assinadas"),
         dict(t="check", text="Jogos suficientes, usados na sequência de 1 a 10"),
         dict(t="check", text="Jogo da semana anterior entregue na portaria"),
       ],
       beats=[
         dict(narr="Para fechar, um resumo rápido do que conferir antes de cada viagem.", show=[]),
         dict(narr="O horário do drive igual ao do rastreador.", show=[0]),
         dict(narr="O disco da placa certa, encaixado na hora exata.", show=[1]),
         dict(narr="A primeira folha completa, e as sete folhas assinadas.", show=[2]),
         dict(narr="Jogos suficientes para a semana, usados na sequência de um a dez.", show=[3]),
         dict(narr="E o jogo da semana anterior entregue na portaria.", show=[4]),
       ]),

  dict(id="encerramento", layout="end", title="Agradecemos a sua participação!", sub="Dúvidas? Fale com o RH · Carlos Roberto",
       beats=[
         dict(narr="O tacógrafo protege você, a empresa e todos na estrada. Preencher e cuidar bem do disco faz parte do seu trabalho."),
         dict(narr="Em caso de dúvidas, procure o RH, com o Carlos Roberto. A Tóliman agradece a sua participação. Boa viagem!"),
       ]),
]

CHARS_PER_SEC = 14.5   # ritmo médio estimado de uma voz pt-BR no ElevenLabs


def beat_duration(text, first=False, last=False):
    d = max(2.8, len(text) / CHARS_PER_SEC + 0.9)
    if first:
        d += 0.5
    if last:
        d += 0.6
    return round(d, 2)
