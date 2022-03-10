import re,sys

datCh = lambda num: int(float(num)) if int(float(num))==float(num) else float(num)

def trunc(num, place=5):
    pw=10**place
    return datCh(round(float(num)*pw)/pw)

class solve():
    def __init__(self,eq):
        self.results=[]
        self.trace=[]
        self.pred={'x':0, 'y':0, '':0}
        self.fi=''
        self.pred.setdefault('x',0)
        self.pred.setdefault('y',0)
        self.pred.setdefault('',0)
        if type(eq)==str:
            self.ruas=eq.split('=')
            if len(self.ruas)==1:
                self.ruas.append('')
            self.parse()
        elif type(eq)==list:
            self.ruas=[]
            for i in range(2):
                self.ruas.append(eq[i][:])

    def write(self, stor):
        write=' '
        for i in range(len(stor)):
            x=stor[i]
            if not set(x).isdisjoint('()'):
                for j in x: write+=j+' '
                continue
            if x[1]!=0 or len(stor)==1:
                write+=x[0]+' ' if x[0] else ''
                write+='- ' if x[1]<0 else '' if '(' in stor[i-1] or x[0] else '+ '
                write+=str(trunc(abs(x[1]))) if abs(x[1])!=1 else '' if x[2] else '1'
                write+=(x[2] if x[1]!=0 else '')+' '
            elif x[1]==0 and '(' in stor[i-1] and stor[i+1]==')':
                write+=str(trunc(abs(x[1])))+' '
        if write[:3]==' + ':
            write=write[2:]
        elif write[:2]=='  ':
            write=write[1:]
        return write

    def push(self):
        written=(self.write(self.ruas[0])+('='+self.write(self.ruas[1]) if self.ruas[1] else ''))
        if self.fi!=written:
            print(written)
            self.fi=written
            self.results.append(written)

    def p(self,text=''):
        stor=[]
        expRead=re.findall(r"((?:[/\*]?[+-]?[\(\)])|(?:[/\*]?[+-]?\d*(?:\.\d+)?\w?))",text)
        expRead.pop(-1)
        for i in range(len(expRead)):
            if not set(expRead[i]).isdisjoint('()'):
                stor.append(expRead[i])
                continue
            cutRead=list(re.match(r"([/\*]?)([+-]?\d*(?:\.\d+)?)(\w?)",expRead[i]).groups())
            ownPlus=True if '+' in cutRead[1] else False
            try: cutRead[1]=datCh(cutRead[1])
            except ValueError: cutRead[1]=datCh(cutRead[1]+'1')
            if stor[-1:]==[')'] and cutRead[1]>=0 and not cutRead[0] and not ownPlus:
                cutRead[0]='*'
            stor.append(cutRead)
        return stor

    def parse(self):
        for i in range(2):
            self.ruas[i]=self.p(self.ruas[i])

    def c(self,sample=[],mode=0,points=[]):
        st,ed,blocked=points[0],points[1],False
        i=st+2
        while (i<ed):
            if ('(' in sample[i]):
                blocked=True
                i+=1
            elif (sample[i]==')'):
                blocked=False
                i+=1
            elif blocked: i+=1
            elif (mode and sample[i][2]!=sample[i-1][2]) or (not mode and set(sample[i][0]).isdisjoint('*/')):
                i+=1
            else:
                if sample[i-1]==')':
                    i+=2
                    continue
                back=sample[i-1][1]
                front=sample[i][1] if mode else pow(sample[i][1],-1 if sample[i][0][0]=='/' else 1)
                back=back+front if mode else back*front
                sample[i]=[sample[i-1][0],back,sample[i][2] if mode else sample[i-1][2]+sample[i][2]]
                sample.pop(i-1)
                ed-=1
        points[1]=ed
        return sample

    def calcu(self,target,points=[]):
        for x in range(2):
            target=self.c(target,x,points)
            self.push()

    def g(self, sample=[], points=[]):
        multi, rem, inherit, special, st, ed=1, [False]*2, '', '', points[0], points[1]
        if (not set(sample[st][0]).isdisjoint('*/') or sample[st]=='('):
            if st>0 and sample[st-1]!=')':
                t=set(sample[st-1][0]).intersection('*/')
                if t: special=next(iter(t),'')
                del t
                multi*=sample[st-1][1]*(pow(sample[st+1][1],-2) if '/' in sample[st] else 1)
                inherit+=sample[st-1][2]
                rem[0]=True
            else:
                special='/' if '/' in sample[st] else '*' if st>0 else ''
        if ed<len(sample)-1 and not set(sample[ed+1][0]).isdisjoint('*/'):
            if sample[ed+1][0] or (not sample[ed+1][0] and sample[ed+1][2]):
                multi*=pow(sample[ed+1][1],-1 if '/' in sample[ed+1][0] else 1)
                inherit+=sample[ed+1][2]
                rem[1]=True
        for x in range(st+1,ed):
            sample[x][0]+=special
            sample[x][1]=datCh(sample[x][1]*multi)
            sample[x][2]+=inherit
        if rem[1]:sample.pop(ed+1)
        sample.pop(ed)
        sample.pop(st)
        if rem[0]: sample.pop(st-1)
        return sample

    def getOut(self, target, points):
        target=self.g(target,points)
        self.push()

    def bTrace(self):
        trace=[]
        for i in range(2):
            for x in range(len(self.ruas[i])):
                if '(' in self.ruas[i][x] or ')' == self.ruas[i][x]:
                    trace.append(x)
                    if ')' == self.ruas[i][x]:
                        self.trace.append(trace[:])
                        trace.clear()
            self.trace.append('|')
        self.trace.pop(-1)

    def insToDict(self,eq,m=1):
        for i in eq:
            self.pred[i[2]]=self.pred.get(i[2],0)+i[1]*m

    def predict(self):
        self.insToDict(self.ruas[0])
        self.insToDict(self.ruas[1],-1)
        return [k for k,v in self.pred.items() if v!=0 or k=='']

    def a(self, stor):
        for i in range(len(stor)):
            stor[i][2]=''.join(sorted(stor[i][2]))
        variables=list(set(i[2] for i in stor))
        variables.sort()
        variables.sort(reverse=True,key=len)
        for x in variables:
            stor.sort(key=lambda i: i[2]==x)
        return stor

    def arrange(self):
        for x in range(2):
            self.calcu(self.ruas[x],[-1,len(self.ruas[x])])
        for i in range(2):
            self.ruas[i]=self.a(self.ruas[i])
        self.push()
        for x in range(2):
            self.calcu(self.ruas[x],[-1,len(self.ruas[x])])

