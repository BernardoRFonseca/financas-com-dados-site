## Dias 10–23 · registo retrospetivo (escrito 30/ago) — nota metodológica
O diário esteve parado desde o Dia 9; as entradas abaixo foram escritas com dados de fecho, não de lançamento — as leituras de velocidade são menos finas do que nas entradas ao vivo. Agravante: o GitHub Actions degradou a recolha horária a partir de 26/ago (23 snapshots/dia → 2-7/dia; ambos os bots em simultâneo = scheduler do GitHub, não tokens; todos os runs que correram ficaram verdes). Corrigido a 30/ago com trigger externo via cron-job.org → workflow_dispatch. As curvas de #17, #68 e #10 têm buracos de 5-12h.

## Veredito #19 · day trading (fecho: 1.500 IG · 1.405 TT)
- Partilhas 0,56% · retenção relativa 19,6% (pior do canal à data) · saves 1
- Tema-informação outra vez abaixo dos temas-EU — consistente com a Lição 2, sem lição nova
- Nota TT: 5 novos seguidores em 1.405 views = melhor conversão TT até então; a espinha académica pode converter melhor do que distribui

## Dia 11-12 · #66 mediana salarial — LIÇÃO 7 REGISTADA
- IG: 2.995 (2º melhor do canal à data, 2.898 nas primeiras 48h) · TT: 310 = O PIOR do canal
- O MESMO vídeo: quase-recorde numa plataforma, fundo da tabela na outra
- **LIÇÃO 7 — as plataformas premeiam temas opostos e a correlação IG↔TT por vídeo é fraca:** IG paga dinheiro-pessoal/identidade (mediana, IRS); TT paga curiosidade/fofoca (elites — ver #67/#68). Deixar de esperar que um vídeo "bom" seja bom nas duas; planear por plataforma-alvo primária.

## Dia 13 · veredito #30 · manifesto OCDE (fecho: 469 IG · 527 TT)
- Pior vídeo completo do canal em IG: 469 views · 277 contas · 0 comentários externos
- Lição 2 reconfirmada pela 3ª vez (tema-sociedade/manifesto): #39, #19, #30 — o padrão já não é hipótese
- Primeira vez que TT > IG num vídeo não-breakout — coerente com a Lição 7

## Dia 15-16 · #67 deputados — RECORDE DUPLO
- **IG: 3.332 = novo máximo absoluto do canal**, destronou o #1 (3.202) e fê-lo em 8 dias vs 23 — 96% das views nas primeiras 48h
- **TT: 7.174 = 1º breakout do projeto** (5× o 2º melhor à data) · +5 seguidores TT (0,07% das views)
- Retenção relativa 37,6% = melhor do canal — a prioridade nº1 (Lição 5) está a dar fruto mensurável
- Slot: sábado 11h30 (2º sábado forte seguido; ressalva — confundido com o tema)

## Veredito #11 · Big Mac (fecho: 2.224 IG · 384 TT)
- Retenção 35,8% (2º melhor) mas partilhas 0,19% e 1 save — curiosidade prende, não posiciona
- TT fraco outra vez num tema não-elite (Lição 7 a acumular casos)

## Dia 18-19 · #49 regra dos 4% — LIÇÃO 8 REGISTADA
- **16 saves = 0,98% do alcance — 4-5× qualquer outro vídeo do canal** · partilhas 1,58% (2º melhor) · 2.078 views
- **LIÇÃO 8 — conteúdo-referência gera SAVES, um comportamento distinto de partilhas e likes:** identidade→partilha (IRS/salário) · curiosidade-elite→views TT · utilidade/regra→save. Três arquétipos com funções diferentes no portefólio. O score real quase não vê saves — corrigir na recalibração.
- Ressalva: n=1 no arquétipo; testar com mais 1-2 vídeos-regra antes de fixar rácio

## Dia 20-21 · #17 habitação Lisboa — o PUZZLE (fecho: 772 IG)
- Tema-EU com números-choque (+102% Lisboa) e mesmo assim 772 views, 760 já dentro às 48h — morreu no lançamento, não na cauda
- Quebra a heurística "tema-EU = performance". Hipóteses por ordenar: (a) hook falhou, (b) saturação do tema habitação no fintok PT, (c) slot quinta 18h30 fraco. Sem dados para escolher — registar e revisitar se outro tema-EU falhar
- Ressalva de dados: curva com buracos (Actions degradado desde 26/ago)

## Dia 22-23 · #68 CEOs + surto de seguidores — LIÇÃO 9 (HIPÓTESE FORTE)
- **TT: 7.109 em ~24h = 2º breakout**, gémeo do #67 em views e tema · IG: 2.608 no dia 1
- **Seguidores TT: 24 → 47 em ~28h (+23 ≈ 0,32% das views) vs #67: +5 em 7,2k (0,07%) — conversão 4-5× superior com alcance idêntico**
- **LIÇÃO 9 — o funil converte quando há SÉRIE reconhecível:** um vídeo é curiosidade, dois é um programa. O 2º episódio do mesmo formato deu ao espectador razão para seguir. Coerente com a prioridade "ganchos de regresso" já identificada. **Ressalva: n=1 no salto de conversão — é a hipótese a testar nas próximas 3-4 semanas, KPI = seguidores/1k views ≥ 0,3%**
- Contraste de plataformas ao mês: TT 19→47 seguidores numa semana · IG 211→230 em 19 dias — o TT passou a converter melhor apesar de menos consistente em views

## Mudanças de canal a registar (30/ago)
- **Baseline IG subiu:** chão passou de ~1k para ~2k+ (coorte #66/#67/#11/#49/#68: 2,1-3,3k) — os baselines de velocidade do score v2 estão obsoletos; recalibrar
- **48h = a vida toda:** 93-97% das views vitalícias chegam nas primeiras 48h em praticamente todos os vídeos — mais duro que a regra do "dia 4"; a cadência de 2 em 2 dias não é mínimo, é o jogo inteiro
- **Like% dilui com o alcance** (recentes 1,5-2,3% vs iniciais 3,5-4,9% do alcance) — é expansão de não-seguidores, não conteúdo pior; o score penaliza sistematicamente os vídeos que rebentam; corrigir na recalibração
- **cliques_bio = 0 é estrutural** (não há link na bio) — métrica inerte até existir destino; quando houver, cliques_bio/visitas_perfil passa a KPI de funil
- Higiene: novos_seguidores por vídeo (manual, TT) descontinuado — canal.historico é a fonte de verdade; campos estado dessincronizados em performance.json; mapping do #10 IG suspeito (alcance 9 vs 187 views)
