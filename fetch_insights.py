#!/usr/bin/env python3
"""v2 — snapshot + HISTORICO: cada corrida acrescenta um ponto à série temporal de cada vídeo.
Desenhado para falhar com elegância: métricas indisponíveis são ignoradas, nunca apagam dados."""
import os, json, urllib.request, urllib.parse, sys, datetime

TOKEN=os.environ["IG_ACCESS_TOKEN"]; IG_USER=os.environ["IG_USER_ID"]
API="https://graph.facebook.com/v21.0"
METRICS=["views","reach","likes","comments","shares","saved","total_interactions","ig_reels_avg_watch_time"]
KEYMAP={"views":"views","reach":"alcance","likes":"likes","comments":"comentarios",
        "shares":"partilhas","saved":"saves","ig_reels_avg_watch_time":"tempo_medio_s"}
HIST_KEYS=["views","alcance","likes","comentarios","partilhas","saves"]  # o que entra na série temporal
HIST_MAX=2000  # ~5 meses a 12 pontos/dia

def get(url, params):
    params["access_token"]=TOKEN
    full=url+"?"+urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(full, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        print("API error:", e.code, e.read().decode()[:400], file=sys.stderr)
        raise

def media_list():
    data=get(f"{API}/{IG_USER}/media",{"fields":"id,permalink,timestamp,media_type","limit":"50"})
    return data.get("data",[])

def insights(media_id):
    vals={}
    for m in METRICS:
        try:
            d=get(f"{API}/{media_id}/insights",{"metric":m})
            for item in d.get("data",[]):
                v=item.get("values",[{}])[0].get("value")
                if isinstance(v,(int,float)): vals[item["name"]]=v
        except Exception as e:
            print(f"  metrica {m}: indisponivel", file=sys.stderr)
    return vals

def main():
    mapping=json.load(open("mapping.json"))
    mapping={k:v for k,v in mapping.items() if not k.startswith("_")}
    perf_path="performance.json"
    perf=json.load(open(perf_path)) if os.path.exists(perf_path) else {}
    perf.setdefault("videos",{})
    now=datetime.datetime.now().isoformat(timespec="minutes")
    for m in media_list():
        code=m.get("permalink","").rstrip("/").split("/")[-1]
        if code not in mapping: continue
        vid=str(mapping[code])
        vals=insights(m["id"])
        slot=perf["videos"].setdefault(vid,{})
        met=slot.setdefault("metricas",{})
        for api_k,out_k in KEYMAP.items():
            if api_k in vals:
                v=vals[api_k]
                met[out_k]=round(v/1000,1) if api_k=="ig_reels_avg_watch_time" else v
        slot["atualizado"]=now
        # série temporal: um ponto por corrida
        hist=slot.setdefault("historico",[])
        ponto={"t":now}
        ponto.update({k:met[k] for k in HIST_KEYS if k in met})
        hist.append(ponto)
        if len(hist)>HIST_MAX: del hist[:len(hist)-HIST_MAX]
        print(f"video {vid} ({code}): {len(vals)} metricas · historico={len(hist)} pontos")
    perf["ultima_sincronizacao"]=now
    json.dump(perf,open(perf_path,"w"),ensure_ascii=False,indent=1)
    print("performance.json atualizado")

if __name__=="__main__": main()
