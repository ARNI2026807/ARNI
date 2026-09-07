import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import re


st.set_page_config(page_title="ARNI", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

# =========================================================
# ARNI ÜYELİK / GİRİŞ SİSTEMİ
# Kullanıcılar GitHub koduna yazılmaz.
# Streamlit Community Cloud > App settings > Secrets bölümünden yönetilir.
# =========================================================
import hmac

def _arni_users():
    try:
        users = st.secrets.get("users", {})
        return dict(users)
    except Exception:
        return {}

def _arni_login():
    if st.session_state.get("arni_logged_in", False):
        return True

    st.markdown("""
    <style>
    .stApp {background:#f7f9fc;}
    .arni-login-box{
        max-width:440px;
        margin:8vh auto 0 auto;
        padding:30px 28px;
        background:#ffffff;
        border:1px solid #d9e2ec;
        border-radius:22px;
        box-shadow:0 12px 36px rgba(15,23,42,.10);
    }
    .arni-login-logo{
        font-size:38px;
        font-weight:800;
        text-align:center;
        color:#0f172a;
    }
    .arni-login-sub{
        text-align:center;
        color:#64748b;
        margin:6px 0 18px;
    }
    </style>
    <div class="arni-login-box">
      <div class="arni-login-logo">📈 ARNI</div>
      <div class="arni-login-sub">Üye Girişi</div>
    </div>
    """, unsafe_allow_html=True)

    users = _arni_users()

    if not users:
        st.error("Üyelik sistemi henüz ayarlanmadı. Streamlit Secrets bölümüne kullanıcı eklenmeli.")
        st.stop()

    with st.form("arni_login_form", clear_on_submit=False):
        username = st.text_input("Kullanıcı adı", placeholder="Kullanıcı adınızı girin")
        password = st.text_input("Şifre", type="password", placeholder="Şifrenizi girin")
        submitted = st.form_submit_button("Giriş Yap", type="primary", use_container_width=True)

    if submitted:
        expected = users.get(username.strip())
        if expected is not None and hmac.compare_digest(str(expected), str(password)):
            st.session_state["arni_logged_in"] = True
            st.session_state["arni_username"] = username.strip()
            st.rerun()
        else:
            st.error("Kullanıcı adı veya şifre yanlış.")

    st.caption("🔒 ARNI yalnızca yetkili üyeler içindir.")
    return False

if not _arni_login():
    st.stop()

st.markdown("""
<style>
:root {--bg:#05080d;--panel:#0b111b;--panel2:#101826;--border:#26364a;--text:#ffffff;--muted:#aebdce;--blue:#2f80ff;--green:#00e676;--yellow:#ffd600;--orange:#ff9800;--red:#ff1744;}
html,body,[class*="css"]{font-family:Inter,Arial,sans-serif}.stApp{background:var(--bg);color:var(--text)}
[data-testid="stHeader"]{background:var(--bg)!important}.block-container{max-width:1540px;padding-top:.8rem;padding-bottom:2rem}
[data-testid="stSidebar"]{background:#080d14!important;border-right:1px solid #26364a}[data-testid="stSidebar"] *{color:#f4f7fb!important}
h1,h2,h3,h4{color:#f8fbff!important}p,label{color:#dbe5f0!important}
.stTextInput input{min-height:48px;border-radius:11px!important;background:#f5f7fa!important;color:#101828!important}
div[data-baseweb="select"]>div{min-height:48px;background:#f5f7fa!important;color:#101828!important;border-radius:11px!important}
div[data-baseweb="select"] span{color:#101828!important}
[data-testid="stMetric"]{background:var(--panel2);border:1px solid var(--border);border-radius:14px;padding:14px;min-height:108px}
[data-testid="stMetricLabel"]{color:#a9bbcf!important}[data-testid="stMetricValue"]{color:#fff!important;font-weight:800!important}[data-testid="stMetricDelta"]{font-weight:700!important}
.stButton>button{width:100%;border-radius:11px;min-height:44px;font-weight:750}[data-testid="stAlert"]{border-radius:12px}
.arni-hero{background:linear-gradient(135deg,#0c2138 0%,#0c1728 100%);border:1px solid #18476f;border-radius:18px;padding:18px 22px;margin-bottom:14px}
.arni-title{font-size:34px;font-weight:900;color:#fff}.arni-sub{color:#9fb4ca;font-size:14px}
.stock-mini{background:#0d1520;border:1px solid #26364a;border-radius:14px;padding:12px;min-height:96px}.stock-mini .sym{font-size:13px;color:#c9d6e5;font-weight:800}.stock-mini .price{font-size:22px;color:#fff;font-weight:900;margin-top:4px}.stock-mini .pos{color:#00e676;font-weight:800;margin-top:4px}.stock-mini .neg{color:#ff1744;font-weight:800;margin-top:4px}
.stock-head{background:#0d1520;border:1px solid #26364a;border-radius:16px;padding:16px;margin-bottom:10px}.stock-name{color:#b9c9da;font-size:14px;font-weight:700}.stock-price{color:#fff;font-size:32px;font-weight:900}.stock-score{font-size:26px;color:#fff;font-weight:900}
.signal-buy,.signal-watch,.signal-wait,.signal-sell{text-align:center;border-radius:10px;padding:10px 12px;font-weight:900;margin-top:10px}.signal-buy{background:rgba(0,230,118,.18);border:1px solid #00e676;color:#00e676}.signal-watch{background:rgba(255,152,0,.18);border:1px solid #ff9800;color:#ffb74d}.signal-wait{background:rgba(255,214,0,.15);border:1px solid #ffd600;color:#ffe45c}.signal-sell{background:rgba(255,23,68,.18);border:1px solid #ff1744;color:#ff5c77}.small-note{color:#91a6bb;font-size:12px}hr{border-color:#17344e}
</style>
""", unsafe_allow_html=True)

HISSELER=sorted(["AEFES","AKBNK","AKSA","AKSEN","ALARK","ALFAS","ARCLK","ASELS","ASTOR","BIMAS","BRSAN","CCOLA","CIMSA","DOAS","EKGYO","ENJSA","ENKAI","EREGL","FROTO","GARAN","GESAN","GUBRF","HALKB","HATSN","HEKTS","ISCTR","KARSN","KCHOL","KONTR","KRDMD","MGROS","ODAS","OYAKC","PETKM","PGSUS","SAHOL","SASA","SISE","SKYMD","SOKE","TABGD","TAVHL","TBORG","TCELL","THYAO","TKFEN","TOASO","TSKB","TUPRS","ULKER","VAKBN","VESBE","YKBNK","YEOTK","ZOREN"])
POPULER=["THYAO","TUPRS","ASELS","KCHOL","SAHOL","SISE","PETKM","TAVHL","ASTOR","ISCTR"]
ABD={"AAPL","TSLA","NVDA","MSFT","GOOGL","AMZN"}
ISIM_SOZLUGU={"tüpraş":"TUPRS","tupras":"TUPRS","aselsan":"ASELS","thy":"THYAO","türk hava yolları":"THYAO","turk hava yollari":"THYAO","akbank":"AKBNK","halkbank":"HALKB","iş bankası":"ISCTR","is bankasi":"ISCTR","garanti":"GARAN","pegasus":"PGSUS","ereğli":"EREGL","eregli":"EREGL","şişecam":"SISE","sisecam":"SISE","koç":"KCHOL","koc":"KCHOL","sabancı":"SAHOL","sabanci":"SAHOL","bim":"BIMAS","bimaş":"BIMAS","söke":"SOKE","soke":"SOKE","skymd":"SKYMD","astor":"ASTOR","petkim":"PETKM","tav":"TAVHL","tavhl":"TAVHL","tuborg":"TBORG","yeotk":"YEOTK","karsan":"KARSN","migros":"MGROS"}

def kod_yap(girdi):
    if not girdi:return None
    girdi=str(girdi).strip()
    if not girdi:return None
    kod=ISIM_SOZLUGU.get(girdi.lower(),girdi.upper())
    kod=re.sub(r"[^A-Z0-9.]","",kod)
    if kod in ABD:return kod
    return kod if kod.endswith(".IS") else kod+".IS"

@st.cache_data(ttl=60,show_spinner=False)
def veri_getir(kod,gun=60):
    try:
        df=yf.download(kod,period=f"{gun}d",interval="1d",progress=False,auto_adjust=False,threads=False)
        if df is None or df.empty:return pd.DataFrame()
        if isinstance(df.columns,pd.MultiIndex):df.columns=df.columns.get_level_values(0)
        return df.dropna(subset=["Close"])
    except Exception:return pd.DataFrame()

def rsi_hesapla(close,period=14):
    delta=close.diff();gain=delta.clip(lower=0);loss=-delta.clip(upper=0)
    ag=gain.ewm(alpha=1/period,adjust=False).mean();al=loss.ewm(alpha=1/period,adjust=False).mean();rs=ag/al.replace(0,np.nan)
    return 100-(100/(1+rs))

def analiz_et(kod,gun,risk_esigi):
    df=veri_getir(kod,gun)
    if df.empty or len(df)<5:return None,df
    close=df["Close"].astype(float);fiyat=float(close.iloc[-1]);onceki=float(close.iloc[-2]);gunluk=((fiyat-onceki)/onceki)*100 if onceki else 0.0
    ma20=float(close.rolling(min(20,len(close))).mean().iloc[-1]);ma50=float(close.rolling(min(50,len(close))).mean().iloc[-1])
    rs=rsi_hesapla(close).dropna();rsi=float(rs.iloc[-1]) if len(rs) else 50.0
    ret=close.pct_change().dropna();vol=float(ret.std()*np.sqrt(252)*100) if len(ret)>1 else 0.0
    son20=df.tail(min(20,len(df)));destek=float(son20["Low"].min());direnc=float(son20["High"].max())
    tr=pd.concat([df["High"]-df["Low"],(df["High"]-df["Close"].shift()).abs(),(df["Low"]-df["Close"].shift()).abs()],axis=1).max(axis=1)
    atrs=tr.rolling(14).mean().dropna();atr=float(atrs.iloc[-1]) if len(atrs) else fiyat*0.02
    stop=max(0,fiyat-1.5*atr);hedef=fiyat+1.5*atr
    skor=50;skor+=12 if fiyat>ma20 else -12;skor+=10 if fiyat>ma50 else -10;skor+=8 if ma20>ma50 else -5
    if gunluk>=3:skor+=8
    elif gunluk>=1:skor+=5
    elif gunluk>0:skor+=2
    elif gunluk<=-3:skor-=10
    else:skor-=5
    if 52<=rsi<=65:skor+=10
    elif 45<=rsi<52:skor+=3
    elif 65<rsi<=72:skor+=4
    elif rsi>75:skor-=10
    elif rsi<30:skor-=5
    if vol>risk_esigi:skor-=8
    skor=int(max(0,min(100,skor)))
    sinyal="AL" if skor>=75 else "AL İZLE" if skor>=62 else "BEKLE" if skor>=42 else "ZAYIF / SAT"
    return {"kod":kod,"fiyat":fiyat,"gunluk":gunluk,"rsi":rsi,"ma20":ma20,"ma50":ma50,"volatilite":vol,"destek":destek,"direnc":direnc,"hedef":hedef,"stop":stop,"skor":skor,"sinyal":sinyal},df

with st.sidebar:
    st.caption(f"👤 Üye: **{st.session_state.get('arni_username','')}**")
    if st.button("🚪 Çıkış Yap", use_container_width=True, key="arni_logout"):
        st.session_state["arni_logged_in"] = False
        st.session_state.pop("arni_username", None)
        st.rerun()
    st.divider()
    st.markdown("## 📈 ARNI");st.caption("Akıllı Borsa Analiz Asistanı");st.divider();st.markdown("### Analiz Ayarları")
    zaman_penceresi=st.slider("Zaman Aralığı (Gün)",20,365,60,5);risk_esigi=st.slider("Risk / Volatilite Eşiği",10,70,35,1)
    st.divider();st.markdown("### Sinyal Renkleri");st.success("AL");st.warning("AL İZLE");st.info("BEKLE");st.error("ZAYIF / SAT")

st.markdown('<div class="arni-hero"><div class="arni-title">📈 ARNI</div><div class="arni-sub">Piyasa her zaman konuşur, ARNI senin için analiz eder.</div></div>',unsafe_allow_html=True)

st.markdown("### Piyasa Özeti")
market_items=[("^XU100","BIST 100",""),("USDTRY=X","Dolar / TL","₺"),("EURTRY=X","Euro / TL","₺"),("GC=F","Ons Altın","$"),("BZ=F","Brent Petrol","$")]
mc=st.columns(5)
for i,(ticker,label,unit) in enumerate(market_items):
    try:
        d=yf.download(ticker,period="5d",progress=False,auto_adjust=False,threads=False)
        if isinstance(d.columns,pd.MultiIndex):d.columns=d.columns.get_level_values(0)
        if len(d)>=2:
            son=float(d["Close"].iloc[-1]);onceki=float(d["Close"].iloc[-2]);deg=((son-onceki)/onceki)*100
            mc[i].metric(label,f"{unit}{son:,.2f}",f"{deg:+.2f}%")
        else:mc[i].metric(label,"—")
    except Exception:mc[i].metric(label,"—")

st.markdown("### 🔥 Popüler Hisseler")
pop_cols=st.columns(5)
for idx,kod in enumerate(POPULER):
    d=veri_getir(kod+".IS",10);col=pop_cols[idx%5]
    with col:
        if not d.empty and len(d)>=2:
            fiyat=float(d["Close"].iloc[-1]);prev=float(d["Close"].iloc[-2]);deg=((fiyat-prev)/prev)*100 if prev else 0.0;cls="pos" if deg>=0 else "neg"
            st.markdown(f'<div class="stock-mini"><div class="sym">{kod}</div><div class="price">₺{fiyat:,.2f}</div><div class="{cls}">{deg:+.2f}%</div></div>',unsafe_allow_html=True)
        else:st.markdown(f'<div class="stock-mini"><div class="sym">{kod}</div><div class="price">—</div></div>',unsafe_allow_html=True)

st.markdown("---");st.markdown("## ⚖️ Hisse Karşılaştırma")
if "stock1" not in st.session_state:st.session_state.stock1="SAHOL"
if "stock2" not in st.session_state:st.session_state.stock2="SISE"

s1,s2=st.columns(2)
with s1:
    secim1=st.selectbox("1. Hisse",HISSELER,index=HISSELER.index(st.session_state.stock1),key="select1")
    elle1=st.text_input("Veya kod / isim yaz",placeholder="Örnek: ASTOR, TUPRS",key="manual1")
with s2:
    secim2=st.selectbox("2. Hisse",HISSELER,index=HISSELER.index(st.session_state.stock2),key="select2")
    elle2=st.text_input("Veya ikinci kod / isim yaz",placeholder="Örnek: ISCTR, BIMAS",key="manual2")

girdi1=elle1.strip() if elle1.strip() else secim1;girdi2=elle2.strip() if elle2.strip() else secim2
kod1=kod_yap(girdi1);kod2=kod_yap(girdi2);sonuc1,veri1=analiz_et(kod1,zaman_penceresi,risk_esigi);sonuc2,veri2=analiz_et(kod2,zaman_penceresi,risk_esigi)
st.info(f"Analiz edilen hisseler: {kod1.replace('.IS','')} ↔ {kod2.replace('.IS','')}")

def sonuc_karti(sonuc):
    if sonuc is None:st.error("Veri alınamadı.");return
    kod=sonuc["kod"];para="₺" if kod.endswith(".IS") else "$";sembol=kod.replace(".IS","")
    cls="signal-buy" if sonuc["sinyal"]=="AL" else "signal-watch" if sonuc["sinyal"]=="AL İZLE" else "signal-wait" if sonuc["sinyal"]=="BEKLE" else "signal-sell"
    html=(f'<div class="stock-head"><div style="display:flex;justify-content:space-between;gap:12px;">'
          f'<div><div class="stock-name">{sembol}</div><div class="stock-price">{para}{sonuc["fiyat"]:,.2f}</div><div class="small-note">Günlük: {sonuc["gunluk"]:+.2f}%</div></div>'
          f'<div class="stock-score">{sonuc["skor"]}/100</div></div><div class="{cls}">{sonuc["sinyal"]}</div></div>')
    st.markdown(html,unsafe_allow_html=True)
    st.caption(f'RSI {sonuc["rsi"]:.1f}  •  Destek {para}{sonuc["destek"]:,.2f}  •  Direnç {para}{sonuc["direnc"]:,.2f}  •  Hedef {para}{sonuc["hedef"]:,.2f}  •  Stop {para}{sonuc["stop"]:,.2f}')

left,mid,right=st.columns([1,1,1.35])
with left:sonuc_karti(sonuc1)
with mid:sonuc_karti(sonuc2)
with right:
    st.markdown("### Performans Karşılaştırması")
    if not veri1.empty and not veri2.empty:
        c1=veri1["Close"].dropna();c2=veri2["Close"].dropna()
        if len(c1) and len(c2):
            p1=((c1/float(c1.iloc[0]))-1)*100;p2=((c2/float(c2.iloc[0]))-1)*100;graf=pd.concat([p1.rename(kod1.replace(".IS","")),p2.rename(kod2.replace(".IS",""))],axis=1);st.line_chart(graf,height=360)
        else:st.info("Grafik için yeterli veri yok.")
    else:st.info("Grafik için veri alınamadı.")

st.markdown("---");st.markdown("## 🤖 ARNI'ye Sor");st.caption("Hisse senetleri hakkında sorun; teknik göstergeleri özetleyeyim.")
q1,q2=st.columns([5,1])
with q1:soru=st.text_input("ARNI sorusu",placeholder="Ör: ASTOR alınır mı? TUPRS gidişatı nasıl? THYAO teknik analiz...",key="arni_soru_alt",label_visibility="collapsed")
with q2:sor_buton=st.button("Gönder",type="primary",key="arni_gonder")
if sor_buton and soru.strip():
    lower=soru.lower();bulunan=None
    for isim,ticker in ISIM_SOZLUGU.items():
        if isim in lower:bulunan=ticker;break
    if bulunan is None:
        for token in re.findall(r"\b[A-Z]{4,6}\b",soru.upper()):
            if token in HISSELER or token in ABD:bulunan=token;break
    if bulunan is None:st.warning("Soruda bir hisse kodu bulamadım. Örnek: ASTOR, TUPRS, THYAO.")
    else:
        soru_kod=bulunan if bulunan in ABD else bulunan+".IS";soru_sonuc,_=analiz_et(soru_kod,zaman_penceresi,risk_esigi)
        if soru_sonuc is None:st.error(f"{bulunan} için veri alınamadı.")
        else:
            para="₺" if soru_kod.endswith(".IS") else "$";st.markdown(f"### {bulunan} Analizi")
            a,b,c,d=st.columns(4);a.metric("Fiyat",f'{para}{soru_sonuc["fiyat"]:,.2f}',f'{soru_sonuc["gunluk"]:+.2f}%');b.metric("ARNI Skoru",f'{soru_sonuc["skor"]}/100');c.metric("RSI",f'{soru_sonuc["rsi"]:.1f}');d.metric("Volatilite",f'%{soru_sonuc["volatilite"]:.1f}')
            if soru_sonuc["sinyal"]=="AL":st.success("ARNI sinyali: AL")
            elif soru_sonuc["sinyal"]=="AL İZLE":st.warning("ARNI sinyali: AL İZLE")
            elif soru_sonuc["sinyal"]=="BEKLE":st.info("ARNI sinyali: BEKLE")
            else:st.error("ARNI sinyali: ZAYIF / SAT")
            st.write(f'Destek **{para}{soru_sonuc["destek"]:,.2f}** · Direnç **{para}{soru_sonuc["direnc"]:,.2f}** · Hedef **{para}{soru_sonuc["hedef"]:,.2f}** · Stop **{para}{soru_sonuc["stop"]:,.2f}**')

st.markdown("---");st.caption("ARNI teknik analiz aracıdır. Yahoo Finance verileri gecikmeli olabilir. Yatırım tavsiyesi değildir.")