def exec(test):
    work=solve(test)
    work.push()
    # print(work.ruas)

    for x in range(2):
        work.ruas[x]=work.c(work.ruas[x],0,[-1,len(work.ruas[x])])
    work.bTrace()
    i=1
    for x in range(len(work.trace)-1,-1,-1):
        if work.trace[x]=='|':
            i=0
        else:
            work.calcu(work.ruas[i],work.trace[x])
            work.getOut(work.ruas[i],work.trace[x])
    del i

    work.arrange()

    if not work.ruas[1]:
        # work.results.append('Please complete the equation e.g. x+5=10')
        return [work.ruas]+work.results, []
    avail_varis=sorted(work.predict())
    if avail_varis==['','x','y'] or avail_varis==['','x'] or avail_varis==['','y']:
        imp=avail_varis[-1]
        def appPop(a,b):
            work.ruas[a].append([i[0],i[1]*-1,i[2]])
            work.ruas[b].pop(work.ruas[b].index(i))
        for i in list(work.ruas[0]):
            if i[2]!=imp: appPop(1,0)
        for i in list(work.ruas[1]):
            if i[2]==imp: appPop(0,1)
        if work.ruas[1]==[]: work.ruas[1].append(['',0,''])
        work.arrange()
        for i in range(len(work.ruas[1])):
            work.ruas[1][i][1]/=work.ruas[0][0][1]
        work.ruas[0][0][1]=1
        work.push()
        tmp={'x':0, 'y':0, '':0}
        for i in work.ruas[1]:
            tmp[i[2]]=i[1]+tmp.get(i[2],0)
        if 'y' in work.ruas[0][0]:
            tmp=[[0,tmp['']+tmp['x']*0],[1,tmp['']+tmp['x']]]
        else:
            tmp=[[tmp[''],0],[tmp[''],1]]
        # print(work.ruas[1])
        return [work.ruas]+work.results, tmp
    else:
        work.results.append('Please only use 2 variables and avoid exponents')
        return [work.ruas]+work.results, []

# exec('y=-0.66666(5)+3.3333')