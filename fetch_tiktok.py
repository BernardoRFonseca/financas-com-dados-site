#!/usr/bin/env python3
"""fetch_tiktok.py — robô TikTok (Display API, sandbox).
Refresca o access token, busca vídeos (match por #fcdNN) e seguidores,
e atualiza performance_tiktok.json PRESERVANDO os campos manuais
(saves, tempo_medio_s, pct_completo, novos_seguidores) que a API não dá.
Se o refresh token rodar, escreve new_refresh_token.txt para o workflow persistir."""
import os, json, re, sys, datetime, urllib.request, urllib.parse

CK=os.environ["TIKTOK_CLIENT_KEY"]; CS=os.environ["TIKTOK_CLIENT_SECRET"]
RT=os.environ["TIKTOK_REFRESH_TOKEN"]
HIST_MAX=2000

def post_form(url, data):
    body=urllib.parse.urlencode(data).encode()
    req=urllib.request.Request(url, data=body, headers={"Content-Type":"application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def post_json(url, token, data):
    req=urllib.request.Request(url, data=json.dumps(data).encode(),
        headers={"Content-Type":"application/json","Authorization":f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def get_json(url, token):
    req=urllib.request.Request(url, headers={"Authorization":f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def main():
    now=datetime.datetime.now().isoformat(timespec="minutes")

    # 1) refresh do access token
    tok=post_form("https://open.tiktokapis.com/v2/oauth/token/",
        {"client_key":CK,"client_secret":CS,"grant_type":"refresh_token","refresh_token":RT})
    access=tok.get("access_token")
    if not access:
        print("ERRO no refresh:", {k:v for k,v in tok.items() if "token" not in k}, file=sys.stderr)
        sys.exit(1)
    new_rt=tok.get("refresh_token")
    if new_rt and new_rt!=RT:
        open("new_refresh_token.txt","w").write(new_rt)
        print("refresh token rodou — será persistido pelo workflow")

    # 2) carregar JSON existente (preserva dados manuais)
    perf=json.load(open("performance_tiktok.json")) if os.path.exists("performance_tiktok.json") else {"plataforma":"tiktok","videos":{}}
    perf.setdefault("videos",{})
    perf["modo"]="api+manual"

    # 3) vídeos (paginação até 60)
    vids=[]; cursor=0; has_more=True; pages=0
    fields="id,create_time,video_description,duration,view_count,like_count,comment_count,share_count"
    while has_more and pages<3:
        d=post_json(f"https://open.tiktokapis.com/v2/video/list/?fields={fields}", access,
                    {"max_count":20, **({"cursor":cursor} if cursor else {})})
        data=d.get("data",{})
        vids+=data.get("videos",[])
        has_more=data.get("has_more",False); cursor=data.get("cursor",0); pages+=1

    n=0
    for v in vids:
        m=re.search(r"#fcd(\d+)", v.get("video_description") or "")
        if not m: continue
        vid=m.group(1)
        slot=perf["videos"].setdefault(vid,{})
        met=slot.setdefault("metricas",{})
        met["views"]=v.get("view_count",met.get("views"))
        met["likes"]=v.get("like_count",met.get("likes"))
        met["comentarios"]=v.get("comment_count",met.get("comentarios"))
        met["partilhas"]=v.get("share_count",met.get("partilhas"))
        # campos manuais preservados: saves, tempo_medio_s, pct_completo, novos_seguidores
        if not slot.get("publicado_em") and v.get("create_time"):
            slot["publicado_em"]=datetime.datetime.fromtimestamp(v["create_time"]).isoformat(timespec="minutes")
        if not slot.get("duracao_s") and v.get("duration"):
            slot["duracao_s"]=v["duration"]
        slot["atualizado"]=now
        hist=slot.setdefault("historico",[])
        hist.append({"t":now,"views":met.get("views"),"likes":met.get("likes"),
                     "comentarios":met.get("comentarios"),"partilhas":met.get("partilhas")})
        if len(hist)>HIST_MAX: del hist[:len(hist)-HIST_MAX]
        n+=1
    print(f"{n} vídeos com #fcd atualizados de {len(vids)} na conta")

    # 4) seguidores da conta (user.info.stats)
    try:
        u=get_json("https://open.tiktokapis.com/v2/user/info/?fields=follower_count,video_count", access)
        st=(u.get("data",{}) or {}).get("user",{})
        if "follower_count" in st:
            canal=perf.setdefault("canal",{})
            hist=canal.setdefault("historico",[])
            hist.append({"t":now,"seguidores":st["follower_count"],"publicacoes":st.get("video_count")})
            if len(hist)>HIST_MAX: del hist[:len(hist)-HIST_MAX]
            print(f"canal TT: {st['follower_count']} seguidores")
    except Exception as e:
        print("user.info.stats falhou (não fatal):", e, file=sys.stderr)

    perf["ultima_atualizacao"]=now
    json.dump(perf, open("performance_tiktok.json","w"), ensure_ascii=False, indent=1)
    print("performance_tiktok.json atualizado")

if __name__=="__main__": main()
