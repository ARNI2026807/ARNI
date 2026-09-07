import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import re

st.set_page_config(page_title="ARNI", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
:root{--bg:#f7f9fc;--panel:#ffffff;--panel2:#f8fafc;--border:#dce4ee;--text:#101828;--muted:#667085;--blue:#2878d8;--green:#36b37e;--watch:#4a90e2;--wait:#e58a32;--red:#e84d5b;}
html,body,[class*="css"]{font-family:Inter,Arial,sans-serif}.stApp{background:var(--bg);color:var(--text)}
[data-testid="stHeader"]{background:var(--bg)!important}.block-container{max-width:1540px;padding-top:.8rem;padding-bottom:2rem}
[data-testid="stSidebar"]{background:#fff!important;border-right:1px solid var(--border)}[data-testid="stSidebar"] *{color:#172033!important}
h1,h2,h3,h4{color:#111827!important}p,label{color:#344054!important}
.stTextInput input{min-height:48px;border-radius:11px!important;background:#fff!important;color:#101828!important;border:1px solid #d7dee8!important}
div[data-baseweb="select"]>div{min-height:48px;background:#fff!important;color:#101828!important;border-radius:11px!important;border:1px solid #d7dee8!important}div[data-baseweb="select"] span{color:#101828!important}
[data-testid="stMetric"]{background:#fff;border:1px solid var(--border);border-radius:14px;padding:14px;min-height:108px;box-shadow:0 2px 8px rgba(16,24,40,.04)}
[data-testid="stMetricLabel"]{color:#667085!important}[data-testid="stMetricValue"]{color:#101828!important;font-weight:800!important}[data-testid="stMetricDelta"]{font-weight:700!important}
.stButton>button{width:100%;border-radius:11px;min-height:44px;font-weight:750;background:#2878d8;color:#fff;border:0}[data-testid="stAlert"]{border-radius:12px}
.arni-hero{background:#fff;border:1px solid var(--border);border-radius:18px;padding:18px 22px;margin-bottom:14px;box-shadow:0 2px 10px rgba(16,24,40,.04)}.arni-title{font-size:34px;font-weight:900;color:#123b70}.arni-sub{color:#667085;font-size:14px}
.stock-mini{background:#fff;border:1px solid var(--border);border-radius:14px;padding:12px;min-height:96px;box-shadow:0 2px 8px rgba(16,24,40,.04)}.stock-mini .sym{font-size:13px;color:#475467;font-weight:800}.stock-mini .price{font-size:22px;color:#101828;font-weight:900;margin-top:4px}.stock-mini .pos{color:#36a676;font-weight:800;margin-top:4px}.stock-mini .neg{color:#df5360;font-weight:800;margin-top:4px}
.stock-head{background:#fff;border:1px solid var(--border);border-radius:16px;padding:14px;margin-bottom:10px;box-shadow:0 2px 8px rgba(16,24,40,.04)}.stock-name{color:#475467;font-size:14px;font-weight:700}.stock-price{color:#101828;font-size:28px;font-weight:900}.stock-score{font-size:26px;color:#101828;font-weight:900}
.signal-buy,.signal-watch,.signal-wait,.signal-sell{text-align:center;border-radius:10px;padding:10px 12px;font-weight:900;margin-top:10px}.signal-buy{background:#edf8f3;border:1px solid #72c9a8;color:#257a5d}.signal-watch{background:#eef5fd;border:1px solid #8db8ea;color:#356fae}.signal-wait{background:#fff5e9;border:1px solid #edb675;color:#a96120}.signal-sell{background:#fceff1;border:1px solid #ed8d97;color:#ad3946}.small-note{color:#667085;font-size:12px}hr{border-color:#dce4ee}
.market-card{background:#fff;border:1px solid var(--border);border-radius:14px;padding:14px 18px;min-height:132px;box-shadow:0 2px 8px rgba(16,24,40,.04)}.market-label{font-size:16px;color:#344054;margin-bottom:14px}.market-price{font-size:28px;line-height:1.1;color:#101828;font-weight:800;white-space:nowrap}.market-delta{display:inline-block;margin-top:12px;padding:4px 9px;border-radius:999px;font-size:15px;font-weight:800}.market-up{background:#dff7e8;color:#267a52}.market-down{background:#fde7e8;color:#b23c45}.market-flat{background:#eef2f6;color:#667085}
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
    st.markdown("## 📈 ARNI");st.caption("Akıllı Borsa Analiz Asistanı");st.divider();st.markdown("### Analiz Ayarları")
    zaman_penceresi=st.slider("Zaman Aralığı (Gün)",20,365,60,5);risk_esigi=st.slider("Risk / Volatilite Eşiği",10,70,35,1)
    st.divider();st.markdown("### Sinyal Renkleri")
    st.markdown('<div class="signal-buy" style="text-align:left">🟢 &nbsp; AL</div>',unsafe_allow_html=True)
    st.markdown('<div class="signal-watch" style="text-align:left">🔵 &nbsp; AL İZLE</div>',unsafe_allow_html=True)
    st.markdown('<div class="signal-wait" style="text-align:left">🟠 &nbsp; BEKLE</div>',unsafe_allow_html=True)
    st.markdown('<div class="signal-sell" style="text-align:left">🔴 &nbsp; ZAYIF / SAT</div>',unsafe_allow_html=True)
    st.divider(); karanlik=st.toggle("🌙 Karanlık Mod", value=False, key="dark_mode")

if karanlik:
    st.markdown("""<style>
    .stApp{background:#111827!important;color:#f8fafc!important}
    [data-testid="stHeader"]{background:#111827!important}
    [data-testid="stSidebar"]{background:#172033!important;border-right-color:#334155!important}
    [data-testid="stSidebar"] *{color:#f8fafc!important}
    h1,h2,h3,h4{color:#ffffff!important}
    p,label,.stCaption{color:#d7e0ea!important}

    .arni-hero,.stock-mini,.stock-head,.market-card,[data-testid="stMetric"]{
        background:#1f2a3d!important;
        border-color:#3a4b63!important;
        box-shadow:0 2px 10px rgba(0,0,0,.18)!important
    }
    .arni-title,.stock-mini .price,.stock-price,.stock-score,.market-price,[data-testid="stMetricValue"]{
        color:#ffffff!important
    }
    .arni-sub,.stock-mini .sym,.stock-name,.small-note,.market-label,[data-testid="stMetricLabel"]{
        color:#cbd5e1!important
    }

    .stTextInput input,div[data-baseweb="select"]>div{
        background:#f8fafc!important;
        color:#111827!important;
        border-color:#94a3b8!important
    }
    .stTextInput input::placeholder{color:#64748b!important;opacity:1!important}
    div[data-baseweb="select"] span{color:#111827!important}

    [data-testid="stSidebar"] .signal-buy{background:#dff4ea!important;border-color:#63c69e!important;color:#1d5f49!important}
    [data-testid="stSidebar"] .signal-watch{background:#e5effc!important;border-color:#7aaee7!important;color:#285f9f!important}
    [data-testid="stSidebar"] .signal-wait{background:#fff0df!important;border-color:#e3a663!important;color:#93551d!important}
    [data-testid="stSidebar"] .signal-sell{background:#fbe5e8!important;border-color:#e87986!important;color:#9d3340!important}
    [data-testid="stSidebar"] .signal-buy *,
    [data-testid="stSidebar"] .signal-watch *,
    [data-testid="stSidebar"] .signal-wait *,
    [data-testid="stSidebar"] .signal-sell *{color:inherit!important}

    .market-up{background:#dff4ea!important;color:#216b50!important}
    .market-down{background:#fbe5e8!important;color:#a43743!important}
    .market-flat{background:#e7edf4!important;color:#475569!important}
    </style>""",unsafe_allow_html=True)

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
            delta_class="market-up" if deg>0 else "market-down" if deg<0 else "market-flat"
            arrow="↑" if deg>0 else "↓" if deg<0 else "→"
            mc[i].markdown(
                f'<div class="market-card"><div class="market-label">{label}</div>'
                f'<div class="market-price">{unit}{son:,.2f}</div>'
                f'<div class="market-delta {delta_class}">{arrow} {deg:+.2f}%</div></div>',
                unsafe_allow_html=True
            )
        else:
            mc[i].markdown(f'<div class="market-card"><div class="market-label">{label}</div><div class="market-price">—</div></div>',unsafe_allow_html=True)
    except Exception:
        mc[i].markdown(f'<div class="market-card"><div class="market-label">{label}</div><div class="market-price">—</div></div>',unsafe_allow_html=True)

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
    if sonuc is None:
        st.error("Veri alınamadı.")
        return
    kod=sonuc["kod"]; para="₺" if kod.endswith(".IS") else "$"; sembol=kod.replace(".IS","")
    cls="signal-buy" if sonuc["sinyal"]=="AL" else "signal-watch" if sonuc["sinyal"]=="AL İZLE" else "signal-wait" if sonuc["sinyal"]=="BEKLE" else "signal-sell"
    html=(f'<div class="stock-head"><div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;">'
          f'<div><div class="stock-name">{sembol}</div><div class="stock-price">{para}{sonuc["fiyat"]:,.2f}</div>'
          f'<div class="small-note">Günlük: {sonuc["gunluk"]:+.2f}%</div></div>'
          f'<div class="stock-score">{sonuc["skor"]}/100</div></div><div class="{cls}">{sonuc["sinyal"]}</div></div>')
    st.markdown(html,unsafe_allow_html=True)

left,right=st.columns(2)
with left:
    sonuc_karti(sonuc1)
with right:
    sonuc_karti(sonuc2)

st.markdown("### 📊 Performans Karşılaştırması")
if not veri1.empty and not veri2.empty:
    c1=veri1["Close"].dropna(); c2=veri2["Close"].dropna()
    if len(c1) and len(c2):
        p1=((c1/float(c1.iloc[0]))-1)*100
        p2=((c2/float(c2.iloc[0]))-1)*100
        graf=pd.concat([p1.rename(kod1.replace(".IS","")),p2.rename(kod2.replace(".IS",""))],axis=1)
        st.line_chart(graf,height=330,use_container_width=True)
    else:
        st.info("Grafik için yeterli veri yok.")
else:
    st.info("Grafik için veri alınamadı.")

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
