
from statistics import mean, median,variance,stdev
from itertools import accumulate
from ortoolpy import stable_matching
from pandas import DataFrame,Series
import pandas as pd
import numpy as np

#最終データをまとめるようーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
Desired_realization=[]  #希望実現度評価
Standard_deviation=[]   #成績平準度評価
Priority_grade=[]       #成績別優先度評価
Unwanted_students=[]    #希望外の学生の平均を最後に出すよう


N=50   #試行回数


#shuffled関数の定義ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
def shuffled(n):
    """0..n-1をシャッフルして返す"""
    a = np.arange(n)
    np.random.shuffle(a)
    return a.tolist()

#shuffled2関数の定義(２割は４倍の人気がある，1,2）ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
def shuffled2(n):
    """0..n-1をシャッフルして返す"""
    a = np.arange(n)
    b = np.ones(3)
    c = np.zeros(3)
    d=np.concatenate([a,b,c])
    np.random.shuffle(d)
    e=[]
    for i in range(len(d)):
        if int(d[i]) not in e:
            e.append(int(d[i]))
    return e

#shuffled3関数の定義(２割は４倍の人気がない，９，１０）ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
def shuffled3(n):
    """0..n-1をシャッフルして返す"""
    a = np.arange(n)
    b = np.ones(3)
    c = np.zeros(3)
    d = np.ones(3)+1
    e = np.ones(3)+2
    f = np.ones(3)+3
    g = np.ones(3)+4
    h = np.ones(3)+5
    j = np.ones(3)+6
    k=np.concatenate([a,b,c,d,e,f,g,h,j,])
    np.random.shuffle(k)
    z=[]
    for i in range(len(k)):
        if int(k[i]) not in z:
            z.append(int(k[i]))
    return z

#shuffled4関数の定義(1割は４倍の人気がない１割は４倍人気がある，９，１０）ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
def shuffled4(n):
    """0..n-1をシャッフルして返す"""
    a = np.arange(n)
    b = np.ones(3)
    c = np.zeros(3)
    d = np.ones(3)+1
    e = np.ones(3)+2
    f = np.ones(3)+3
    g = np.ones(3)+4
    h = np.ones(3)+5
    j = np.ones(3)+6
    l = np.ones(15)+7
    k=np.concatenate([a,b,c,d,e,f,g,h,j,])
    np.random.shuffle(k)
    z=[]
    for i in range(len(k)):
        if int(k[i]) not in z:
            z.append(int(k[i]))
    return z
#shuffled5関数の定義(2割は２倍の人気，３割は１，５倍の人気，残りの人気は同程度）ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
def shuffled5(n):
    """0..n-1をシャッフルして返す"""
    a = np.arange(n)
    b = np.ones(3)
    c = np.zeros(3)
    d = np.ones(2)+1
    e = np.ones(2)+2
    f = np.ones(2)+3
    g = np.ones(1)+4
    h = np.ones(1)+5
    j = np.ones(1)+6
    l = np.ones(1)+7
    o = np.ones(1)+8
    k=np.concatenate([a,b,c,d,e,f,g,h,j,l,o])
    np.random.shuffle(k)
    z=[]
    for i in range(len(k)):
        if int(k[i]) not in z:
            z.append(int(k[i]))
    return z

#stable_matching2関数の定義ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
def stable_matching2(prefs, prefl, capa):
    """
    非対称マッチング
    prefs: 研修医が持つ配属先に対する選好
    prefl: 研修医に対する選好(全ての配属先は同じ選好とする)
    capa: 配属先の受入可能数
    """
    acca = list(accumulate([0] + capa[:-1])) # 累積受入可能数
    idx = [i for i, j in enumerate(capa) for _ in range(j)] # ダミー配属先→配属先の変換リスト
    prefs = [[j+acca[i] for i in pr for j in range(capa[i])] for pr in prefs] # ダミーの選考
    res = stable_matching([prefl] * len(prefl), prefs)
    return{k:idx[v] for k, v in res.items()} # ダミーをオリジナルに戻して返す

#変数の定義－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
    lab_capa = [8,8,8,8,8,8,8,8,8,8] # 配属先の受入可能数
    ns, nl = sum(lab_capa), len(lab_capa) # 研修医数と配属先数

    haizokusaki=[] #成績順に並んだ学生番号に配属先をリストで相関づける

