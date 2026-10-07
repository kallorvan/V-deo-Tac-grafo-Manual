# Handoff: Vídeo de treinamento do Tacógrafo (Integração Tóliman 2026)

## Objetivo
Vídeo narrado de integração para motoristas (Tóliman Transportes / Grupo Dínamo) que ensina como funciona o tacógrafo e como usar o disco: preenchimento, inserção no drive, deveres, entrega/devolução e reposição. A base é o PPTX do RH, `fonte/Integr.Reciclag.RH - Tacógrafo - REV 03 Motoristas -2026.pptx` (responsável: Carlos Roberto, RH).

## Status (07/10/2026)
- **Concluído:** vídeo final narrado, `Tacografo_Integracao_2026_narrado.mp4` (6 min 35 s, 1920×1080, 30 fps, H.264 + AAC). Foi entregue ao usuário e não está neste pacote, mas é regenerável com `python build.py`.
- A narração foi gerada pelo usuário no **ElevenLabs**: 13 MP3, um por cena, em `audio/`.
- O roteiro de narração está em `roteiro.md` (é o texto que foi colado no ElevenLabs).
- **Pendências de conteúdo** (herdadas do PPTX, ainda não confirmadas com o RH):
  1. Endereços de entrega citados: portaria Tóliman **Machado**, Dínamo Machado, pátio da antiga Ferracini. Confirmar se ainda valem.
  2. Base legal: art. 105 do CTB e Resoluções CONTRAN 14/98 e 87/99, mantidos como no PPTX. Podem estar desatualizados.
  3. A sigla "RV" (canal da manutenção) foi mantida sem explicação.
  4. O PPTX lista o tema "Possíveis avarias", mas não tem slide próprio. O tema foi incorporado à cena `inserir`.

## Estrutura
```
CLAUDE.md          este arquivo
scenes.py          ROTEIRO + ESTRUTURA VISUAL (fonte única de verdade)
build.py           renderizador (Playwright → frames PNG → ffmpeg) + sincronização com áudio
stills.py          gera um PNG do estado final de cada cena (build/still_*.png + build/contact.png) para revisar o layout rápido
roteiro.md         roteiro para o ElevenLabs (gerado a partir de scenes.py, com timecodes da versão sem áudio)
requirements.txt
assets/            imagens extraídas do PPTX (logos, disco, drive, caminhão, etc.) + fonts/ (Poppins, OFL)
audio/             NN_<id>.mp3, narração por cena (ElevenLabs)
fonte/             PPTX original
build/             saída (criada pelo build): HTML por cena, timeline.json, video_silent.mp4
```

## Como rodar
```bash
pip install -r requirements.txt
python -m playwright install chromium
# ffmpeg e ffprobe precisam estar no PATH
python stills.py                                  # revisão visual rápida (segundos)
python build.py build/Tacografo_Integracao_2026_narrado.mp4   # vídeo completo (~8 min de render)
python build.py saida.mp4 --preview               # só as 3 primeiras cenas (teste rápido)
```

## Como funciona
- **`scenes.py`**: tem a lista `SCENES`, uma cena por slide do vídeo. Os layouts são:
  - `cover` / `end`: capa e encerramento, com fundo navy e logos.
  - `content`: título e chip "Módulo X de 5". O painel da esquerda é `img` (uma imagem de assets/) ou `panel=(número grande, legenda)`. A coluna da direita tem os `items`, que aparecem animados.
  - Tipos de item: `check`, `num` (com `n`), `warn` (caixa coral), `field` (grade de 2 colunas quando `grid=True`), `head` (subtítulo) e `flow` (passos com setas; `steps` e `label` opcional).
  - `beats`: lista de `{narr: texto falado, show: [índices de items que aparecem nesse trecho]}`. Com `spread=True`, os itens aparecem um por frase do `narr`. É o caso dos 7 campos do disco.
  - `MODULES`: os nomes da barra de progresso do rodapé. O `module` de cada cena indica o segmento ativo.
- **Sincronização (`timeline()` em build.py)**:
  - Sem áudio: a duração vem da estimativa de `len(texto)/CHARS_PER_SEC`.
  - Com `audio/*<id>.mp3`: a duração da cena fica em 0,4 s + áudio + 0,6 s. O `narr` é quebrado em frases, e as fronteiras entre frases são alinhadas às pausas reais do áudio (ffmpeg `silencedetect`, alinhamento monotônico por programação dinâmica). Cada item aparece quando a frase dele começa a ser falada. O alinhamento foi verificado: a cena do preenchimento bate com o áudio em cerca de 0,1 s.
  - **Ao mudar um `narr`, mantenha o mesmo número de frases do áudio**, ou regenere o MP3. A divisão é feita por `. ! ? :`.
- **Render**:
  - Cada cena vira um HTML (`build/<id>.html`) com a função JS `render(t)`, que posiciona as animações (fade/slide com easing) no tempo t.
  - O Playwright tira screenshot só dos frames em que algo anima. Nos frames parados, o PNG anterior é repetido. Os frames vão por pipe para o ffmpeg.
  - Entre cenas há um crossfade de 10 frames.
  - No final, os MP3 são mixados com `adelay` no início de cada cena.
- **Identidade visual**: navy `#0B2350`, coral `#E9516B`, lilás `#AB85B6`, amarelo `#F9D590`, fonte Poppins. Rodapé navy com o logo Tóliman, o progresso por módulo e o logo Dínamo.

## Fluxos comuns
- **Trocar uma fala:** edite o `narr` em `scenes.py`, regere só aquele MP3 no ElevenLabs com o mesmo nome (`NN_<id>.mp3`) e rode `build.py`. Atualize `roteiro.md` se quiser manter o roteiro em dia.
- **Trocar o texto na tela:** edite `items[].text` em `scenes.py`. Não precisa de áudio novo.
- **Nova cena:** acrescente um dict em `SCENES` com `id` único e grave `audio/NN_<id>.mp3`. O glob do áudio procura `*<id>.mp3`, então use ids que não sejam sufixo de outro id.
- **Configurações usadas no ElevenLabs:** Multilingual v2, voz pt-BR, Stability ~50%, Similarity ~75%, Style 0–15%. Os números da narração estão escritos por extenso.

## Contexto do usuário
Paulo Eduardo trabalha na Tóliman Transportes (Grupo Dínamo) e fala português. O vídeo é para a integração e reciclagem de motoristas (RH).
