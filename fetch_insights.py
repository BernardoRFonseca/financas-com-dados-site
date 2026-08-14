#!/usr/bin/env python3
"""v3 — histórico por vídeo + HISTÓRICO DO CANAL (seguidores totais e insights de conta).
Defensivo: qualquer métrica indisponível é ignorada sem partir o resto."""
import os, json, urllib.request, urllib.parse, sys, datetime

TOKEN=os.environ["IG_ACCESS_TOKEN"]; IG_USER=os.environ["IG_USER_ID"]
API="https://graph.facebook.com/v21.0"
METRICS=["views","reach","likes","comments","shares","saved","total_interactions","ig_reels_avg_watch_time","follows","profile_visits"]
KEYMAP={"views":"views","reach":"alcance","likes":"likes","comments":"comentarios","shares":"partilhas",
        "saved":"saves","ig_reels_avg_watch_time":"tempo_medio_s","follows":"seguidores","profile_visits":"visitas_perfil"}
HIST_KEYS=["views","alcance","likes","comentarios","partilhas","saves","seguidores"]
HIST_MAX=2000
CANAL_INSIGHTS=["reach","profile_views","accounts_engaged","total_interactions","website_clicks"]

def get(url, params):
    params["access_token"]=TOKEN
    full=url+"?"+urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(full, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        print("API error:", e.code, e.read().decode()[:300], file=sys.stderr)
        raise

def main():
    mapping={k:v for k,v in json.load(open("mapping.json")).items() if not k.startswith("_")}
    perf=json.load(open("performance.json")) if os.path.exists("performance.json") else {}
    perf.setdefault("videos",{})
    now=datetime.datetime.now().isoformat(timespec="minutes")

    # ---- por vídeo ----
    medias=get(f"{API}/{IG_USER}/media",{"fields":"id,permalink,timestamp,caption","limit":"50"}).get("data",[])
    import re as _re
    for m in medias:
        code=m.get("permalink","").rstrip("/").split("/")[-1]
        vid=None
        if code in mapping: vid=str(mapping[code])              # override manual vence
        else:
            tag=_re.search(r"#fcd(\d+)", m.get("caption") or "")  # auto: hashtag-codigo na descricao
            if tag: vid=tag.group(1)
        if not vid: continue
        vals={}
        for met in METRICS:
            try:
                d=get(f"{API}/{m['id']}/insights",{"metric":met})
                for item in d.get("data",[]):
                    v=item.get("values",[{}])[0].get("value")
                    if isinstance(v,(int,float)): vals[item["name"]]=v
            except Exception: pass
        slot=perf["videos"].setdefault(vid,{})
        metd=slot.setdefault("metricas",{})
        for ak,ok in KEYMAP.items():
            if ak in vals:
                metd[ok]=round(vals[ak]/1000,1) if ak=="ig_reels_avg_watch_time" else vals[ak]
        if not slot.get("publicado_em"): slot["publicado_em"]=m.get("timestamp","")
        slot["atualizado"]=now
        hist=slot.setdefault("historico",[])
        ponto={"t":now}; ponto.update({k:metd[k] for k in HIST_KEYS if k in metd})
        hist.append(ponto)
        if len(hist)>HIST_MAX: del hist[:len(hist)-HIST_MAX]
        print(f"video {vid}: {len(vals)} metricas · hist={len(hist)}")

    # ---- canal ----
    canal=perf.setdefault("canal",{})
    ponto={"t":now}
    try:
        f=get(f"{API}/{IG_USER}",{"fields":"followers_count,follows_count,media_count"})
        ponto["seguidores"]=f.get("followers_count"); ponto["a_seguir"]=f.get("follows_count"); ponto["publicacoes"]=f.get("media_count")
    except Exception: pass
    for met in CANAL_INSIGHTS:
        try:
            d=get(f"{API}/{IG_USER}/insights",{"metric":met,"period":"day","metric_type":"total_value"})
            for item in d.get("data",[]):
                v=(item.get("total_value") or {}).get("value")
                if v is None:
                    vs=item.get("values",[{}]); v=vs[0].get("value") if vs else None
                if isinstance(v,(int,float)): ponto[{"reach":"alcance_dia","profile_views":"visitas_perfil","accounts_engaged":"contas_interagiram","total_interactions":"interacoes","website_clicks":"cliques_bio"}.get(item["name"],item["name"])]=v
        except Exception: pass
    # demografia (snapshot, nao-historico: muda devagar)
    demo={}
    for met,brk in [("follower_demographics","country"),("follower_demographics","age"),("engaged_audience_demographics","country"),("engaged_audience_demographics","age")]:
        try:
            d=get(f"{API}/{IG_USER}/insights",{"metric":met,"period":"lifetime","metric_type":"total_value","breakdown":brk,"timeframe":"this_month"})
            for item in d.get("data",[]):
                res=(item.get("total_value") or {}).get("breakdowns",[{}])[0].get("results",[])
                top=sorted(res,key=lambda r:-(r.get("value") or 0))[:6]
                demo[f"{item['name']}_{brk}"]={ (r.get("dimension_values") or ["?"])[0]: r.get("value") for r in top }
        except Exception: pass
    if demo:
        demo["atualizado"]=now
        canal["demografia"]=demo
        # série temporal da demografia: 1 snapshot por dia (muda devagar; poupa espaço)
        histd=canal.setdefault("demografia_historico",[])
        hoje=now[:10]
        if not histd or histd[-1]["t"][:10]!=hoje:
            ponto_d={"t":now}
            ponto_d.update({k:v for k,v in demo.items() if k!="atualizado"})
            histd.append(ponto_d)
            if len(histd)>400: del histd[:len(histd)-400]
    hist=canal.setdefault("historico",[])
    hist.append(ponto)
    if len(hist)>HIST_MAX: del hist[:len(hist)-HIST_MAX]
    print(f"canal: {len(ponto)-1} metricas · hist={len(hist)}")

    perf["ultima_sincronizacao"]=now
    json.dump(perf,open("performance.json","w"),ensure_ascii=False,indent=1)
    print("performance.json atualizado")

if __name__=="__main__": main()
