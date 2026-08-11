#!/usr/bin/env python3
"""Vai buscar métricas dos Reels à Instagram Graph API e atualiza performance.json.
Desenhado para falhar com elegância: métricas indisponíveis são ignoradas, nunca apagam dados existentes."""
import os, json, urllib.request, urllib.parse, sys, datetime

TOKEN=os.environ["IG_ACCESS_TOKEN"]; IG_USER=os.environ["IG_USER_ID"]
API="https://graph.facebook.com/v21.0"
# métricas a tentar (a Meta renomeia com frequência — falhas individuais são ignoradas)
METRICS=["views","reach","likes","comments","shares","saved","total_interactions","ig_reels_avg_watch_time"]
# mapeia nomes da API -> chaves do performance.json do dashboard (ajustar às chaves do teu dashboard)
KEYMAP={"views":"views","reach":"alcance","likes":"likes","comments":"comentarios",
        "shares":"partilhas","saved":"saves","ig_reels_avg_watch_time":"tempo_medio_s"}

def get(url, params):
    params["access_token"]=TOKEN
    with urllib.request.urlopen(url+"?"+urllib.parse.urlencode(params), timeout=30) as r:
        return json.load(r)

def media_list():
    out=[]; url=f"{API}/{IG_USER}/media"
    data=get(url,{"fields":"id,permalink,timestamp,media_type","limit":"50"})
    out+=data.get("data",[])
    return out

def insights(media_id):
    vals={}
    for m in METRICS:
        try:
            d=get(f"{API}/{media_id}/insights",{"metric":m})
            for item in d.get("data",[]):
                v=item.get("values",[{}])[0].get("value")
                if isinstance(v,(int,float)): vals[item["name"]]=v
        except Exception as e:
            print(f"  metrica {m}: indisponivel ({e})", file=sys.stderr)
    return vals

def main():
    mapping=json.load(open("mapping.json"))          # {"SHORTCODE": video_id}
    perf_path="performance.json"
    perf=json.load(open(perf_path)) if os.path.exists(perf_path) else {}
    perf.setdefault("videos",{})
    medias=media_list()
    for m in medias:
        code=m.get("permalink","").rstrip("/").split("/")[-1]
        if code not in mapping: continue
        vid=str(mapping[code])
        vals=insights(m["id"])
        slot=perf["videos"].setdefault(vid,{})
        met=slot.setdefault("metricas",{})
        for api_k,out_k in KEYMAP.items():
            if api_k in vals:
                v=vals[api_k]
                met[out_k]=round(v/1000,1) if api_k=="ig_reels_avg_watch_time" else v  # ms->s
        slot["atualizado"]=datetime.date.today().isoformat()
        print(f"video {vid} ({code}): {len(vals)} metricas")
    perf["ultima_sincronizacao"]=datetime.datetime.now().isoformat(timespec="minutes")
    json.dump(perf,open(perf_path,"w"),ensure_ascii=False,indent=1)
    print("performance.json atualizado")

if __name__=="__main__": main()