"""ここからデータを50回回す！！その中の平均（期待値），max,minをだすーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー"""
for a in range(1,N+1):#試行を繰り返す
   #変数の定義－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
    lab_capa = [8,8,8,8,8,8,8,8,8,8] # 配属先の受入可能数
    ns, nl = sum(lab_capa), len(lab_capa) # 研修医数と配属先数

    haizokusaki=[] #成績順に並んだ学生番号に配属先をリストで相関づける

    #ランダムに成績，選好を作成-----------------------------------------------------------------------------------
    performance = shuffled(ns) # 研修医に対する選好 成績順
    preferences = [shuffled5(nl) for i in range(ns)] # 配属先に対する選好

    #安定マッチングの試行--------------------------------------------------------------------------------------------
    res = stable_matching2(preferences, performance, lab_capa)
    for k, v in res.items():
        haizokusaki.append([k,v])

    #0始まりから１始まりに変更するーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    def calc_add(n):
        return n+1

    b=haizokusaki
    haizokusaki=[]
    for i in range(sum(lab_capa)):
        haizokusaki.append(list(map(calc_add,b[i])))
    c=preferences
    preferences=[]
    for i in range(sum(lab_capa)):
        preferences.append(list(map(calc_add,c[i])))

    performance=list(map(calc_add,performance))

    #DataFrameにデータをまとめる--------------------------------------------------------------------------------------
    dframe=DataFrame(haizokusaki,columns=["学籍番号","配属研究室"])
    dframe2=DataFrame(preferences)
    dframe2.index.name ="学籍番号"
    dframe2.index=dframe2.index+1
    dframe2.columns=list(range(1,len(lab_capa)+1))
    Experimental = data=pd.merge(dframe, dframe2, on="学籍番号")
    dframe3=DataFrame(performance,columns=["成績順位"])
    dframe3.index.name="学籍番号"
    dframe3.index=dframe3.index+1
    Experimental = data=pd.merge(Experimental, dframe3, on="学籍番号")
    Experimental = Experimental.sort_values("学籍番号")
    Experimental['配属された希望番号'] = Experimental.apply(lambda d: (d.loc[list(range(1,len(lab_capa)+1))] == d['配属研究室']).idxmax(), axis=1)
    Experimental.reset_index(drop=True)
    Experimental["配属された希望番号"][np.abs(Experimental["配属された希望番号"])>5] =8 #第6希望以降を第10希望に

    #Excelfailを作る．-------------------------------------------------------------------------------------------
    #Experimental.to_excel(r"C:\Users\hashimoto\Desktop\プログラミング用ファイル\安定マッチング解法\データ\Galeshapleydata"+str(a)+".xlsx")


    #以降，評価関数の設定ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    """ファイルの保存場所は最終結果ーデータに保存"""
    #１，希望実現度評価ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    """学生がどの希望順位で配属されているかを表す学生（成績i位）がどの程度の希望順位の研究室に配属されたかの期待値をしらべる"""
    Desired_realization.append(Experimental["配属された希望番号"].mean())

    #２，成績平準度評価ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    """配属された学生の成績順位を研究室ごとに合計したものの標準偏差をとることで，研究室間のばらつきを調べる"""
    Xi=[]
    for i in range(1,len(lab_capa)+1):
        Xi.append(stdev(Experimental[Experimental["配属研究室"]==i]["成績順位"])+mean(Experimental[Experimental["配属研究室"]==i]["成績順位"]))
    Xmean=mean(Xi)

    S=0
    for i in range(0,len(lab_capa)):
        S=S+(Xi[i]-Xmean)**2
    Standard_deviation.append(S)

    #３，成績別優先度評価ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    """成績の順位別に大体どれくらいの希望で書いた研究室に配属されるかという期待値を表す"""
    df = Experimental.sort_values("成績順位").head(40)
    b=df["配属された希望番号"].tolist()
    h=0
    for i in range(1,41):
        c=4/39*i+35/39
        A=b[i-1]-c
        if A>0:
            h=h+A
    Priority_grade.append(h)

    print(a)

    # 希望外の学生の数
    Unwanted_students.append(len(Experimental["配属された希望番号"][np.abs(Experimental["配属された希望番号"])>5]))
"""ループ終了ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー"""
#4,総合評価ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー

E=mean(Desired_realization)
Emin=min(Desired_realization)
Emax=max(Desired_realization)
S=mean(Standard_deviation)
Smin=min(Standard_deviation)
Smax=max(Standard_deviation)
R=sum(Priority_grade)/len(Priority_grade)
Rmin=min(Priority_grade)
Rmax=max(Priority_grade)

fitness=(1-(E-1)/7)*(1-S/7296)*(1-R/200)*100
D=E*S*R #ただかけただけのやつ
print("希望実現度 mean={},max={},min={}".format(E,Emax,Emin))
print("成績平準度 mean={},min={},max={},".format(S,Smin,Smax))
print("成績別優先度 mean={},min={},max={}".format(R,Rmin,Rmax))
print("総合評価   "+str(fitness))
print("希望外の学生が平均何人出るか {}".format(mean(Unwanted_students)))
