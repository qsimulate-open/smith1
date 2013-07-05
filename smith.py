import sys
class Sign:
    def __init__(self,sign=1):
        self.sign=sign

    def __eq__(self,other):
        if self.sign==other.sign:
            return 1
        else:
            return 0
        
    def __mul__(self,other):
        return Sign(self.sign * other.sign)

    def __str__(self):
        return self.show()

    def show(self):
        if self.sign>0:
            show="+"
        else:
            show="-"
        return show    
        
class Fraction:
    def __init__(self,numerator=1,denominator=1):
        self.numerator  =numerator
        self.denominator=denominator
        
    def __eq__(self,other):
        if self.numerator  ==other.numerator and \
           self.denominator==other.denominator:
            return 1
        else:
            return 0
        
    def __str__(self):
        return self.show()
    
    def __mul__(self,other):
        num   =self.numerator * other.numerator
        denom =self.denominator * other.denominator
        return Fraction(num,denom)
    
    def __floordiv__(self,other):
        num=self.numerator
        denom=self.denominator
        if num%other.numerator:
            denom=denom * other.numerator
        else:
            num=num / other.numerator
        if denom%other.denominator:
            num=num*other.denominator
        else:
            denom=denom/other.denominator
        return Fraction(num,denom)    
        
    def __add__(self,other):
        denom=self.denominator * other.denominator
        num  =self.denominator * other.numerator \
             +self.numerator   * other.denominator
        return Fraction(num,denom)
        
    def __sub__(self,other):
        denom=self.denominator * other.denominator
        num  =self.numerator   * other.denominator \
             -self.denominator * other.numerator 
        return Fraction(num,denom)
        
    def iszero(self):
        if self.numerator==0:
            return 1
        else:
            return 0
        
    def reduction(self):
        import copy
        denom=copy.deepcopy(self.denominator)
        num  =copy.deepcopy(self.numerator)
        target=min(denom,num)
        aa=PrimeFactor(target)

        itmp=0
        for xx in aa[:-1]:
            if not self.denominator%xx and\
               not self.numerator%xx:
                num  /=xx
                denom/=xx
                itmp=1
                break
        out=Fraction(num,denom)
        if itmp:
            out=out.reduction()
        return out
        
    def show(self):
        show=' '
        show+=str(self.numerator)
        show+=' / '
        show+=str(self.denominator)
        show+=' '
        return show

    def showCpp(self):
        if self.numerator==1 and self.denominator==2:
            return "0.5"
        elif self.numerator==1 and self.denominator==4:
            return "0.25"
        elif self.numerator==1 and self.denominator==8:
            return "0.125"
        else:
            show=""
            if self.denominator==1:
                show+=str(self.numerator)
                show+=".0"
            else:
                show+="("+str(self.numerator)
                show+=".0"
                show+='/'
                show+=str(self.denominator)
                show+=".0)"
            return show
        

    def tex(self):
        if self.numerator==self.denominator:
            return ""
        tex='{\\scriptstyle\\frac{'
        tex+=str(self.numerator)
        tex+='}{'
        tex+=str(self.denominator)
        tex+='}}'
        return tex



class Factor:
    def __init__(self,sign=Sign(),fraction=Fraction()):
        # sign     : Sign class object
        # fraction : Fraction class object 
        self.sign     = sign
        self.fraction = fraction

    def __eq__(self,other):
        if self.sign    ==other.sign and \
           self.fraction==other.fraction:
            return 1
        else:
            return 0

    def __cmp__(self,other):
        valself=float(self.fraction.numerator) \
               /float(self.fraction.denominator)
        valself*=self.sign.sign
        valother=float(other.fraction.numerator) \
                /float(other.fraction.denominator)
        valother*=other.sign.sign
        if valself < valother:
            return -1
        elif valself > valother:
            return 1
        else:
            return 0
    
    def __str__(self):
        return self.show()

    def __mul__(self,other):
        import copy
        if isinstance(other,Sign):
            tmpsign     = self.sign * other
            tmpfraction = copy.deepcopy(self.fraction)
        else:
            tmpsign     = self.sign * other.sign
            tmpfraction = self.fraction * other.fraction
        return Factor(tmpsign, tmpfraction)
        

    def __add__(self,other):
        if self.sign == other.sign:
            tmpfraction=self.fraction+other.fraction
            tmpsign= Sign(self.sign.sign * tmpfraction.numerator)
        else:
            tmpfraction=self.fraction-other.fraction
            if self.sign.show()=="-":
                tmpsign= Sign(self.sign.sign * tmpfraction.numerator)
            else:
                tmpsign= Sign(tmpfraction.numerator)
        outfraction=Fraction(abs(tmpfraction.numerator)    ,
                                 tmpfraction.denominator   )
        return Factor(tmpsign,outfraction)

    def iszero(self):
        if self.fraction.iszero():
            return 1
        else:
            return 0
        
    def show(self):
        show=""
        show+=self.sign.show()
        show+=self.fraction.show()
        return show

    def tex(self):
        show=self.sign.show()
        show+=self.fraction.tex()
        return show

    def __floordiv__(self,other):
        newfraction = self.fraction // other.fraction
        newsign     = self.sign * other.sign
        return Factor(newsign, newfraction)

class Indexrange:
    def __init__(self,type,comp=""):
        # type <- string 
        self.type=type
        self.comp=comp

    def showall(self):
        return self.type
    
    def show(self):
        import string
        mytype=self.type
        if mytype=="general":
            out="g"
        elif mytype=="hole":
            out="h"
        elif mytype=="particle":
            out="p"
        if self.comp:
            out=string.upper(out)
            #out+="("
            #out+=self.comp[:min(4,len(self.comp))]
            #out+=")"
        return out

    def __eq__(self,other):
        if self.type==other.type:
            return 1
        else:
            return 0
        
    def __cmp__(self,other):

        if self.type =="general" and \
           not other.type=="general":
            return 1
        elif not self.type =="general" and \
           other.type=="general":
            return -1
        elif self.type ==other.type :
            return 0
        else:
            print "this comparison may be nonsence", \
                  self.show(),other.show()
    
class ConnectionIndex:
    def __init__(self,mine=[],others=[]):
        # mine   <- [string,]
        # others <- [string,]
        self.mine  =mine
        self.others=others

    def __add__(self,other):
        import copy 
        newmine=copy.deepcopy(self.mine)
        for xx in other.mine:
            if xx in newmine:
                continue
            newmine.append(copy.deepcopy(xx))

        newothers=copy.deepcopy(self.others)
        for xx in other.others:
            if xx in newothers:
                continue
            newothers.append(copy.deepcopy(xx))
        return ConnectionIndex(newmine,newothers)    

    def __str__(self):
        return self.show()

    def show(self):
        import string
        import copy
        show=""
        tmp=copy.deepcopy(self.mine)
        tmp.sort()
        mine=string.join(tmp,"")
        show+=mine

        show+="->"

        tmp=copy.deepcopy(self.others)
        tmp.sort()
        others=string.join(tmp,"")
        show+=others

        return show
        
    def connectwith(self,listtensor):
        # listtensor <- [ String, ]
        # -> boolian
        import copy
        if len(self.others)>len(listtensor):
            return 0
        trial=GenerateCombination(len(listtensor),len(self.others))
        for xx in trial:
            tmp=[]
            for ii in xx:
                tmp.append(copy.deepcopy(listtensor[ii]))
            if Samearray(tmp,self.others):
                return 1
        return 0    
        
    def hasthesametarget(self,other):
        return self.hasthesameconnection(other,itarget=1)
    
    def hasthesameconnection(self,other,itarget=0):
        #itarget <- interger
        # 0: all 1: other only -1: mine only
        # -> boolian
        
        if not itarget:
            if Samearray(self.mine  ,other.mine  ) and\
               Samearray(self.others,other.others):
                return 1
        
            if Samearray(self.others,other.mine  ) and\
               Samearray(self.mine  ,other.others):
                return -1
        #else:
        elif itarget>0:
            if Samearray(self.others,other.others):               
                return 1
        elif itarget<0:
            if Samearray(self.mine  ,other.mine  ):               
                return 1
        return 0
    
    def transpose(self):
        import copy
        newmine  =copy.deepcopy(self.others)
        newothers=copy.deepcopy(self.mine)
        return ConnectionIndex(newmine,newothers)

#    def __init__(self,mine,others=""):
#        # mine   <- string
#        # others <- string
#        self.mine  =mine
#        self.others=others
#
#    def __add__(self,other):
#        import copy 
#        slf =copy.deepcopy(self.mine)
#        othr=copy.deepcopy(other.mine)
#        if slf==othr:
#            mymine=slf
#        else:
#            mymine=slf+othr
#
#        slf =copy.deepcopy(self.others)
#        othr=copy.deepcopy(other.others)
#        if slf==othr:
#            myothers=slf
#        else:
#            myothers=slf+othr
#        return ConnectionIndex(mymine,myothers)
#            
#
#    def __str__(self):
#        return self.show()
#
#    def show(self):
#        if len(self.mine)>len(self.others):
#            show=self.others+self.mine
#        elif len(self.mine)<len(self.others):
#            show=self.mine+self.others
#        else:
#            if self.mine>self.others:
#                show=self.others+self.mine
#            else:
#                show=self.mine+self.others
#         
#        return show        
            

def totalcompleteindextype():
    return ["","complete","ABS","CABS"]

class Topsym:
    def __init__(self,conf=[],ass=[]):
        self.conf=conf
        self.ass =ass

class Listtopsym:
    def __init__(self,topsyms):
        self.topsyms=topsyms

    def topsym_true(self):
        import copy
        list=copy.deepcopy(self.topsyms)
        if not list: return 0
        c=list[0].conf
        a=list[0].ass
        sortc=[copy.deepcopy(c)]
        sorta=[]
        while 1:
            if not a: return 1
            xa=a.pop()
            if not xa in sorta: sorta.append(copy.deepcopy(xa))
            addass=[]
            flag=0
            for yy in list:
                if not xa==yy.conf : continue
                else:
                    flag=1
                    for pp in yy.ass:
                        if not pp in sorta:
                            sorta.append(copy.deepcopy(pp))
                            if not pp in sortc:
                                a.append(copy.deepcopy(pp)) 
                    sortc.append(copy.deepcopy(yy.conf))
                    sorta.sort()
                    sortc.sort()
                    break
            if not flag: return 0

            if sorta==sortc: return 1
        return 0

class Index:
    def __init__(self,type,num,dagger=0,comp=""):
        self.type  =type
        self.num   =num
        self.dagger=dagger
        self.comp  =comp

    def __str__(self):
        return self.show()

    def show(self,showdagger=1,showcomp=0,incode=0):
        import string
        if self.type=="particle":
            show="p"
        elif self.type=="hole":
            show="h"
        elif self.type=="general":
            show="g"
        else:
            print "unknown type",self.type
            sys.exit()
        if self.comp:
            if not incode:
                show=string.upper(show)
            else:
                show="q"
            if showcomp:
                show+="("
                show+=self.comp
                show+=")"
        show+=str(self.num)
        if self.dagger and showdagger:
            show+="+"
        return show    

    def showdagger(self):
        return self.dagger

    def showtype(self):
        return self.type

    def showcomp(self):
        return self.comp
        
    def transpose(self):
        import copy
        out=copy.deepcopy(self)
        if self.dagger:
            out.dagger=0
        else:
            out.dagger=1
        return out    

    def isequalto(self,other,nodagger=0,nonum=0):
        if not self.type==other.type:  
            return 0
        if not nonum and not self.num==other.num:
            return 0
        if not nodagger and not self.dagger==other.dagger:
            return 0
        if not self.comp==other.comp:
            return 0
        return 1

    def __cmp__(self,other):

        if self.dagger > other.dagger:
            return -1
        elif self.dagger < other.dagger:
            return 1

        # canonical order
        if self.type=="hole" and self.type!=other.type:
            return -1
        if self.type=="general" and self.type!=other.type:
            return 1
        if self.type=="particle" and other.type=="hole":
            return 1
        if self.type=="particle" and other.type=="general":
            return -1

        if self.comp > other.comp:
            return 1
        elif self.comp < other.comp:
            return -1

        if self.num > other.num:
            return 1
        elif self.num < other.num:
            return -1
        else:
            print "numbering is wrong",self.num,other.num
            print self,other
        return 0
        
class AnalyzedIndices:
    def __init__(self,indices,symbol,size,target=0,diff=0):
        #indices <- [Index,.]
        #symbol  <- ConnectionIndex
        #size    <- Indexrange
        #insum   <- logical
        #target  <- [AnalyzedIndices]
        self.indices = indices
        self.symbol  = symbol
        self.size    = size
        self.target  = target
        self.diff    = diff

    def __len__(self):
        return len(self.indices)
        
    def __add__(self,other):
        import copy
        newindices=[]
        newindices+=copy.deepcopy(self.indices)
        newindices+=copy.deepcopy(other.indices)
        newindices.sort()

        newsymbol=self.symbol+other.symbol

        newsize=min(self.size,other.size)
        
        return AnalyzedIndices(newindices,newsymbol,newsize)

    def __str__(self):
        return self.show()

    def show(self,
             showcurly=1,
             separator=" "):
        show=""
#shio1 
#       showcurly=1
        if showcurly:
            show+="{ "
        for xx in self.indices:
            show+=xx.show()
            show+=separator
        show=show[:-len(separator)]    
        if showcurly:
            show+=" }_"
            #show+=self.symbol
            #show+=str(self.symbol)
            show+=self.abbreviation()
        return show    

    def showsize(self):
        tmp=self.size.show()
        show=tmp*len(self)
        return show
        
    def abbreviation(self):
        # -> String
        out =str(self.symbol)
        out+="("
        mytype=self.showtype()
        if mytype=="general":
            out+="g"
        elif mytype=="hole":
            out+="h"
        elif mytype=="particle":
            out+="p"
        out+=","
        out+=self.size.show()
        out+=")"
        return out

    def hasthesamenum(self,other):
        for ii in range(len(self.indices)):
           if not self.indices[ii].num==other.indices[ii].num:
               return 0
        return 1

    def hasthesametype(self,other,nodagger=0,noconnection=1,
                       nosize=1,itarget=1,nprint=0):

        if not isinstance(other,Index) and \
           not isinstance(other,AnalyzedIndices):
            return 0

        if not nodagger:
            if not self.showdagger()==other.showdagger():
                return 0
            
        if not self.showtype()==other.showtype():
            return 0

        if not self.showcomp()==other.showcomp():
            return 0

        if not nosize:
            if not self.size==other.size:
                return 0
        if not noconnection:
            if not self.symbol.hasthesameconnection(other.symbol,itarget):
                return 0
        return 1

    def isequalto(self,other,itarget=1,nodagger=0,nosize=1,nonum=1,nocon=0):
        if not isinstance(other,AnalyzedIndices):
            return 0

        if not self.hasthesametype(other,nodagger):
            return 0
        
        if not len(self.indices)==len(other.indices):
            return 0
        
        #if not self.symbol.others==other.symbol.others:
        if not nocon:
            if not self.symbol.hasthesameconnection(other.symbol,itarget):
                return 0

        if not nonum:
            if not self.hasthesamenum(other):
                return 0

        if not nosize:
            if not self.size==other.size:
                return 0
        return 1

    def issameas(self,other,nodagger=0,nosize=1,nonum=1):
        if not isinstance(other,AnalyzedIndices):
            return 0

        if not self.hasthesametype(other,nodagger,nprint=1):
            return 0
        
        if not len(self.indices)==len(other.indices):
            return 0

        if not nonum:
            if not self.hasthesamenum(other):
                return 0

        #if self.symbol.connectwith(["Pp"]):
        #    if not other.symbol.connectwith(["Pp"]):
        #        return 0
        #elif self.symbol.connectwith(["Ph"]):
        #    if not other.symbol.connectwith(["Ph"]):
        #        return 0
        #else:
        #    if other.symbol.connectwith(["Pp"]):
        #       return 0
        #   if other.symbol.connectwith(["Ph"]):
        #       return 0

        if not nosize:
            if not self.size==other.size:
                return 0
        return 1

    def permutable(self,other,lista,listb):
        import copy

        myAI=copy.deepcopy(self.indices)
        yourAI=copy.deepcopy(other.indices)
        list=lista+listb
        targetnum=[]

        for xx in list:
            xxnum=[]
            for yy in xx.indices: 
                xxnum.append(yy.num)
            if myAI[0].num in xxnum:
                targetnum=copy.deepcopy(xxnum)
                break
        #print "&",targetnum,myAI[0].num

        #if not targetnum:
        #    for xx in lista: print "a",xx
        #    for xx in listb: print "b",xx
        #    print "s",self
        #    print "o",other

        if not len(myAI)==0:
            myAI.pop(0)
            for xx in myAI:
                if xx.num in targetnum: continue
                return 0 
        for xx in yourAI:
            if xx.num in targetnum: continue
            return 0
        return 1

    def showdagger(self):
        for ii in range(len(self.indices)):

            if ii==0:
                idagger=self.indices[ii].dagger
                continue
            if not idagger==self.indices[ii].dagger:
                print "Something is wrong "
                print idagger,self.indices[ii].dagger
        return idagger        
        
    def showtype(self):
        for ii in range(len(self.indices)):
            if ii==0:
                itype=self.indices[ii].type
                continue
            if not itype==self.indices[ii].type:
                print "Something is wrong "
                print itype,self.indices[ii].type
        return itype        
        
    def showcomp(self):
        for ii in range(len(self.indices)):
            if ii==0:
                icomp=self.indices[ii].comp
                continue
            if not icomp==self.indices[ii].comp:
                print "Something is wrong "
                print icomp,self.indices[ii].comp
        return icomp        

    def maxval(self):
        import copy
        for ii in range(len(self.indices)):
            if ii==0:
                maxval=copy.deepcopy(self.indices[ii].num)
            else:
                maxval=max(maxval,self.indices[ii].num)
        return maxval        

    def minval(self):
        import copy
        for ii in range(len(self.indices)):
            if ii==0:
                minval=copy.deepcopy(self.indices[ii].num)
            else:
                minval=min(minval,self.indices[ii].num)
        return minval        

    def __cmp__(self,other):
        import copy
        import string
        #other <- AnalyzedIndices
        if not isinstance(other,AnalyzedIndices):
            print "Warning ",other,"is not correct type"
        
        if self.showdagger()>other.showdagger():
            return -1
        elif self.showdagger()<other.showdagger():
            return 1

        # canonical order
        if self.showtype()=="hole" and \
           self.showtype()!=other.showtype():
            return -1
        if self.showtype()=="general" and \
           self.showtype()!=other.showtype():
            return 1
        if self.showtype() =="particle" and \
           other.showtype()=="hole":
            return 1
        if self.showtype() =="particle" and \
           other.showtype()=="general":
            return -1

        #if self.showcomp() > other.showcomp():
        if self.indices[0].comp > other.indices[0].comp:
            return 1
        elif self.indices[0].comp < other.indices[0].comp:
            return -1

        # This is implicitly considered
        # external index.num are always smaller than others
        if self.symbol.connectwith(["Ph"]) or\
           self.symbol.connectwith(["Pp"]):
            if (not other.symbol.connectwith(["Ph"])) and\
               (not other.symbol.connectwith(["Pp"])):
                return -1
        elif (not self.symbol.connectwith(["Ph"])) and\
             (not self.symbol.connectwith(["Pp"])):
            if other.symbol.connectwith(["Ph"]) or\
               other.symbol.connectwith(["Pp"]):
                return 1

        if not self.symbol.others[0]==other.symbol.others[0]:
            if (not len(self.symbol.others[0].split("_"))==1) and (not len(other.symbol.others[0].split("_"))==1):
                if self.symbol.others[0].split("_")[1] and other.symbol.others[0].split("_")[1]:
                    return cmp(self.symbol.others[0].split("_")[1],other.symbol.others[0].split("_")[1])

        if self.target:
            if not other.target:
                return -1
        elif not self.target:
            if other.target:
                return 1

        if self.minval() > other.maxval():
            return 1
        elif self.maxval() < other.minval():
            return -1

        if len(self) > len(other):
            return 1
        elif len(self) < len(other):
            return -1
        
        if self.minval() > other.minval():
            return 1
        elif self.minval() < other.minval():
            return -1

        #print "something is wrong !!!!!!!!!!!!!!!!!!!!!!"
        #print self,other
        return 0

    def transpose(self):
        # -> AnalyzedIndices
        import copy
        out=[]
        for xx in self.indices:
            out.append(xx.transpose())
        return AnalyzedIndices(out,
                               self.symbol.transpose(),
                               copy.deepcopy(self.size))
        
    def a2list(self):
        #->[Index]
        import copy
        return copy.deepcopy(self.indices)

    def a2p(self):
        #->PrimitiveIndices
        import copy
        return PrimitiveIndices(copy.deepcopy(self.indices))

    def evaluatecost(self,restricted=1):
        mytype=self.showtype()
        multiplier=len(self.indices)
        mycomp=self.showcomp()

        if restricted:
            fraction=Fraction(denominator=factorial(multiplier))
        else:
            fraction=Fraction()
        aa=PrimitiveComputationalCost(mytype,
                                      multiplier,
                                      fraction,
                                      mycomp)
        return ComputationalCost([aa])

    def a2c(self):
        import copy
        return CodeIndices(copy.deepcopy(self.indices),
                           copy.deepcopy(self.symbol),
                           copy.deepcopy(self.size)    )
    
    def permute(self,table):
        #table <- PermutationTable
        import copy
        out=[]
        for xx in self.indices:
            aa=table.permute(xx)
            if aa:
                out.append(copy.deepcopy(aa))
            else:
                out.append(copy.deepcopy(xx))

        return AnalyzedIndices(out,
                               copy.deepcopy(self.symbol),
                               copy.deepcopy(self.size))

        ##check
        #list1=[]
        #for xx in out:
        #    isin=0    
        #    for yy in list1:
        #        if xx.isequalto(yy,nonum=0):
        #            isin=1
        #            break
        #    if not isin:    
        #        list1.append(copy.deepcopy(xx))
        #if len(list1)==1:    
        #    return AnalyzedIndices(out,
        #                           copy.deepcopy(self.symbol),
        #                           copy.deepcopy(self.size))
        #else:
        #    list3=[]
        #    for xx1 in list1:
        #        list2=[]
        #        for yy in out:
        #            if yy.isequalto(xx1,nonum=0):
        #                list2.append(copy.deepcopy(yy))
                        
                            
            

    #def setindexparam(self,target,parameter):
    #    
    #    import copy
    #    me=copy.deepcopy(self)
    #    out=[]
    #    if target="comp":
    #        for xx in me.indices:
    #            xx.comp=parameter
    #            out.append(xx)
    #        me.size.comp=parameter     
    #    return AnalyzedIndices(out,
    #                           me.symbol,
    #                           me.size)
                               

class ListAnalyzedIndices:
    def __init__(self,listindices,permutable=[]):
        #listindices <-[AnalyzedIndices,...]
        self.listindices = listindices
        self.permutable  = permutable

    def __add__(self,other):
        import copy
        tmplist=[]
        tmplist+=copy.deepcopy(self.listindices)
        tmplist+=copy.deepcopy(other.listindices)
        out=ListAnalyzedIndices(tmplist)
        return out

    def __len__(self):
        return len(self.listindices)
        

    def __getitem__(self,key):
        # Warning direct access
        return self.listindices[key]

    def __str__(self):
        return self.show()

    def show(self,
             showcurly=1,
             showparenthess=1,
             separator=" , ",
             inseparator=" "):
        # -> String

        show=""
        if showparenthess:
            show+=" ( "
        if self.listindices:   
            for xx in self.listindices:
                show+=xx.show(showcurly=showcurly,
                              separator=inseparator)
                show+=separator
            #show=show[:-3]    
            show=show[:-len(separator)]    
        if showparenthess:
            show+=" ) "
        return show    

    def tex(self,bracket=0):
        import string
        sup= self.listtermswith(dagger=1).listindices
        sub= self.listtermswith(dagger=0).listindices
       
        supscr=""
        subscr=""
        bracket=0
        
        for xx in sup:
            if xx.indices[0].type=="hole": abt="i"
            elif xx.indices[0].type=="particle": abt="a"
            if xx.indices[0].comp: abt="\\alpha"
            if len(xx.indices)==1:
                supscr+=abt+"_{"+str(xx.indices[0].num)+"}"
            else:
                if bracket: supscr+="["
                for ii in range(len(xx.indices)):
                    supscr+=abt+"_{"+str(xx.indices[ii].num)+"}"
                if bracket: supscr+="]"
        for xx in sub:
            if xx.indices[0].type=="hole": abt="i"
            elif xx.indices[0].type=="particle": abt="a"
            if xx.indices[0].comp: abt="\\alpha"
            if len(xx.indices)==1:
                subscr+=abt+"_{"+str(xx.indices[0].num)+"}"
            else:
                if bracket: subscr+="[" 
                for ii in range(len(xx.indices)):
                    subscr+=abt+"_{"+str(xx.indices[ii].num)+"}"
                if bracket: subscr+="]"
        return "^{"+supscr+"}_{"+subscr+"}"

    def showsize(self):
        show=""
        for xx in self.listindices:
            show+=xx.showsize()
        return show    
        
    def isequalto(self,other):
        #-> boolian
        import copy 
        if not isinstance(other,ListAnalyzedIndices):
            return 0
        tmpself =copy.deepcopy(self.listindices)
        tmpother=copy.deepcopy(other.listindices)
        tmpself.sort()
        tmpother.sort()

        if not len(tmpself)==len(tmpother):
            return 0
        for ii in range(len(tmpself)):
            if not tmpself[ii].isequalto(tmpother[ii]):
                return 0
        return 1    

    def extract(self):
        import copy
        tmpself=copy.deepcopy(self.listindices)
        indicesself=[]
        for xx in range(len(tmpself)):
            ii=tmpself[xx] 
            for jj in ii.indices:
                indicesself.append((xx,jj)) #index
        listself=[]
        for ii in range(len(indicesself)):
            (xx,jj)=indicesself[ii]
            listself.append(AnalyzedIndices([jj],tmpself[xx].symbol,tmpself[xx].size))
        listself.sort()
        laiself=ListAnalyzedIndices(listself)
        return laiself

    def getpermutable_1(self):
        import copy
        listAIp=copy.deepcopy(self).extract()
        listAIx=[]
        used=[]
        ix=-1
        for xx in listAIp:
            ix+=1
            if ix in used: continue
            used.append(ix)
            iy=-1
            for yy in listAIp:
                iy+=1
                if iy in used: continue
                xx0=copy.deepcopy(xx.indices[0])
                yy0=copy.deepcopy(yy.indices[0])
                if xx0.dagger==yy0.dagger and xx0.type==yy0.type \
                  and xx0.comp==yy0.comp:
                    used.append(iy)
                    xx.indices.append(yy0) 
            listAIx.append(xx)
        return listAIx

    def getpermutable(self,inx,iny):
    #shiozaki#####################################################
    # obtain the permutablity from self=inx*iny binary contraction
    # inx and iny have been assumed to have "permutable"
    # input of the self is ListAnalyzedIndces (not extracted)
        import copy
        outLAI=[]
        myLAI=copy.deepcopy(self)
        inxLAI=copy.deepcopy(inx)
        inyLAI=copy.deepcopy(iny)

        ix=-1
        used=[]
        for xx in myLAI:
            ix+=1
            if ix in used: continue
            used.append(ix)
            iy=-1
            for yy in myLAI:
                iy+=1
                if iy in used: continue
                if xx.permutable(yy,inxLAI,inyLAI):
                    used.append(iy)
                    for zz in copy.deepcopy(yy.indices):
                        xx.indices.append(zz)
            outLAI.append(xx)
        return outLAI

    def permutable_in_factorize(self,other,xx):
        import copy
        myperm=copy.deepcopy(self.listindices)
        ## FOR DEBUG ########
        #other=other.extract()
        #####################
        yourperm=copy.deepcopy(other.listindices)
        allnum=[]
        mygroup=[]
        for xx in myperm:
            ss=[]
            for yy in xx.indices:
                allnum.append(copy.deepcopy(yy.num))
                ss.append(copy.deepcopy(yy.num))
            mygroup.append(copy.deepcopy(ss))
        yourgroup=[]
        for xx in yourperm:
            ss=[]
            for yy in xx.indices:
                ss.append(copy.deepcopy(yy.num))
            yourgroup.append(copy.deepcopy(ss))

        usednum=[]
        outgroup=[]
        for xx in allnum:
            if xx in usednum: continue
            for yy in mygroup:
                if xx in yy:
                    mine=copy.deepcopy(yy)
                    break
            for yy in yourgroup:
                if xx in yy:
                    yours=copy.deepcopy(yy)
                    break
            out=[]
            for yy in mine:
                if yy in yours: 
                    usednum.append(yy)
                    out.append(yy)
            if not xx in out: 
                print "something is WRONG!!! *3",xx
            outgroup.append(out) 
            
        outperm=[]
        myperm2=copy.deepcopy(myperm)
        if not outgroup==mygroup: 
            for xx in outgroup:
                if xx in mygroup:
                    outperm.append(copy.deepcopy(myperm2[0]))
                    myperm2.pop(0)
                else:
                    tempperm=copy.deepcopy(myperm2[0])
                    for ix in range(len(myperm2[0].indices)-len(xx)):
                        tempperm.indices.pop()
                    for ix in range(len(xx)):
                        myperm2[0].indices.pop(0) 
                    outperm.append(copy.deepcopy(tempperm))
                    if myperm2[0].indices==[]: myperm2.pop(0)
#            print self,other,ListAnalyzedIndices(outperm)
            print xx,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
            return outperm
        else:
            return myperm

    def issameas(self,other,list1,list2,nonum=1):
        #-> boolian
        import copy 
        if not isinstance(other,ListAnalyzedIndices):
            return 0
        tmpself =self.extract().listindices
        tmpother=other.extract().listindices
        tmp=ListAnalyzedIndices(list1)
        list1=tmp.extract().listindices
        tmp=ListAnalyzedIndices(list2)
        list2=tmp.extract().listindices

        for xx in tmpself:
            for yy in list1:
                if xx.isequalto(yy,nocon=1,nonum=0):
                    xx.target=1
                    break
        for xx in tmpother:
            for yy in list2:
                if xx.isequalto(yy,nocon=1,nonum=0): 
                    xx.target=1 
                    break
        if not len(tmpself)==len(tmpother):
            return 0

        for ii in range(len(tmpself)):
            if not tmpself[ii].issameas(tmpother[ii],nonum=nonum):
                return 0
            if not tmpself[ii].target==tmpother[ii].target:
                return 0
        return 1

    def sum_show(self,restricted=0):
        # -> String
        show=" Sum"
        if not restricted:
            show+=self.show(showcurly=0)
        else:
            show+=self.rshow(showcurly=0)
            
        return show
        
    def p_show(self,restricted=0):
        # -> String
        show=" P"
        if not restricted:
            show+=self.show(showcurly=0,
                            separator=" / ")
        else:
            show+=self.rshow(showcurly=0,
                            separator=" / ")
            
        return show
    
    def rshow(self,
             showcurly=1,
             showparenthess=1,
             separator=" , "):
        
        # -> String
        return self.show(showcurly,
                         showparenthess,
                         separator,
                         inseparator=" < ")

    def listConnectionIndex(self,itarget=0):
        # -> [ConnectionIndex]
        import copy
        out=[]
        for xx in self.listindices:
            tmp=copy.deepcopy(xx.symbol)
            isin=0
            for yy in out:
                if yy.hasthesameconnection(tmp,itarget):
                    isin=1
                    break
            if not isin:
                out.append(tmp)
        return out

    
    def showsumindices(self,nodagger=1,nosum=0):
        # -> ListAnalyzedIndices
        import copy
        out=[]
        mylist=copy.deepcopy(self.listindices)
        
        while mylist:
            xx=mylist.pop(0)
            isin=0
            for ii in range(len(mylist)):
                #print "xx",xx,"mylist[ii]",mylist[ii]
                if not xx.isequalto(mylist[ii],
                                    itarget=0,
                                    nodagger=1,
                                    nonum=0,nocon=1):
                    continue
                isin=1
                break
            #if isin:
            #    print "isin",xx,mylist[ii]
            if not nosum:
                if isin:
                    out.append(xx)
                    yy=mylist.pop(ii)
                    out.append(yy)
            else:
                if isin:
                    yy=mylist.pop(ii)
                else:
                    out.append(xx)
        output=ListAnalyzedIndices(out)        
    
        if nodagger:
            output=output.listtermswith(dagger=0)
        output.sort()    
        return output    
                    
    def showsummedindices(self):
        # -> ListAnalyzedIndices (copied)
        import copy
        import string
        
        output=self.showsumindices(nodagger=0,nosum=1)
    
        #reduce index range
        for ii in range(len(output)):
            output[ii].size=Indexrange(output[ii].showtype(),
                                       output[ii].size.comp)
        
        listtarget=output.listConnectionIndex(itarget=1)
        outLAI=ListAnalyzedIndices([])
        for xx in listtarget:
            tmp=output.listtermswith(connectionto=xx)
            #print tmp
    
            if len(tmp)==1:
                outLAI+=tmp
                continue
    
            #Simplify
            tmplist=[]
            for xtmp in tmp.listindices:
                isin=0
                for ii in range(len(tmplist)):
                    if xtmp.hasthesametype(tmplist[ii]):
                        isin=1
                        break
                if not isin:
                    tmplist.append(xtmp)
                    continue
                else:
                    newtmp=tmplist[ii]+xtmp
                    tmplist[ii]=newtmp
                    tmplist[ii].diff=1
            outLAI+=ListAnalyzedIndices(tmplist)
        #print outLAI.show(showcurly=0)
        return outLAI

    def showoutindices(self):
        # -> ListAnalyzedIndices (copied)
        import copy
        import string
        
        #output=self.showsummedindices()
        output=copy.deepcopy(self)
        listtarget=output.listConnectionIndex(itarget=-1)
        outLAI=ListAnalyzedIndices([])
        for xx in listtarget:
            tmp=output.listtermswith(connectionfrom=xx)
            if len(tmp)==1:
                outLAI+=tmp
                continue
    
            #Simplify
            tmplist=[]
            for xtmp in tmp.listindices:
                isin=0
                for ii in range(len(tmplist)):
                    if xtmp.hasthesametype(tmplist[ii]):
                        isin=1
                        break
                if not isin:
                    tmplist.append(xtmp)
                    continue
                else:
                    newtmp=tmplist[ii]+xtmp
                    tmplist[ii]=newtmp
            outLAI+=ListAnalyzedIndices(tmplist)
        #print outLAI.show(showcurly=0)
        outLAI.sort()
        return outLAI
            
    def applyrestriction(self,target=[]):
        # target <- { String, } == abbs of Tensors
        import copy
        mylist=copy.deepcopy(self.listindices)
        outlist=[]
        tmplist=[]
        for xx in mylist:
            #print "connectwith",xx,xx.symbol.connectwith(target)
            if xx.symbol.connectwith(target):
                tmplist.append(xx)
            else:
                outlist.append(xx)

        newlist=[]        
        for xx in tmplist:
            isin=0
            for ii in range(len(newlist)):
                if xx.hasthesametype(newlist[ii]):
                    isin=1
                    break
            if not isin:
                newlist.append(xx)
                continue
            else:
                tmp=newlist[ii]+xx
                newlist[ii]=tmp
        outlist+=newlist
        outlist.sort()
        return ListAnalyzedIndices(outlist)
    
    def updateindices(self,other):
        import copy
        
        targetCI=other.listConnectionIndex(itarget=-1)
        out=copy.deepcopy(self)
        #print "kind",len(targetCI)
        for xx in targetCI:
            #print "targetCI",xx,xx.mine
            #print "--before",out
            out=out.applyrestriction(target=xx.mine)
            #print "--after",out
        return out    

    #def unsummedindices(self,other):
    #    import copy
    #    mylist=copy.deepcopy(self.listindices)
    #    outlist=[]
    #
    #    #  Summed indices
    #    tmplist=[]
    #    for xx in mylist:
    #        isin=0
    #        for yy in other.listindices:
    #            if not xx.isequalto(yy,itarget=0,nodagger=1):
    #                continue
    #            isin=1
    #            break
    #        if isin:
    #            outlist.append(xx)
    #
    #    return ListAnalyzedIndices(outlist)
    def unsummedindices(self,other):
        out1,out2=self.classifysumindices(other)
        return out2
    
    def classifysumindices(self,other):
        import copy
        mylist=copy.deepcopy(self.listindices)
        outlist1=[]
        outlist2=[]
        #  Summed indices
        for xx in mylist:
            isin=0
            for yy in other.listindices:
                if not xx.isequalto(yy,itarget=0,nodagger=1,nonum=0,nocon=1):
                    continue
                isin=1
                break
            if isin:
                outlist1.append(xx)
            else:
                outlist2.append(xx)

        out1=ListAnalyzedIndices(outlist1)
        out2=ListAnalyzedIndices(outlist2)

        return out1,out2

        
    def reduceunsummedindices(self,other):
        import copy
        #mylist=copy.deepcopy(self.listindices)
        #outlist=[]
        #
        ##  Summed indices
        #tmplist=[]
        #for xx in mylist:
        #    isin=0
        #    for yy in other.listindices:
        #        if not xx.isequalto(yy,itarget=0,nodagger=1):
        #            continue
        #        isin=1
        #        break
        #    if isin:
        #        outlist.append(xx)
        #    else:
        #        tmplist.append(xx)
        #mylist=copy.deepcopy(tmplist)         
        out1,out2=self.classifysumindices(other)
        outlist=out1.listindices
        mylist=out2.listindices

        # indices which is connected to deexcitation operator
        # permutation operator
        targetCI=other.listConnectionIndex(itarget=1)
        tmplist=[]
        for xx in mylist:
            isin=0
            for target in targetCI:
                if xx.symbol.hasthesametarget(target):
                    #print "p()",xx
                    outlist.append(xx)
                    isin=1
                    break
            if not isin:
                tmplist.append(xx)
        mylist=copy.deepcopy(tmplist)         
        
        myLAI=ListAnalyzedIndices(mylist)
        #print ListAnalyzedIndices(mylist)
        #print myLAI.showoutindices()
        outlist+=myLAI.showoutindices().listindices 
        #print ListAnalyzedIndices(outlist)
        outlist.sort()
        return ListAnalyzedIndices(outlist)
            
    def listtermswith(self,
                      dagger=-1,
                      types="",
                      connectionto="",
                      connectionfrom="",
                      comp=0):
        # ! Input
        # dagger       <- interger
        # types        <- String
        # connectionto <- ConnectionIndex
        #
        # ! Output
        # -> ListAnalyzedIndices (copyed)
        import copy
        out=[]
        for xx in self.listindices:
            if not xx.showdagger()==dagger and not dagger==-1:
                continue

            #print xx.symbol.others
            #if not connectionto=="" and \
            #   not xx.symbol.others==connectionto:
            #    continue
            if isinstance(connectionto,ConnectionIndex) and \
                   not xx.symbol.hasthesameconnection(connectionto,
                                                      itarget=1):
                continue

            if isinstance(connectionfrom,ConnectionIndex) and \
                   not xx.symbol.hasthesameconnection(connectionfrom,
                                                      itarget=-1):
                continue

            if not types=="" and \
               not xx.showtype()==types:
                continue

            if not comp==0 and \
               not xx.showcomp()==comp:
                continue

            out.append(copy.deepcopy(xx))
        return ListAnalyzedIndices(out)        
            
        
    def sort(self):
        self.listindices.sort()

    def transpose(self):
        out=[]
        for xx in self.listindices:
            out.append(xx.transpose())
        return ListAnalyzedIndices(out)     
       
    def factorrule6(self):
        # -> Fraction
        #sumindices=self.showsumindices()
        #print sumindices
        outfact=Fraction(1,1)
        #for xx in sumindices.listindices:
        for xx in self.listindices:
            nn=factorial(len(xx))
            outfact*=Fraction(1,nn)
        return outfact    
    
    def a2list(self):
        #-> [Index]
        out=[]
        for xx in self.listindices:
            out+=xx.a2list()
        return out    

    def a2p(self):
        #-> PrimitiveIndices
        out=PrimitiveIndices([])
        for xx in self.listindices:
            out+=xx.a2p()
        return out    


    def evaluatecost(self,restricted=1):
        out=ComputationalCost([])
        for xx in self.listindices:
            out*=xx.evaluatecost(restricted)
        return out    

    def a2c(self):
        tmp=[]
        for xx in self.listindices:
            tmp.append(xx.a2c())
        return CodeListIndices(tmp,self.permutable)    

    def permute(self,table):
        # table <- PermutationTable
        tmp=[]
        for xx in self.listindices:
            tmp.append(xx.permute(table))
        return ListAnalyzedIndices(tmp)   

    def removeinternal(self):
        import copy
        tmp=copy.deepcopy(self.listindices)
        numlist=[]
        for xx in tmp:
            for yy in xx.indices:
                numlist.append(yy.num)
        twolist=[]
        for ix in range(len(numlist)):
            for iy in range(ix+1,len(numlist)):
                if numlist[ix]==numlist[iy]: twolist.append(copy.deepcopy(numlist[ix])) 
        er2=[]
        count=0
        for xx in tmp:
            er=[]
            for iy in range(len(xx.indices)):
                if xx.indices[iy].num in twolist:
                    er.append(iy) 
            er.reverse()
            for iy in er:
                xx.indices.pop(iy)
            if len(xx.indices)==0: er2.append(count) 
            count+=1
        er2.reverse()
        for xx in er2:
            tmp.pop(xx)
        tmp.sort()
        out=ListAnalyzedIndices(tmp)
        return out

    def extractifnecesarry(self,targetpermutable): 
        import copy
        #assuming numering is already correct

        out=[]
        for xx in self.listindices:
            flag=0
            numa=[]
            for ii in xx.indices: numa.append(copy.deepcopy(ii.num))

            for yy in targetpermutable: 
                numb=[]
                for ii in yy.indices: numb.append(copy.deepcopy(ii.num))
                if Includearray(numa,numb):
                    flag=1
                    break
            if not flag: 
                for yy in ListAnalyzedIndices([xx]).extract().listindices:
                    out.append(yy)
            else:
                out.append(xx)
        return ListAnalyzedIndices(out)
            

class Permutations:
    def __init__(self,permutations=[]):
        # permutations <- [ListAnalyzedIndices]
        self.permutations=permutations
        
    def __str__(self):
        return self.show()

    def show(self,restricted=0):
        # -> String
        tmp=""
        for xx in self.permutations:
            tmp+=xx.p_show(restricted=restricted)
        return tmp    

    def turn2Primitive(self):
        # -> [PrimitivePermutation]
        import copy
        out=[]
        for xx in self.permutations:
            tmp=[]
            for yy in xx.listindices:
                tmp.append(copy.deepcopy(yy.indices))
            tmp2=PrimitivePermutation(tmp)
            #print tmp2
            out.append(tmp2)
        return out
    
class PrimitivePermutation:
    def __init__(self,indices=[]):
        # indices <- [[Index object,...],...]
        self.indices=indices
        
    def __str__(self):
        return self.show()

    def show(self):
        # -> string object
        if not self.indices:
            return ""
        show="P ( "
        for xx in self.indices:
            for yy in xx:
                show+=str(yy)+" "
            show=show[:-1]    
            show+=" / "
        if len(xx):
            show=show[:-3]
        show+=" ) "
        return show
    def __eq__(self,others):
        import copy
        mine  =copy.deepcopy(self.indices)
        others=copy.deepcopy(others.indices)
    
        if not len(mine)==len(others):
            return 0
    
        # Sort
        for ii in range(len(mine)):
            for jj in range(ii):
                if (len(mine[ii])<len(mine[jj])) or \
                   (len(mine[ii])==len(mine[jj]) and \
                    max(mine[ii])< min(mine[jj])):
                    tmp     =copy.deepcopy(mine[ii])
                    mine[ii]=copy.deepcopy(mine[jj])
                    mine[jj]=copy.deepcopy(tmp)
                    
    
        for ii in range(len(others)):
            for jj in range(ii):
                if (len(others[ii])<len(others[jj])) or \
                   (len(others[ii])==len(others[jj]) and \
                    max(others[ii])< min(others[jj])):
                    tmp     =copy.deepcopy(others[ii])
                    others[ii]=copy.deepcopy(others[jj])
                    others[jj]=copy.deepcopy(tmp)
                    
        for ii in range(len(mine)):
            if not len(mine[ii])==len(others[ii]):
                return 0
            mine[ii].sort()
            others[ii].sort()
            for jj in range(len(mine[ii])):
                if not mine[ii][jj].isequalto(others[ii][jj]):
                    return 0
            return 1                

    #def decompose(self,nprint):
    #    import copy
    #    myindices=copy.deepcopy(self.indices)
    #    length=len(myindices)
    #
    #    comb=[]
    #    for ii in range(length):
    #        for jj in range(ii):
    #            comb.append([jj,ii])
    #
    #    out1=[]
    #    for xx in comb:
    #        tmparray=[]
    #        for yy in xx:
    #            tmparray.append(myindices[yy])
    #        out1.append(tmparray)
    #        
    #    out=[]
    #    for xx in out1:
    #        if len(xx)!=2:
    #            print "Warning!! Something is wrong"
    #        for yy0 in xx[0]:
    #            for yy1 in xx[1]:
    #                out.append(PrimitivePermutation([[yy0],[yy1]]))
    #
    #    if nprint:            
    #        print "Original   :",self            
    #        tmp=  "Decomposed : "
    #        for xx in out:
    #            tmp+=str(xx)
    #        print tmp
    #
    #    return out
    #                
    #def expand(self):
    #    import copy
    #    def perm(aa):
    #        import copy
    #        if not aa:
    #            return [[]]
    #        out=[]
    #        for ii in range(len(aa)):
    #            myaa=copy.deepcopy(aa)
    #            xx=myaa.pop(ii)
    #            for yy in perm(myaa):
    #                out.append([xx]+yy)
    #        return out    
    #    def countpermutation(aa):
    #        import copy
    #        myaa=copy.deepcopy(aa)
    #        sign=1
    #        for ii in range(len(myaa)):
    #            for jj in range(ii):
    #                if myaa[ii]>myaa[jj]:
    #                    continue
    #                tmp   =myaa[ii]
    #                myaa[ii]=myaa[jj]
    #                myaa[jj]=tmp
    #                sign*=-1
    #        return sign        
    #    def expandpermutation(level):
    #    
    #        aa=range(level)
    #        array=perm(aa)
    #    
    #        out=[]
    #        for xx in array:
    #            if aa==xx:
    #                continue
    #            tmparray=[]
    #            for ii in range(len(aa)):
    #                if aa[ii]==xx[ii]:continue
    #                tmparray.append((aa[ii],xx[ii]))
    #            sign=countpermutation(xx)
    #            out.append((sign,dict(tmparray)))
    #        return out    
    #
    #    def getindices(a):
    #        if len(a)==1:
    #            out=[]
    #            for xx in a[0]:
    #                out.append([xx])
    #        else:
    #            tmpout=getindices(a[1:])
    #            out=[]
    #            for xx in tmpout:
    #                for yy in a[0]:
    #                    out.append([yy]+xx)
    #        return out          
    #
    #    pertype=expandpermutation(len(self.indices))
    #    if not self.indices:
    #        return []
    #    out=[]
    #    for index in getindices(self.indices):
    #        for xx in pertype:
    #            tmptuple=[]
    #            for key in xx[1].keys():
    #                tmptuple.append( (index[int(key)].show(0),
    #                                  index[xx[1][key]])  )
    #            out.append([xx[0],dict(tmptuple)])
    #    return out        

        
class Indexpairs:
    def __init__(self,pairs=[]):
        # pairs <- [ ( Index , Index ),... ]
        self.pairs=pairs

    def __str__(self):
        # -> String
        show=""
        for xx in self.pairs:
            show+="("
            for yy in xx:
                show+=str(yy)
            show+=")"
        return show

    def pshow(self):
        # -> String
        show=""
        for xx in self.pairs:
            for yy in xx:
                show+=str(yy)
                show+=" -> "
            if xx:
                show=show[:-4]
            show+=" , "
        if self.pairs:
            show=show[:-3]
        return show
    
    def __add__(self,other):
        # -> Indexpairs (copied)
        import copy
        out=[]
        out+=copy.deepcopy(self.pairs)
        out+=copy.deepcopy(other.pairs)
        return Indexpairs(out)

    def findoneloop(self,target):
        # -> number, Indexpairs(copied)
        import copy
        if not self.pairs:
            return 0,Indexpairs()
        mytarget=copy.deepcopy(target)
        mypairs =copy.deepcopy(self.pairs)
        while mypairs:
            found=0
            for ii in range(len(mypairs)):
                if mypairs[ii][1].isequalto(mytarget[0],
                                            nodagger=1):
                    found=1
                    break
            if found:
                mytarget=mypairs.pop(ii)
            else:
                return 0,Indexpairs(mypairs)

            if mytarget[0].isequalto(target[1],
                                     nodagger=1):
                return 1,Indexpairs(mypairs)
            elif not mytarget[0]:
                return 0,Indexpairs(mypairs)
            
            if not mypairs:
                return 0,Indexpairs(mypairs)

        print "Worning!! Something is wrong"
            
    def findloops(self,nprint=0):

        import copy
        myIp=copy.deepcopy(self)
        tot=0
        while myIp.pairs:
            init=myIp.pairs.pop()
            count,myIp=myIp.findoneloop(init)
            tot+=count
            if nprint:
                print "Num of loops:",count
                print "Residual    :",myIp
        if nprint:        
            print     "Total       :",tot
        return tot    

    def showpairof(self,target,key=0):
        #target <- Index
        #key    <- 0,1
        import copy
        for xx in self.pairs:
            if xx[key].isequalto(target,nodagger=1):
                tmp=copy.deepcopy(xx[1-key])
                tmp.dagger=target.dagger
                return tmp
        return 0    
    
class AnalyzedTensor:
    def __init__(self,symbol,indices,abb="",symmetry=[],fraction=Fraction()):
        # symbol  <- String
        # indices <- ListAnalyzedIndices
        # abb     <- String
        # symmetry<- [String,]
        self.symbol  = symbol
        self.indices = indices
        self.abb     = abb
        self.symmetry= symmetry
        self.fraction= fraction

    def __str__(self):
        return self.show()

    def show(self,restricted=0,showsym=1,showsize=1):    
        import string
        show=""
        show+=self.symbol
        if restricted:
            show+=self.indices.rshow(showcurly=0)
        else:
            show+=self.indices.show(showcurly=0)
        if showsym:
            show=show[:-1]
            show+="_"
            for xx in self.symmetry:
            	show+=xx
            show+=" "
        if showsize:
            show=show[:-1]
            if not showsym:
                show+="_"
            show+="("
            show+=self.indices.showsize()
            show+=")"
            show+=" "
        return show

    def tex(self):
        import string
        show=""
        if len(self.symbol)>1 and self.symbol[1]=="d":
            show+="("
            show+=self.symbol[:1]
            show+="^{\\dagger})"
            #show+=self.indices.tex()
        elif len(self.symbol)>1 and self.symbol[0]=="K":
            #show+=self.fraction.tex()
            show+="(\\Xi_{"
            show+=self.symbol.split("_")[0][1:]
            show+="})"
        else:
            show+=self.symbol.split("_")[0]

        show+=self.indices.tex(bracket=1)
        return show

    def __cmp__(self,other):
        if self.symbol[0]=="t":
            return 1
        if other.symbol[0]=="t":
            return -1
        if self.symbol[0]=="l":
            return 1
        if other.symbol[0]=="l":
            return -1
        if self.symbol[0]=="s":
            return 1
        if other.symbol[0]=="s":
            return -1
        if self.symbol[0]=="K":
            return -1
        if other.symbol[0]=="K":
            return 1
        if self.symbol[0]=="v":
            return -1
        if other.symbol[0]=="v":
            return 1
        if self.symbol[0]=="f":
            return -1
        if other.symbol[0]=="f":
            return 1
        if self.symbol[0]=="z":
            return -1
        if other.symbol[0]=="z":
            return 1
        return 0

    def isequalto(self,other,comp=0,topsym=[]):
        import copy
        import string
        if not isinstance(other,AnalyzedTensor):
            return 0
        if not self.symbol.split("_")[0]==other.symbol.split("_")[0]:
            return 0
        if self.indices.isequalto(other.indices):
            return 1
        if not comp: return 0

        mylai=copy.deepcopy(self.indices.listindices)
        mylai.sort()        
        yourlai=copy.deepcopy(other.indices.listindices)
        yourlai.sort()        
        if not len(mylai)==len(yourlai): return 0  

        assumption=[]
        confirmed=[]
        for ix in range(len(mylai)):
            if mylai[ix].isequalto(yourlai[ix]): continue
            if not mylai[ix].hasthesametype(yourlai[ix],nodagger=1):
                return 0
            if not len(mylai[ix].indices)==len(yourlai[ix].indices):
                return 0

            mytarget=mylai[ix].symbol.others[0]
            yourtarget=yourlai[ix].symbol.others[0]
            if mytarget[0]=="P": return 0
            if not mytarget.split("_")[0]==yourtarget.split("_")[0]: 
                return 0
            if not mytarget.split("_")[1]==yourtarget.split("_")[1]: 
                return 0
            else:
                newass=[int(mytarget.split("_")[1]),int(yourtarget.split("_")[1])]
                newass.sort()
                assumption.append(newass)

        newconf=[int(self.symbol.split("_")[1]),int(other.symbol.split("_")[1])]
        newconf.sort()
        
        topsym.append(Topsym(newconf,assumption))
        ltopsym=Listtopsym(topsym)
        if ltopsym.topsym_true(): return 1
        return 0

    def issameas(self,other,list1,list2,nonum=1):
        import string
        if not isinstance(other,AnalyzedTensor):
            return 0
        if not self.symbol.split("_")[0]==other.symbol.split("_")[0]:
            return 0
        if len(self.symbol)>2 and len(other.symbol)==2:
            return 0
        if len(self.symbol)==2 and len(other.symbol)>2:
            return 0
        if not self.indices.issameas(other.indices,list1,list2,nonum=nonum):
            return 0
        return 1

    def generateIndexpairs(self,nprint=0):
        # -> Indexpairs
        dindcs=self.indices.listtermswith(dagger=1)
        nindcs=self.indices.listtermswith(dagger=0)
        listdindcs=dindcs.a2list()
        listnindcs=nindcs.a2list()
        npair=min(len(listdindcs),len(listnindcs))
        pairs=[]
        for ii in range(npair):
            tmp=(listdindcs[ii],listnindcs[ii])
            pairs.append(tmp)
        out=Indexpairs(pairs)
        if nprint:
            print "Tensor     : ",self
            print "Indexpairs : ",out
        return out

    def reduceunsummedindices(self,others):
        import copy
        if isinstance(others,AnalyzedTensor):
            oindices=copy.deepcopy(others.indices)
        elif isinstance(others,AnalyzedTensorSequence):
            oindices=others.listindices()
        else:
            print "Error in reduceunsummedindices"

        newindices = self.indices.reduceunsummedindices(oindices)
        newsymbol  =copy.deepcopy(self.symbol)
        newabb     =copy.deepcopy(self.abb)
        newsymmetry=copy.deepcopy(self.symmetry)
        return AnalyzedTensor(newsymbol,
                              newindices,
                              newabb,
                              newsymmetry)

    def updateindices(self,other):
        import copy
        newindices =self.indices.updateindices(other.indices)
        newsymbol  =copy.deepcopy(self.symbol)
        newabb     =copy.deepcopy(self.abb)
        newsymmetry=copy.deepcopy(self.symmetry)
        return AnalyzedTensor(newsymbol,
                              newindices,
                              newabb,
                              newsymmetry)

    def a2c(self):
        # -> 
        import copy
        newindices=self.indices.a2c()
        return CodeTensor(copy.deepcopy(self.symbol),
                          newindices,
                          copy.deepcopy(self.abb),
                          copy.deepcopy(self.symmetry),
                          copy.deepcopy(self.fraction))
                          
    def a2p(self):
        #-> PrimitiveTensor
        import copy
        return PrimitiveTensor(copy.deepcopy(self.symbol),
                               self.indices.a2p())

    def a2p_abb(self):
        #-> PrimitiveTensor
        import copy
        out=PrimitiveTensor(copy.deepcopy(self.abb),
                               self.indices.a2p(),"x")
        out.abb=out.abb[:-1]
        return out

    #def applyrestriction(self,target=[]):
    #    # target <- { String, } == abbs of Tensors
    #    import copy
    #    newindices=self.indices.applyrestriction(target)
    #    newsymbol=copy.deepcopy(self.symbol)
    #    newabb   =copy.deepcopy(self.abb)
    #    return AnalyzedTensor(newsymbol,
    #                          newindices,
    #                          newabb)
        
class AnalyzedTensorSequence:
    def __init__(self,tensors):
        # tensors <- [AnalyzedTensor]
        self.tensors = tensors

    def __str__(self):
        return self.show()

    def show(self,restricted=0):
        show=""
        for xx in self.tensors:
            show+=xx.show(restricted=restricted)
        return show    

    def tex(self):
        tex=""
        for xx in self.tensors:
            tex+=xx.tex()
        return tex

    def __add__(self,other):
        import copy
        out=[]
        out+=copy.deepcopy(self.tensors)
        out+=copy.deepcopy(other.tensors)
        return AnalyzedTensorSequence(out)

    def __getitem__(self,key):
        return self.tensors[key]

    def __len__(self):
        return len(self.tensors)
        
    def listindices(self):
        import copy
        out=ListAnalyzedIndices([])
        for xx in self.tensors:
            out+=xx.indices
        return out    

    def listabbs(self):
        # -> [String]
        import copy
        out=[]
        for xx in self.tensors:
            tmp=copy.deepcopy(xx.abb)
            if tmp in out:
                continue
            out.append(tmp)
        return out

    def contractionabb(self):
        import string
        # -> String
        out=""
        for xx in self.tensors:
            out+=xx.abb.split("_")[0]
        return out
    
    def factorrule7(self,nprint=0,comp=0):
        # -> Fraction
        import copy
        dicttensors={}
        topsym=[]
        for ii in range(len(self.tensors)):
            isin=0
            keys=dicttensors.keys()
            for xx in keys:
                jj=dicttensors[xx][0]
                
                if self.tensors[jj].isequalto(self.tensors[ii],comp=comp,topsym=topsym):
                    dicttensors[xx].append(ii)
                    isin=1
                    break
            if not isin:
                xx=copy.deepcopy(self.tensors[ii].abb)
                dicttensors[xx]=[ii]

        out=Fraction()
        for xx in dicttensors.keys():
            nn=factorial(len(dicttensors[xx]))
            out*=Fraction(1,nn)

        if nprint:
            tmp="\no Tensor Analysys"
            for xx in dicttensors.keys():
                tmp+="\n - key \""+xx+"\""
                tmp+="\n    Tensors : "
                for ii in dicttensors[xx]:
                    tmp+=str(self.tensors[ii])+" , "
                tmp=tmp[:-3]     
                tmp+="\n    factor  : "    
                nn=factorial(len(dicttensors[xx]))
                tmp+=str(Fraction(1,nn))
            tmp+="\n\no Factor from Rule7 : "
            tmp+=str(out)
            print tmp
        return out    
        
    def estimatepermutation(self):
        # -> Permutations
        # estimate permutation operater based on rule 9
        import copy
        tmpindices=self.listindices()
        tmpindices=tmpindices.showsumindices(nodagger=0,nosum=1)
        target=tmpindices.listConnectionIndex(itarget=1)
        
        Perms=[]
        for xx in target:
            pindices=tmpindices.listtermswith(connectionto=xx).listindices
            if len(pindices)==1:
                continue
            usedindices=[]
            for yy in pindices:
                if yy in usedindices:
                    continue
                usedindices.append(yy)
                tmplist=[yy]
                for zz in pindices:
                    if zz in usedindices:
                        continue
                    if yy.hasthesametype(zz):
                        tmplist.append(zz)
                        usedindices.append(zz)
                if len(tmplist)==1:
                    continue
                tmplist.sort()
                outperm=ListAnalyzedIndices(tmplist)
                Perms.append(copy.deepcopy(outperm))
                
            #pindices.sort()
            #Perms.append(copy.deepcopy(pindices))
            #print pindices.p_show()
                    
        return Permutations(Perms)

    #def estimatepermutation(self):
    #    # -> Permutations
    #    # estimate permutation operater based on rule 9
    #    import copy
    #    tmpindices=self.listindices()
    #    i_target=tmpindices.listtargettensor()
    #    myabbs=self.listabbs()
    #
    #    outtensors=[]
    #    for xx in i_target:
    #        if xx in myabbs:
    #            continue
    #        outtensors.append(xx)
    #    #print outtensors    
    #    
    #    Perms=[]
    #    for xx in outtensors:
    #        pindices=tmpindices.listtermswith(connectionto=xx)
    #        if len(pindices)==1:
    #            continue
    #        pindices.sort()
    #        Perms.append(copy.deepcopy(pindices))
    #        #print pindices.p_show()
    #    return Permutations(Perms)

    def generateIndexpairs(self,nprint=0):
        # -> Indepxairs
        out=Indexpairs()
        for xx in self.tensors:
            out+=xx.generateIndexpairs(nprint)
        return out    

    def numberofloops(self,nprint=0):
        # -> number
        pair=self.generateIndexpairs(nprint)
        nloops=pair.findloops(nprint)
        return nloops

    def numberofholes(self,nprint=0):
        # -> number
        listindices=self.listindices()
        #hole=listindices.listtermswith(types="hole")
        hole=listindices.listtermswith(types="hole",dagger=0)
        nholes=len(hole.a2list())
        if nprint:
            print hole
            print "Total number of holes : ",nholes
        return nholes

    def showsummedindices(self):
        # -> ListAnalyzedindices
        tmp=self.listindices().showsummedindices()
        tmp.sort()
        return tmp

    def showsumindices(self,nodagger=1,nosum=0):
        # -> ListAnalyzedindices
        tmp=self.listindices().showsumindices(nodagger=nodagger,
                                              nosum=nosum)
        return tmp
        
    def estimatesign(self,
                    withprojection=0,
                    nprint=0):
        # -> Sign
        # estimate sign based on rule 8
        import copy

        myTS=copy.deepcopy(self)
        if withprojection:
            #tmp=self.listindices().showsummedindices()
            tmp=self.showsummedindices()
            projectionindices=tmp.transpose()
            projectionindices.sort()
            projection=AnalyzedTensor("z",projectionindices)
            if nprint:
                print "Projection operator   : ",projection
            myTS=AnalyzedTensorSequence([projection])+myTS
        
        #nloop=self.numberofloops(0)
        nloop=myTS.numberofloops(0)
        nhole=myTS.numberofholes(0)
        outsign=Sign((-1)**(nloop+nhole))
        if nprint:
            print "Total number of loops : ",nloop
            print "Total number of holes : ",nhole
            print "===> Sign from Rule 8 = ",outsign
        return outsign    

    def estimatefraction(self,nprint=0,comp=0,norule7=0):
        rule6=self.showsumindices().factorrule6()
        newfactor=rule6
        if not norule7:
            rule7=self.factorrule7(comp=comp)
            newfactor*=rule7
        if nprint:
            print "From Rule 6 : ",rule6
            if not norule7:
                print "From Rule 7 : ",rule7
            print "===> Total  = ",newfactor
        return newfactor    

    def estimaterestrictedfraction(self,nprint=0):
        rule7=self.factorrule7()
        newfactor=rule7
        if nprint:
            print "From Rule 6 : Waived"
            print "From Rule 7 : ",rule7
            print "===> Total  = ",newfactor
        return newfactor    

    def estimatememorycost(self,restricted=1,nprint=0):
        # -> CompuatationalCost
        tmp=self.showsummedindices()
        cost=tmp.evaluatecost(restricted)
        if nprint:
            print "o Memory Cost"
            print cost.show(nprint)
        return cost

    def estimateoperationcost(self,restricted=1,nprint=0):
        # -> CompuatationalCost
        tmpall=self.showsumindices(nodagger=0,nosum=1)
        allcost=tmpall.evaluatecost(restricted)
    
        tmpsum=self.showsumindices()
        sumcost=tmpsum.evaluatecost(restricted)
    
        out=allcost*sumcost
        if nprint:
            print "o Operation Cost"
            print out.show(nprint)
        return out    

    def reduceunsummedindices(self):
        import copy
        mytensors=copy.deepcopy(self.tensors)
        if len(mytensors)==1:
            tmp=mytensors[0].showoutindices()
            return AnalyzedTensorSequence([tmp])

        outlist=[]
        for ii in range(len(mytensors)):
            tmp=copy.deepcopy(mytensors)
            target=tmp.pop(ii)
            others=AnalyzedTensorSequence(tmp)
            outlist.append(target.reduceunsummedindices(others))
            
        return AnalyzedTensorSequence(outlist)
        
        
    def updateindices(self):
        import copy
        mytensors=copy.deepcopy(self.tensors)
        if len(mytensors)==1:
            return copy.deepcopy(self)
        
        comb=GenerateCombination(len(mytensors),2)
        for aa in comb:
            #print aa
            t1=mytensors[aa[0]]
            t2=mytensors[aa[1]]

            newt1=t1.updateindices(t2)
            newt2=t2.updateindices(t1)

            mytensors[aa[0]]=newt1
            mytensors[aa[1]]=newt2
        return AnalyzedTensorSequence(mytensors)

    def totalsymmetry(self):
        out=[]
        for xx in self.tensors:
            out+=xx.symmetry
        return out

    def a2c(self):
        out=[]
        for xx in self.tensors:
            out.append(xx.a2c())
        return CodeTensorSequence(out)    

    def a2p(self):
        out=[]
        for xx in self.tensors:
            out.append(xx.a2p())
        return PrimitiveTensorSequence(out)    
   
    def a2p_abb(self):
        out=[]
        for xx in self.tensors:
            out.append(xx.a2p_abb())
        return PrimitiveTensorSequence(out)    

    def swhich(self):
        import copy
        out=copy.deepcopy(self)
        for xx in out.tensors:
            xx.abb=copy.deepcopy(xx.symbol)
        return out 
   
class PrimitiveIndices:
    def __init__(self,indices):
        # indices <- [Index,]
        self.indices=indices

    def show(self,showdagger=1):
        show=""
        for xx in self.indices:
            show+=xx.show(showdagger)
        return show

    def __add__(self,other):
        import copy
        out=[]
        out+=copy.deepcopy(self.indices)
        out+=copy.deepcopy(other.indices)
        return PrimitiveIndices(out)
        
    def __len__(self):
        return len(self.indices)

    def __getitem__(self,key):
        return self.indices[key]

    def sort(self):
        self.indices.sort()

    def isequalto(self,other,nonum=1):

        if not isinstance(other,PrimitiveIndices):
            return 0

        if not len(self)==len(other):
            return 0

        for dagger in [1,0]:
            for types in ["general","particle","hole"]:
                for comp in totalcompleteindextype():
                    aa=self.listtermswith(dagger=dagger,
                                          types=types,
                                          comp=comp)
                    bb=other.listtermswith(dagger=dagger,
                                           types=types,
                                           comp=comp)

                    if not len(aa)==len(bb):
                        return 0

                    if not nonum:
                        aa.sort()
                        bb.sort()
                        for ii in range(len(aa)):
                            if not aa[ii].isequalto(bb[ii]):
                                return 0
        return 1                    

                  
    def listtermswith(self,dagger=-1,types="",comp=0):
        import copy
        out=[]
        for xx in self.indices:
            if not dagger==-1 and not xx.dagger==dagger:
                continue
            if not types=="" and not xx.type==types:
                continue
            if not comp==0 and not xx.comp==comp:
                continue
            out.append(copy.deepcopy(xx))
        return PrimitiveIndices(out)
        
    def signbycanonicalization(self):
        # -> Sign
        import copy
        aa=copy.deepcopy(self.indices)
        ipermute=0
        for ii in range(len(aa)):
            for jj in range(ii):
                if aa[ii]<aa[jj]:
                    tmp   =copy.deepcopy(aa[jj])
                    aa[jj]=copy.deepcopy(aa[ii])
                    aa[ii]=copy.deepcopy(tmp)
                    ipermute+=1
        outsign=Sign((-1)**(ipermute))
        return outsign

    def genexchangetable(self,targetorder):
        #targetorder < PrimitiveIndices
        #-> Indexpairs
        import copy
        if not isinstance(targetorder,PrimitiveIndices):
            print targetorder,"is not ",PrimitiveIndices," class object"
        if not len(self)==len(targetorder):
            print "length of ",self," and ",targetorder,"is different."

        out=[]
        for ii in range(len(self)):
            if self[ii].isequalto(targetorder[ii]):
                continue
            out.append( (copy.deepcopy(self[ii]),
                         copy.deepcopy(targetorder[ii])) )
        myip=Indexpairs(out)
        return myip
        
    def generatepermutation(self,targetorder):
        myip=self.genexchangetable(targetorder)
        
        ssign=self.signbycanonicalization()
        tsign=targetorder.signbycanonicalization()
        mysign=ssign*tsign

        #print myip.pshow(),mysign.show()
        
        return PermutationTable(myip,mysign)

    def gensortorderlist(self,target):
        #target < PrimitiveIndices
        #-> [str,]
        import copy
        my=copy.deepcopy(self.indices)
        ii=1
        tlist=[]
        for xx in my:
            tlist.append( (xx,ii) )
            ii+=1

        out=[]    
        for yy in target:
            isin=0
            for zz in tlist:
                if yy.isequalto(zz[0]):
                    out.append(str(zz[1]))
                    isin=1
                    break
            if not isin:
                print "Something is wrong"
        return out        

    def exchangeindices(self,indexpair):
        # indexpair < IndexPair
        import copy
        out=[]
        for xx in self.indices:
            aa=indexpair.showpairof(xx)
            if aa:
                out.append(copy.deepcopy(aa))
            else:
                out.append(copy.deepcopy(xx))
        return PrimitiveIndices(out)        
        
class PrimitiveTensor:
    def __init__(self,symbol,indices,abb=""):
        # symbol  <- String
        # indices <- [Index]
        self.symbol  = symbol
        self.indices = indices
        if abb:
            self.abb = abb
        else:
            tabb=""
            tabb+=self.symbol
            tabb+=str(len(self.indices)/2)
            self.abb = tabb

    def __str__(self):
        return self.show()

    def show(self):
        show=""
        show+=self.symbol
        show+=" ( "
        for xx in self.indices:
            show+=xx.show()
            show+=" "
        show=show[:-1]
        show+=" ) "
        return show
    
    def abbreviation(self):
        out=""
        out+=self.symbol
        out+=str(len(self.indices)/2)
        return out

    def contains(self,target):
        #target <- Index
        # -> boolian
        isin=0
        for xx in self.indices:
            if target.isequalto(xx,nodagger=1):
                isin=1
                break
        return isin    

    def isequalto(self,other,nonum=1):
        if not isinstance(other,PrimitiveTensor):
            return 0
        aa=PrimitiveIndices(self.indices)
        bb=PrimitiveIndices(other.indices)
        if not aa.isequalto(bb,nonum):
            return 0
        return 1
        
    def listindiceswith(self,
                        dagger=-1,
                        types="",
                        comp=0):
        import copy
        out=[]
        for xx in self.indices:
            if not dagger==-1 and not xx.dagger==dagger:
                continue
            if not types=="" and not xx.type==types:
                continue
            if not comp==0 and not xx.comp==comp:
                continue
            out.append(copy.deepcopy(xx))
        return out    
                        
class PrimitiveTensorSequence:
    def __init__(self,tensors):
        # tensors <- [PrimtiveTensor]
        self.tensors = tensors

    def __str__(self):
        return self.show()

    def __getitem__(self,key):
        return self.tensors[key]
    
    def __len__(self):
        return len(self.tensors)
    
    def show(self):
        show=""
        for xx in self.tensors:
            show+=xx.show()
        return show    

    def isequalto(self,other,nonum=1):
        if isinstance(other,PrimitiveTensorSequence):
            return 0
        if not len(self)==len(other):
            return 0
        for ii in range(len(self)):
            if not self[ii].isequalto(other[ii]):
                return 0
        return 1    
        
    def relabel(self,nprint=0):
        # -> PrimitiveTensorSequence (new)
        import copy
        my_PTensors=copy.deepcopy(self.tensors)
        dictabb={}
        for ii in range(len(my_PTensors)):
            listkeys=dictabb.keys()
            abb=my_PTensors[ii].abb
            if abb in listkeys:
                dictabb[abb].append(ii)
            else:
                dictabb[abb]=[ii]
        listkeys=dictabb.keys()
        for xx in listkeys:
            if len(dictabb[xx])==1:
                continue
            for ii in range(len(dictabb[xx])):
                kk=dictabb[xx][ii]
                abb=my_PTensors[kk].abb
                abb+="_"
                abb+=str(ii)
                my_PTensors[kk].abb=abb
        if nprint:        
            print "\no New labels"
            for xx in my_PTensors:
                print xx.abb,"for Tensor",xx
        return PrimitiveTensorSequence(my_PTensors)        

    def relabelnum(self,pmytarget,sup=0):
        import copy
        mxx=copy.deepcopy(self)
        usediddict={}

        htn=1
        ptn=1
        htd=1
        ptd=1
        id2=1
        for ii in pmytarget:
            if ii.type=="hole" and ii.dagger==0:
                htd+=1 
                ptn+=1 
                ptd+=1 
                id2+=1
            elif ii.type=="particle" and ii.dagger==0:
                htd+=1
                ptd+=1
                id2+=1
            elif ii.type=="hole" and ii.dagger==1:
                ptd+=1
                id2+=1
            elif ii.type=="particle" and ii.dagger==1:
                id2+=1
        id2sv=copy.deepcopy(id2)

        output=copy.deepcopy(mxx)
        #print output
        for ii in range(len(mxx.tensors)):
            count=-1
            for jj in mxx.tensors[ii].indices.indices:
                count+=1
                nn=output.tensors[ii].indices.indices[count]
                flag=0
                for kk in pmytarget:
                    if jj.isequalto(kk):
                        flag=1
                keys=usediddict.keys()
                kk=copy.deepcopy(nn.num)
                if not str(kk) in keys:  
                    if flag and jj.type=="hole" and jj.dagger==0:
                        nn.num=copy.deepcopy(htn)
                        usediddict[str(kk)]=copy.deepcopy(htn)
                        htn+=1
                    elif flag and jj.type=="particle" and jj.dagger==0:
                        nn.num=copy.deepcopy(ptn)
                        usediddict[str(kk)]=copy.deepcopy(ptn)
                        ptn+=1
                    elif flag and jj.type=="hole" and jj.dagger==1:
                        nn.num=copy.deepcopy(htd)
                        usediddict[str(kk)]=copy.deepcopy(htd)
                        htd+=1
                    elif flag and jj.type=="particle" and jj.dagger==1:
                        nn.num=copy.deepcopy(ptd)
                        usediddict[str(kk)]=copy.deepcopy(ptd)
                        ptd+=1
                    elif not flag:
                        nn.num=copy.deepcopy(id2)
                        usediddict[str(kk)]=copy.deepcopy(id2)
                        id2+=1
                    else:
                        print "?"
                        continue
                else: 
                    nn.num=usediddict[str(kk)]
        if sup:
            output=output.relabel_sup(id2sv)
        return output

    def relabel_sup(self,id):
        import copy
        mxx=copy.deepcopy(self)
        pairs=[]
        for ii in range(len(mxx.tensors)):
            iitensor=mxx.tensors[ii]
            iiindices=iitensor.indices.indices
            alld=[]
            alls=[]
            for mm in range(ii+1,len(mxx.tensors)):
                mmtensor=mxx.tensors[mm]
                mmindices=mmtensor.indices.indices 
                for nn in mmindices:
                    if nn.dagger: alls.append(copy.deepcopy(nn.num))
                    else:         alld.append(copy.deepcopy(nn.num))
            flagd=0
            flags=0
            used=[]
            for jj in range(len(iiindices)):
                if jj in used: continue
                used.append(jj)
                indjj=iiindices[jj]
                pair=[]
                for kk in range(jj+1,len(iiindices)): 
                    if kk in used: continue
                    indkk=iiindices[kk]
                    if indjj.num>=id and indkk.num>=id and indjj.dagger==indkk.dagger\
                        and indjj.comp==indkk.comp and indjj.type==indkk.type:
                        if (indjj.dagger and (indjj.num in alld)) or (not indjj.dagger and (indjj.num in alls)):
                            if not indjj.num in pair: pair.append(copy.deepcopy(indjj.num))
                            used.append(kk)
                            pair.append(copy.deepcopy(indkk.num))
                if pair: 
                    pair.sort()
                    if not pair in pairs:
                        pairs.append(copy.deepcopy(pair))
                    else:
                        for yy in range(len(pairs)):
                            if pair==pairs[yy]: outyy=yy
                        pairs.pop(outyy)
        for pair in pairs:
            cntd=-1
            cnts=-1
            for ii in range(len(mxx.tensors)):
                iiindices=mxx.tensors[ii].indices.indices
                for kk in iiindices:
                    if (kk.num in pair) and kk.dagger:
                        cntd+=1
                        kk.num=copy.deepcopy(pair[cntd])
                    elif (kk.num in pair) and (not kk.dagger):
                        cnts+=1
                        kk.num=copy.deepcopy(pair[cnts])
        return mxx
        

    def listindiceswith(self,
                      dagger=-1,
                      types="",
                      comp=0):
        # -> [ Indices, ..} (copied)
        out=[]
        for xx in self.tensors:
            out+=xx.listindiceswith(dagger,types,comp)
        return out    
        
    #def analyze(self,nprint=0):
    def analyze(self,nprint=0,listgeneral=["v","f"],dorelabel=1,noadd=0):
        import copy
        if dorelabel:
            my_PTs=self.relabel()
        else:
            my_PTs=copy.deepcopy(self)

        myTensors=[]
        for itensor in range(len(my_PTs.tensors)):
            target_t=my_PTs.tensors[itensor]
            iabb=target_t.abb
            dictlabel={}

            # classify indices according to their connectivity
            for iindx in range(len(target_t.indices)):
                t_indx=target_t.indices[iindx]
                noprojection=0
                for jtensor in range(len(my_PTs.tensors)):
                    if itensor==jtensor: continue
                    if my_PTs.tensors[jtensor].contains(t_indx):
                        noprojection=1
                        break
                    
                jabb=my_PTs.tensors[jtensor].abb

                if noprojection:
                    newabb=jabb
                else:
                    newabb="P"
                    if t_indx.type=="particle":
                        newabb+="p"
                    elif t_indx.type=="hole":
                        newabb+="h"
                    elif t_indx.type=="general":
                        newabb+="g"
                    else:
                        print "Someting is wrong!!",t_indx
                        
                listkeys=dictlabel.keys()
                if not newabb in listkeys:
                    dictlabel[newabb]=[t_indx]
                else:
                    dictlabel[newabb].append(t_indx)

            # classify indices according to their type
            listAIs=[]
            #listAI=[]
            listkeys=dictlabel.keys()
            for xx in listkeys:
                listAI=[]
                #cnn=ConnectionIndex(iabb,xx)
                cnn=ConnectionIndex([iabb],[xx])
                for yy in dictlabel[xx]:
                    isin=0
                    for ii in range(len(listAI)):
                        zz=listAI[ii]
                        #if zz.showdagger() == yy.dagger and \
                        #   zz.showtype()   == yy.type   and \
                        #   zz.showcomp()   == yy.comp   :
                        if zz.hasthesametype(yy):
                            listAI[ii].indices.append(yy)
                            isin=1
                            break
                    if not isin:    
                        if target_t.symbol in listgeneral:
                            irng=Indexrange("general")
                        else:
                            irng=Indexrange(yy.type,yy.comp)
                            
                        #listAI.append(AnalyzedIndices([yy],xx))
                        #listAI.append(AnalyzedIndices([yy],cnn))
                        listAI.append(AnalyzedIndices([yy],cnn,irng))
                        
                listAIs+=listAI        
                #for yy in listAI:        
                #    print yy

            listAIs.sort()    

            myLAI=ListAnalyzedIndices(listAIs)    
            #print "\no Target",target_t
            #print myLAI
            #print myLAI.show(0)

            myLAI.permutable=myLAI.getpermutable_1()

            myTensor=AnalyzedTensor(target_t.symbol,
                                    myLAI,
                                    iabb,
                                    [target_t.symbol])
            #print myTensor
                                                  
            myTensors.append(myTensor)
            
        out=AnalyzedTensorSequence(myTensors)

        if nprint:
            print "\no Analyzed Tensors"
            print out

        return out    

class ListPrimitiveTensorSequence:
    def __init__(self,tensorsequences):
        # tensorsequences <- [(Factor,PrimitiveTensorSequence)]
        self.tensorsequences = tensorsequences

    def __getitem__(self,key):
        return self.tensorsequences[key]

    def __len__(self):
        return len(self.tensorsequences)
        
    def __str__(self):
        return self.show()
    
    def show(self):
        show=""
        for xx in self.tensorsequences:
            show+=xx[0].show()
            show+=" "
            show+=xx[1].show()
            show+="\n"
        return show    

    def __add__(self,other):
        import copy
        out =[]
        out+=copy.deepcopy(self.tensorsequences)
        out+=copy.deepcopy(other.tensorsequences)
        return ListPrimitiveTensorSequence(out)
        
    def multiplysign(self,sign):
        # sign <- Sign
        import copy
        my=copy.deepcopy(self)
        out=[]
        for xx in my.tensorsequences:
            out.append((xx[0]*sign,xx[1]))
        return ListPrimitiveTensorSequence(out)    
        
class TensorContraction:
    def __init__(self,
                 target,
                 factor,
                 permutations,
                 sum,
                 tensors,
                 restricted=0):
        # target       <- AnalyzedTensor
        # factor       <- Factor
        # permutations <- Permutations
        # sum          <- ListAnalyzedIndices
        # tensors      <- AnalyzedTensorSequence
        # restricted   <- Integer
        
        self.target       = target
        self.factor       = factor
        self.permutations = permutations
        self.sum          = sum
        self.tensors      = tensors
        self.restricted   = restricted
        self.ordering     = []
        
    def __str__(self):
        return self.show()

    def show(self,showtarget=0):
        show = ""
        if showtarget:
            show+=self.target.show(restricted=self.restricted)
            show+=" += "
        show+=self.factor.show()
        show+=self.permutations.show(restricted=self.restricted)
        show+=self.sum.sum_show(restricted=self.restricted)
        show+=self.tensors.show(restricted=self.restricted)
        return show

    def tex(self):
        import copy
        tex=""
        #tex+=self.target.tex()
        tex+=self.factor.tex()

        tmpperm=self.permutations.permutations
        if len(tmpperm)>0:
            for jj in tmpperm:
                kk=copy.deepcopy(jj.extract())
                tex+="P"+"_{"+str(len(kk.listindices))+"}"

        tex+=self.tensors.tex()
        return tex

    def restrict(self,nprint=0):
        import copy

        mysign=copy.deepcopy(self.factor.sign)
        oldfrac=copy.deepcopy(self.factor.fraction)

        tmpfrac=self.tensors.estimatefraction(nprint)

        if not oldfrac==tmpfrac:
            print "Something is wrong in original tensor"
            print "in estimated and original fraction",tmpfrac,oldfrac
            
        myfrac=self.tensors.estimaterestrictedfraction(nprint)
        myfactor=Factor(mysign,myfrac)
        
        out=TensorContraction(copy.deepcopy(self.target),
                              myfactor,
                              copy.deepcopy(self.permutations),
                              copy.deepcopy(self.sum),
                              copy.deepcopy(self.tensors),
                              restricted=1)
        return out

    def hastlevel(self,level):
        import string
        if level==0: return 1
        tmp=self.tensors.tensors
        for ii in tmp:
            if ii.symbol.split("_")[0][1:]==str(level): return 1
        return 0

    def issameas(self,other):
        if not len(self.tensors.tensors)==len(other.tensors.tensors): 
            return 0
        
        ll=len(self.tensors.tensors)
        for ii in range(ll):
            selfsum=self.tensors.showsumindices()
            othersum=self.tensors.showsumindices()
            if not self.tensors.tensors[ii].indices.extract()\
                .issameas(other.tensors.tensors[ii].indices.extract(),selfsum,othersum):
                return 0 
            if not self.tensors.tensors[ii].symbol==other.tensors.tensors[ii].symbol: 
                return 0                  
        return 1

    def isequalto(self,other):
        if not len(self.tensors.tensors)==len(other.tensors.tensors): 
            return 0

        ll=len(self.tensors.tensors)

        for ii in range(ll):
            selfsum=self.tensors.showsumindices()
            othersum=self.tensors.showsumindices()
            if not self.tensors.tensors[ii].indices\
                .isequalto(other.tensors.tensors[ii].indices):
                return 0 
            if not self.tensors.tensors[ii].symbol==other.tensors.tensors[ii].symbol: 
                return 0                  
        return 1

    def updateconnindex(self):
        import copy
        cnt1=0
        for xx in self.tensors.tensors:
            for yy in xx.indices.listindices:
                bkup=copy.deepcopy(yy.symbol)
                ynum=yy.indices[0].num
                cnt2=0
                flag=0
                for zz in self.tensors.tensors:
                    if cnt1==cnt2: 
                        cnt2+=1
                        continue
                    flag=0
                    for ww in zz.indices.listindices:
                        numlist=[]
                        for uu in ww.indices:
                            numlist.append(uu.num)
                        if ynum in numlist:
                            flag=1
                            break 
                    if flag: break
                    cnt2+=1
                if flag:
                    yy.symbol.others=[zz.symbol]
            cnt1+=1
        return self 

    def estimatecontractioncost(self,inordering,nprint=0):
        # ordering <- [ interger, ]
        # -> (ComputationalCost, ComputationalCost, String)
        import copy
        import string
        #############################################
        #        maxmem,maxopr is now LIST
        #############################################
        #ordering=range(len(self.tensors))
        ordering=copy.deepcopy(inordering)
        ii=ordering.pop(0)
        jj=len(self.tensors)
        ListTensor=[copy.deepcopy(self.tensors[ii])]
        abbs=[copy.deepcopy(self.tensors[ii].abb)]
        maxmem=[]
        maxopr=[]
        if nprint>1:
            print "\no Order :",inordering
        while ordering:
            ii=ordering.pop(0)
            jj-=1
            #print "bf",self.tensors[ii].indices
            #print "af",self.tensors[ii].indices.applyrestriction(abbs)
            #print self.tensors[ii],self.tensors[ii].applyrestriction(abbs)
            ListTensor.append(copy.deepcopy(self.tensors[ii]))
            #ListTensor.append(self.tensors[ii].applyrestriction(abbs))
            abbs.append(copy.deepcopy(self.tensors[ii].abb))
            TS=AnalyzedTensorSequence(ListTensor)
            #print "bf",TS
            #print "af",TS.updateindices()
            TS=TS.updateindices()
            
            mem=TS.estimatememorycost(restricted=self.restricted)
            opr=TS.estimateoperationcost(restricted=self.restricted)

            #print TS.listindices()
            #print TS.listindices().dictconnectionindices()
            #print "sum :",TS.showsumindices()
            #print "out :",TS.showsummedindices()

            tmplist=TS.showsummedindices()
            tmpabb =TS.contractionabb()
            #tmpabb =string.join(TS.listabbs(),"")
            tmpsym ="i"+str(jj)
            tmpsymmetry=TS.totalsymmetry()

            #print abbs
            #print tmplist
            #print TS.showsumindices()
            IM=AnalyzedTensor(tmpsym,tmplist,tmpabb,tmpsymmetry)
            ListTensor=[IM]

            #if nprint>1:
            #    print tmpabb," : ",IM," = ",TS
            #    print "Memory Cost",   mem.show(1),\
            #          "Operation Cost",opr.show(1)

            #if not maxmem or maxmem < mem:
            #    maxmem=copy.deepcopy(mem)
            #if not maxopr or maxopr < opr:
            #    maxopr=copy.deepcopy(opr)
            maxmem.append(copy.deepcopy(mem))
            maxopr.append(copy.deepcopy(opr))
        if not len(ordering)==1:
            maxmem.sort()
            maxmem.reverse()
            maxopr.sort()
            maxopr.reverse()
        memlist=Memlist(maxmem)
        oprlist=Oprlist(maxopr)
        if nprint:        
            print "Order",inordering,\
                  "Peak Cost: Memory",maxmem[0].show(), \
                  "Operation",maxopr[0].show()
        if nprint>1:
            print 

        return memlist,oprlist,tmpabb

    def findthebestcontractionorder(self,nprint=0,memory=0,shift=0):
        import copy
        if len(self.tensors)==1:
            minorder={self.tensors.tensors[0].abb:[0]}
            keys=minorder.keys()
            if nprint:
                for xx in keys:
                    print xx," : ",minorder[xx]
            return minorder,[]
        if not shift:
            orderings=GenerateOrdering(len(self.tensors))
        else:
        #else:
        #    orderings=GenerateOrdering(len(self.tensors))
            comp_tensors=[]
            else_tensors=[]
            comp_orderings=[]
            else_orderings=[]
            
            for ii in range(len(self.tensors)):
                flag=0
                for jj in self.tensors[ii].indices.listindices:
                    if jj.indices[0].comp: 
                        flag=1
                        comp_tensors.append(ii)
                        break
                if not flag:
                    else_tensors.append(ii) 
    
            if len(comp_tensors)==0 or len(else_tensors)==0:
                orderings=GenerateOrdering(len(self.tensors))
            else:
                if len(comp_tensors)==1:
                    comp_orderings.append(comp_tensors)
                else:
                    tmp_orderings=GenerateOrdering(len(comp_tensors))
                    for ii in range(len(tmp_orderings)):
                         tmpjj=[]
                         for jj in range(len(comp_tensors)):
                             tmpjj.append(comp_tensors[tmp_orderings[ii][jj]])
                         comp_orderings.append(copy.deepcopy(tmpjj))
    
                if len(else_tensors)==1:
                    else_orderings.append(else_tensors)
                else:
                    #tmp_orderings=GenerateOrdering(len(else_tensors))
                    tmp_orderings=GeneratePermutation(len(else_tensors))
                    for ii in range(len(tmp_orderings)):
                         tmpjj=[]
                         for jj in range(len(else_tensors)):
                             tmpjj.append(else_tensors[tmp_orderings[ii][jj]])
                         else_orderings.append(copy.deepcopy(tmpjj))
    
                orderings=[]
                for ii in range(len(comp_orderings)):
                    for jj in range(len(else_orderings)):
                        tmpij=[]
                        for kk in range(len(comp_tensors)):
                            tmpij.append(comp_orderings[ii][kk])
                        for kk in range(len(else_tensors)):
                            tmpij.append(else_orderings[jj][kk])
                        orderings.append(tmpij)

        minorder={}
        #print
        usedkey=[]
        id=-1
        for ordering in orderings:
            id+=1
            #mem,opr,abb=self.estimatecontractioncost(ordering,nprint)
            mem,opr,abb=self.estimatecontractioncost(ordering,0)
            #print ordering,mem,"*",opr,"*",abb

            if id==0:
                minmem=mem
                minopr=opr
                minorder[abb]=ordering
                continue

            if memory:
                #memory,operation 
                if minmem > mem:
                    minmem=mem
                    minopr=opr
                    minorder={abb:ordering}
                elif minmem==mem and minopr > opr:
                    minmem=mem
                    minopr=opr
                    minorder={abb:ordering}
                elif minmem==mem and minopr==opr:
                    minorder[abb]=ordering
            else:
                #operation,memory
                if minopr > opr:
                    minmem=mem
                    minopr=opr
                    minorder={abb:ordering}
                    usedkey.append(abb)
                elif minopr==opr and minmem > mem:
                    minmem=mem
                    minopr=opr
                    minorder={abb:ordering}
                    usedkey.append(abb)
                elif minmem==mem and minopr==opr:
                    if abb in usedkey:
                       #minorder[tmp]=ordering
                       continue
                    else:
                       minorder[abb]=ordering

        keys=minorder.keys()
        keys.sort()
        #keys.reverse()
	for xx in keys:
	    if self.tensors.tensors[minorder[xx][0]].symbol[0]=="t" or \
	       self.tensors.tensors[minorder[xx][0]].symbol[0]=="u":
	        ptmp=copy.deepcopy(minorder[xx][0])
                minorder[xx][0]=copy.deepcopy(minorder[xx][1])
	        minorder[xx][1]=ptmp
        nprint=1
        if nprint:
            for xx in keys:
                print xx," : ",minorder[xx]
            print "Peak Cost: Memory",minmem, \
                  "Operation",minopr
        return minorder,minopr

#    def cancel_rule10(self,nprint=0):
#        import copy
#        nprint=1
#        mylisttensor=copy.deepcopy(self.tensors.tensors)
#        exist=0
#        for ii in range(len(mylisttensor)):
#            for jj in range(ii):
#                if mylisttensor[ii].indices.isequalto(mylisttensor[jj].indices):
#                    exist=1
#        if not exist:
#            return self
#        if nprint:
#            print "++ Cancel rule10 ++"
#        expected_p=self.tensors.estimatepermutation()
#        #print expected_p
#        if nprint:
#            print self.tensors
#            print "Expected permutations are"
#            print expected_p
#            print "Original Permutations are"
#            print self.permutations

    def pickintermediate(self,xlist):
        import copy
        xx=copy.deepcopy(self)
        tex=""
        scr={}
        scr_num=[]
        temp_tensors=[]
        comp_tensors=[]
        comp_indices=[]
        usedlist=[]
        ipp=0
        # picking V, X, P intermediates
        for ii in range(len(xx.tensors.tensors)):
            for jj in xx.tensors.tensors[ii].indices.listindices:
                if len(jj.indices)<2: continue
                if jj.indices[0].comp: 
                    temp_tensors.append(copy.deepcopy(xx.tensors.tensors[ii]))
                    comp_indices.append(copy.deepcopy(jj))
                    usedlist.append(ii)
                    break
        # picking B intermediate
        for iii in range(len(xx.tensors.tensors)):
            ii=xx.tensors.tensors[iii]
            if ii.symbol[0]=="f":
                if ii.indices.listindices[0].indices[0].comp and \
                    ii.indices.listindices[1].indices[0].comp:
                    scr[iii]=copy.deepcopy(ii) 
                    usedlist.append(iii)
                    scr_num.append(copy.deepcopy(ii.indices.listindices[0].indices[0].num))
                    scr_num.append(copy.deepcopy(ii.indices.listindices[1].indices[0].num))
        if scr.keys():
            for iii in range(len(xx.tensors.tensors)):
                ii=xx.tensors.tensors[iii]
                if ii.symbol[0]=="R":
                    for jj in ii.indices.listindices:
                        if jj.indices[0].comp:
                            if jj.indices[0].num in scr_num:
                                scr[iii]=copy.deepcopy(ii)
                                usedlist.append(iii)
                                break
        if len(scr.keys())==3:
            flag=0
            keys=scr.keys()
            for jj in scr[usedlist[1]].indices.listindices:
                if jj.indices[0].comp:
                    if not jj.indices[0].num in scr_num:
                         scr_num2=copy.deepcopy(jj.indices[0].num)
            for jj in scr[usedlist[2]].indices.listindices:
                if jj.indices[0].comp:
                    if (not jj.indices[0].num in scr_num) and jj.indices[0].num==scr_num2:
                        flag=1
            if flag:
                usedlist.sort()
                for ii in usedlist:
                    temp_tensors.append(scr[ii]) 
                 
        if usedlist:
            if len(usedlist)<4:
                num_int=1
                comp_tensors.append(temp_tensors)
            # sometimes there are two intermidiates (V & X)
            if len(usedlist)==4:
                num_int=2
                cta=comp_indices[0]
                ctb=comp_indices[1]
                ctc=comp_indices[2]
                n1=[]
                if   cta.isequalto(ctb,nodagger=1,nonum=0,nocon=1): n1=[0,1]
                elif cta.isequalto(ctc,nodagger=1,nonum=0,nocon=1): n1=[0,2]
                else :                     n1=[0,3]
                c0=[]
                c1=[]
                for ii in range(4):
                    if ii in n1:
                        c0.append(temp_tensors[ii])
                    else:
                        c1.append(temp_tensors[ii])
                comp_tensors.append(c0)
                comp_tensors.append(c1)
        else: num_int=0

        for pp in range(num_int):         
            yysymbol=""
            for qq in range(len(comp_tensors[pp])):
                yysymbol+=comp_tensors[pp][qq].symbol[0]
            if   yysymbol=="RR" : yysymbol="Xs"
            elif yysymbol=="vR" : yysymbol="Vr"
            elif yysymbol=="Rv" : yysymbol="Vd"
            elif yysymbol=="RvR": yysymbol="Ps"
            elif yysymbol=="RfR": yysymbol="Bs"
            else: print "intermediate error" 
                
            yyt=AnalyzedTensorSequence(comp_tensors[pp]) 
            yysum=yyt.showsumindices()
            yyperm=yyt.estimatepermutation()
            #yysign=yyt.estimatesign(withprojection=1)
            yysign=Sign()
            yyfraction=yyt.estimatefraction(comp=0)
            yyfactor=Factor(yysign,yyfraction)
            yysummed=yyt.showsummedindices()
            yysymmetry=yyt.totalsymmetry()
            yyabb=yysymbol
            yytarget=AnalyzedTensor(yysymbol,yysummed,yyabb,yysymmetry)
            yy=TensorContraction(yytarget,yyfactor,yyperm,yysum,yyt)
            yy_f=0
            for ii in range(len(xlist)):
                ixx=xlist[ii]
                if ixx.issameas(yy):
                    yy.target.symbol=ixx.target.symbol
                    yy_f=1
            if not yy_f:
                tex+=yytarget.tex()+"&\\hspace{-3pt}=\\hspace{-3pt}&"
                tex+=yy.factor.tex()
                for ii in range(len(comp_tensors[pp])):
                    tex+=comp_tensors[pp][ii].tex()
                tex+="\\\\\n"
                xlist.append(yy)
                print yytarget,"=",yy 
            xx.tensors.tensors.append(yy.target)
            
        usedlist.sort()
        usedlist.reverse()
        for ii in usedlist:
            xx.tensors.tensors.pop(ii)
        return xx,tex

    def findreusable(self,other):
        import copy
        if len(self.tensors.tensors)==1 or \
           len(other.tensors.tensors)==1:
            return 0
        tmp=copy.deepcopy(self.tensors.tensors[0:2])
        myats_org=AnalyzedTensorSequence(tmp)
        tmp=copy.deepcopy(other.tensors.tensors[0:2])
        yourats_org=AnalyzedTensorSequence(tmp)

        self0 =copy.deepcopy(self.tensors.tensors[0])
        self1 =copy.deepcopy(self.tensors.tensors[1])
        self0.indices=self0.indices.extract()
        self1.indices=self1.indices.extract()
        myts =[]
        myts.append(self0)
        myts.append(self1)
        myats=AnalyzedTensorSequence(myts)
        list1=myats.showsummedindices().extract()
        other0=copy.deepcopy(other.tensors.tensors[0])
        other1=copy.deepcopy(other.tensors.tensors[1])
        other0.indices=other0.indices.extract()
        other1.indices=other1.indices.extract()
        yourts =[]
        yourts.append(other0)
        yourts.append(other1)
        yourats=AnalyzedTensorSequence(yourts)
        list2=yourats.showsummedindices().extract()


        # if the reusable intermediate has the permutation operator in it,
        # special care is needed. checking weather all the permutation 
        # operators are the same between self and other.
        if self0.issameas(other0,list1,list2) and\
           self1.issameas(other1,list1,list2):
            p1=[]
            p2=[]
            for ii in myats_org.estimatepermutation().permutations:
                usedp=[]
                for jj in ii.extract().listindices:
                    for kk in range(len(list1)):
                        if jj.indices[0].num==list1[kk].indices[0].num:
                            usedp.append(kk)
                            break
                p1.append(copy.deepcopy(usedp))
            for ii in yourats_org.estimatepermutation().permutations:
                usedp=[]
                for jj in ii.extract().listindices:
                    for kk in range(len(list2)):
                        if jj.indices[0].num==list2[kk].indices[0].num:
                            usedp.append(kk)
                            break
                p2.append(copy.deepcopy(usedp))
            p1.sort()
            p2.sort()
            if not p1==p2:
                return 0
            return 1
        return 0

    def breakdowntooperationtree(self,ordering,inpfactor,nline,nprint=0):
        import string
        import copy

        n_tensor=len(self.tensors.tensors)
        mytc    = copy.deepcopy(self)
        mytc_t  = mytc.tensors.tensors
        mytc_pm = copy.deepcopy(mytc.permutations)
        mytc_f  = copy.deepcopy(mytc.factor)
        saveall =[]
    
        for ii in ordering:
            saveall.append(copy.deepcopy(mytc_t[ii])) 
        saveall.reverse()
        saveall.pop()
        #print mytc.sum
        #print mytc.target
        #print mytc.restricted

        tmpindices=self.tensors.showsummedindices()
        for ii in range(len(tmpindices)):
            for jj in tmpindices[ii].indices:
                jj.dagger=abs(jj.dagger-1)
        tmpindices.sort()
        projection=tmpindices
        #print projection
            
        lpidx=copy.deepcopy(mytc.tensors)

        # init
        #################
        newpermutations=[]
        usedtensors    =[]
        newfactor      =Factor()
        cnnsign        =Sign()
        cnndict        ={}

        # first pair
        #################
        mytensors=[]
        myoperator=[]
        ii=ordering[0]
        mytensors.append(copy.deepcopy(mytc_t[ii]))
        if not len(ordering)==1:
            jj=ordering[1]
            mytensors.append(copy.deepcopy(mytc_t[jj]))

        mytensors.sort()
        mytensors.reverse()

        myts=AnalyzedTensorSequence(mytensors)

        if not len(ordering)==1:
            usedind=[]
            myposition=mytensors[0].abb.split("_")[1]
            for jj in range(len(mytensors[0].indices.listindices)):
                if jj in usedind: continue
                aijj=mytensors[0].indices.listindices[jj]
                for kk in range(jj+1,len(mytensors[0].indices.listindices)):
                    if kk in usedind: continue
                    aikk=mytensors[0].indices.listindices[kk]
                    if not aijj.indices[0].type==aikk.indices[0].type:
                        continue
                    if not aijj.indices[0].dagger==aikk.indices[0].dagger:
                        continue
                    if not aijj.indices[0].comp==aikk.indices[0].comp:
                        continue
                    if aijj.symbol.others[0]=="Ph": continue
                    if aijj.symbol.others[0]=="Pp": continue
                    if not \
                       (aijj.symbol.others[0].split("_")[1]>myposition and \
                        aikk.symbol.others[0].split("_")[1]>myposition) or \
                       (aijj.symbol.others[0].split("_")[1]<myposition and \
                        aikk.symbol.others[0].split("_")[1]<myposition): 
                        continue
                    for xx in aikk.indices:
                        aijj.indices.append(xx)
                    usedind.append(kk)
            usedind.sort()
            usedind.reverse()
            
            for jj in usedind:
                if not jj<len(mytensors[0].indices.listindices):
                    print jj,usedind,mytensors[0]
                mytensors[0].indices.listindices.pop(jj)

        #print myts
        mypermutation=myts.estimatepermutation()
        mysummation  =myts.showsumindices()
        myfraction   =myts.estimatefraction()
        #mysign       =lpidx.estimatesign(withprojection=1)
        #myfactor     =Factor(mysign,myfraction)

        newout=myts.showsummedindices()

        tarsymbol    ="J"+str(max(len(ordering)-2,0))+"_"+str(nline)
        tarabb   =tarsymbol+str(len(newout.a2list())/2)
        tarsymmetry=myts.totalsymmetry()
        mytarget=AnalyzedTensor(tarsymbol,newout,tarabb,tarsymmetry)

        # myfactor=+1.0
        #mysign     = Sign()
        #myfraction = Fraction()
        if not len(ordering)==1:
            myfraction = myts.estimatefraction(norule7=1)
            for xx in saveall:
                if xx.isequalto(mytc_t[ordering[0]],comp=1):
                    myfraction*=Fraction(1,2)
            saveall.pop()
            for xx in saveall:
                if xx.isequalto(mytc_t[ordering[1]],comp=1):
                    myfraction*=Fraction(1,2)
            if not len(ordering)==2:
                saveall.pop()
        
        else:
            myfraction = Fraction()

        myopfraction=Fraction()
        if not len(ordering)==1:
            myopfraction*=mytensors[1].fraction

        mysign     = Sign()
            
        myfactor   = Factor(mysign,myfraction)

        mytc=TensorContraction(mytarget,myfactor,mypermutation,\
                               mysummation,myts)

        if not len(ordering)==1:
            tmp=copy.deepcopy(mytensors[1])
            tmpf=copy.deepcopy(inpfactor)
            tmpf.fraction=copy.deepcopy(myopfraction) 
            tmpperm=copy.deepcopy(mytensors[1].indices.permutable)
            myoperator.append(LastOperator(tmp,tmpf,tmpperm))
        else:
            tmp=copy.deepcopy(mytensors[0])
            tmpf=copy.deepcopy(inpfactor)
            tmpf.fraction=copy.deepcopy(myopfraction) 
            tmpperm=copy.deepcopy(mytensors[0].indices.permutable)
            myoperator.append(LastOperator(tmp,tmpf,tmpperm))


        mysymbol    ="J"+str(max(len(ordering)-2,0))+"_"+str(nline)
        #mysymbol    ="I"+str(max(len(ordering)-2,0))

        #mysymbol    =mytc.getsymbol()
        myabb       =mytc.getabb()
        myoutindices=mytc.tensors.showsummedindices()
        mysymmetry  =mytc.tensors.totalsymmetry()

        mypermutable=[]
        prevperm=[]
        if not len(ordering)==1:
            mypermutable=myoutindices.getpermutable(\
                            mytensors[0].indices.permutable,\
                            mytensors[1].indices.permutable)
            prevperm=copy.deepcopy(mypermutable)
        else:
            mypermutable=copy.deepcopy(mytensors[0].indices.permutable)
#        for xx in mypermutable: print "@@@",xx
#        print "###################################"
            

        myot=OperationTree(operation=mytc,outindices=myoutindices,\
                        symbol=mysymbol,permutable=mypermutable,\
                        children=[],operator=myoperator)
        myot.operation.target.indices.permutable=copy.deepcopy(mypermutable) 
     
        prot=myot
        #print prot

        newpermutations.append(mypermutation)
        newfactor*=myfactor
        for xx in mytensors:
            usedtensors.append(xx)

        # The others (1,n_tensor)
        #########################
        for ii in range(2,len(ordering)):
            mytensor  = copy.deepcopy(mytc_t[ordering[ii]])
            tmptensors= [copy.deepcopy(mytc_t[ordering[ii]]),\
                         AnalyzedTensor(symbol=copy.deepcopy(mysymbol),\
                                      indices=copy.deepcopy(myoutindices),\
                                      symmetry=copy.deepcopy(mysymmetry))]
            mytensors = copy.deepcopy(tmptensors)
            tmptensors[1].indices.permutable=copy.deepcopy(prevperm)
            #tmptensors.sort()
            #tmptensors.reverse()

            tmpts= AnalyzedTensorSequence(tmptensors)

            usedind=[]
            myposition=tmptensors[0].abb.split("_")[1]
            for jj in range(len(tmptensors[0].indices.listindices)):
                if jj in usedind: continue
                aijj=tmptensors[0].indices.listindices[jj]
                for kk in range(jj+1,len(tmptensors[0].indices.listindices)):
                    if kk in usedind: continue
                    aikk=tmptensors[0].indices.listindices[kk]
                    if not aijj.indices[0].type==aikk.indices[0].type:
                        continue
                    if not aijj.indices[0].dagger==aikk.indices[0].dagger:
                        continue
                    if not aijj.indices[0].comp==aikk.indices[0].comp:
                        continue
                    if aijj.symbol.others[0]=="Ph": continue
                    if aijj.symbol.others[0]=="Pp": continue
                    if not \
                       (aijj.symbol.others[0].split("_")[1]>myposition and \
                        aikk.symbol.others[0].split("_")[1]>myposition) or \
                       (aijj.symbol.others[0].split("_")[1]<myposition and \
                        aikk.symbol.others[0].split("_")[1]<myposition): 
                        continue
                    for xx in aikk.indices:
                        aijj.indices.append(xx)
                    usedind.append(kk)
            usedind.sort()
            usedind.reverse()
            
            for jj in usedind:
                if not jj<len(tmptensors[0].indices.listindices):
                    print jj,usedind,tmptensors[0]
                tmptensors[0].indices.listindices.pop(jj)

            mypermutation=tmpts.estimatepermutation()
            mysummation  =tmpts.showsumindices()

            newout=tmpts.showsummedindices()
            tarsymbol    ="J"+str(max(len(ordering)-ii-1,0))+"_"+str(nline)
            tarabb   =tarsymbol+str(len(newout.a2list())/2)
            tarsymmetry=tmpts.totalsymmetry()
            mytarget=AnalyzedTensor(tarsymbol,newout,tarabb,tarsymmetry)

            tmpsign     = Sign()
            tmpfraction = copy.deepcopy(tmpts.estimatefraction())
            if not ii==(len(ordering)-1):
                for xx in saveall:
                    if xx.isequalto(mytensor,comp=1): 
                        tmpfraction*=Fraction(1,2)
                saveall.pop()

            tmpfactor   = Factor(tmpsign,tmpfraction)

            tmptc=TensorContraction(mytarget,tmpfactor,mypermutation,\
                                    mysummation,tmpts)

            #mysymbol    ="I"+str(max(len(ordering)-ii-1,0))
            mysymbol    ="J"+str(max(len(ordering)-ii-1,0))+"_"+str(nline)
            #mysymbol=tmptc.getsymbol()
            myoutindices=tmptc.tensors.showsummedindices()
            mysymmetry=tmptc.tensors.totalsymmetry()

            mypermutable=myoutindices.getpermutable(\
                        mytensors[0].indices.permutable,\
                        prevperm)
            prevperm=copy.deepcopy(mypermutable)
         
            myot= OperationTree(operation=tmptc,\
                                outindices=myoutindices,\
                                symbol=mysymbol,\
                                permutable=mypermutable,\
                                children=[prot],operator=[])
            myot.operation.target.indices.permutable=copy.deepcopy(mypermutable) 
            prot=copy.deepcopy(myot)

            newpermutations.append(mypermutation)
            newfactor*=myfactor
            for xx in mytensors:
                usedtensors.append(xx)

        return myot

    def getsymbol(self):
        mysymbol=""
        for xx in range(len(self.tensors.tensors)):
            mysymbol+=self.tensors.tensors[xx].symbol
        return mysymbol

    def getabb(self):
        myabb=""
        for xx in range(len(self.tensors.tensors)):
            myabb+=self.tensors.tensors[xx].abb
        return myabb

    def relabel(self,ordering):
        import copy
        import string
        out=copy.deepcopy(self)
        myts=out.tensors.tensors
        
        count=0
        for ii in ordering:
            count+=1
            abb=copy.deepcopy(myts[ii].abb.split("_")[0])
            abb+="_"+str(len(ordering)-count)
            myts[ii].abb=abb
        return out 

    def a2c(self):
        import copy
        mytarget = self.target.a2c()
        myfactor = copy.deepcopy(self.factor)
        mypermutations= copy.deepcopy(self.permutations)
        mysum = self.sum.a2c()
        mytensors = self.tensors.a2c()
        myrestricted = copy.deepcopy(self.restricted)

        return CodeTensorContraction(mytarget,myfactor,mypermutations,\
                                     mysum,mytensors,myrestricted)
 
class Memlist:
    def __init__(self,mem):
        self.mem=mem

    def __str__(self):
        show=""
        for xx in self.mem:
            show+=xx.show()
            show+=" "
        show=show[:-1]
        return show

    def __cmp__(self,other):
        for ii in range(len(self.mem)):
            if self.mem[ii] < other.mem[ii]:
                return -1
            elif self.mem[ii] > other.mem[ii]:
                return 1
            else: continue
        return 0

class Oprlist:
    def __init__(self,opr):
        self.opr=opr

    def __str__(self):
        show=""
        for xx in self.opr:
            show+=xx.show()
            show+=" "
        show=show[:-1]
        return show

    def __cmp__(self,other):
        if len(self.opr)>len(other.opr):
            rangeopr=len(other.opr) 
        else:
            rangeopr=len(self.opr) 
        for ii in range(rangeopr):
            if self.opr[ii] < other.opr[ii]:
                return -1
            elif self.opr[ii] > other.opr[ii]:
                return 1
            else: continue
        return 0

class LastOperator:
    def __init__(self,tensor,factor,permutable=[]):
        self.tensor     =tensor
        self.factor     =factor
        self.permutable =permutable
    
    def __str__(self):
        return self.show()

    def operator2ctc(self):
        import copy
        mytarget=copy.deepcopy(self.tensor)
        myfactor=copy.deepcopy(self.factor)
        mypermutation=Permutations()
        mysummation=ListAnalyzedIndices([],permutable=copy.deepcopy(self.permutable))
        myts=AnalyzedTensorSequence([copy.deepcopy(self.tensor)])
        return TensorContraction(mytarget,myfactor,mypermutation,\
                                 mysummation,myts).a2c()
        
    def show(self):
        show=""
        show+=self.factor.show()
        show+=self.tensor.show(showsym=0,showsize=0)
        return show

    def tex(self):
        #show=self.factor.tex()
        show+=self.tensor.tex()
        return show
 
    def issameas(self,other,list1,list2):
        if not self.tensor.issameas(other.tensor,list1,list2):
            return 0
        return 1

class ListTensorContraction:
    def __init__(self,tensorcontraction,filename=""):
        # tensorcontraction <- [TensorContraction, ]
        self.tensorcontraction=tensorcontraction
        self.filename=filename

    def __getitem__(self,key):
        return self.tensorcontraction[key]
    
    def __str__(self):
        return self.show()
    
    def show(self):
        show=""
        for xx in self.tensorcontraction:
            show+=xx.show()
            show+="\n"
        show=show[:-2]
        return show

    def tex(self,filename,level=0):
        if not self.tensorcontraction:
            print "no tensorcontraction"
            return self
        tex=""
        tex+=self.tensorcontraction[0].target.tex()+"="
        for xx in self.tensorcontraction:
            if xx.hastlevel(level):
                tex+=xx.tex()
                tex+="\n"
        outfile=open(filename,'w')
        outfile.write(tex) 
        outfile.close()
        return self

    def delete_rwithpp(self,short=1,sa=0):
        import copy
        import string
        ltc=copy.deepcopy(self.tensorcontraction)
        deletelist=[]
        cnt=-1
        for yy in ltc:
            cnt+=1
            flag2=0
            for id in range(len(yy.tensors.tensors)):
                if short:
                    yy.tensors.tensors[id].symbol=yy.tensors.tensors[id].symbol.split("_")[0]+"_"+str(id)
                ii=yy.tensors.tensors[id]
                if ii.symbol[0]=="R": 
                    flag=0
                    for jj in ii.indices.listindices:
                        if jj.indices[0].comp: flag=1
                    if flag==0:
                        flag2=1
                        break
                    if sa and flag==1:
                        flag2=1
                        break
            if flag2:
                deletelist.append(cnt)
                continue
            if short:
                yy=yy.updateconnindex()
                yy.factor.fraction=yy.tensors.estimatefraction(comp=1)
        deletelist.reverse()
        for ii in deletelist:
            ltc.pop(ii)
        out=ListTensorContraction(ltc)
        return out

    def combine_Fc(self):
        import copy
        import re
        ltc=copy.deepcopy(self).tensorcontraction
        for xx in ltc:
            xx=xx.updateconnindex()
            dellist=[]
            ix=-1
            for ii in xx.tensors.tensors:
                flag2=0
                ix+=1
                if not ii.symbol[0]=="R": continue
                ip=-1
                for yy in ii.indices.listindices:
                    ip+=1 
                    if len(yy.indices)==2 and (yy.symbol.others[0][0]=="t" or\
                                               yy.symbol.others[0][0]=="s" or\
                                               yy.symbol.others[0][0]=="l")\
                                          and yy.indices[0].type=="hole":
                        inum=yy.indices[0].num 
                        iy=-1
                        flag=0
                        for jj in xx.tensors.tensors:
                            iy+=1
                            if ix==iy: continue
                            if (not jj.symbol[0]=="t") and\
                               (not jj.symbol[0]=="s") and\
                               (not jj.symbol[0]=="l") : continue
                            iz=-1
                            for zz in jj.indices.listindices:
                                iz+=1
                                if zz.indices[0].num==inum: 
                                    flag=1
                                    break
                            if flag: 
                                dellist.append(iy)
                                cjj=copy.deepcopy(jj.indices.listindices)
                                cjj.pop(iz)
                                break
                        if flag: 
                            flag2=1
                            break
                if flag2: 
                    ii.indices.listindices.pop(ip)
                    for yy in cjj:
                        ii.indices.listindices.append(yy)
                    if jj.symbol[0]=="t":
                        ii.symbol=re.sub("R","Q",ii.symbol,1)
                        ii.abb=re.sub("R","Q",ii.symbol,1)
                        ii.symmetry=re.sub("R","Q",ii.symbol,1)
                    elif jj.symbol[0]=="s":
                        ii.symbol=re.sub("R","S",ii.symbol,1)
                        ii.abb=re.sub("R","S",ii.symbol,1)
                        ii.symmetry=re.sub("R","S",ii.symbol,1)
                    elif jj.symbol[0]=="l":
                        ii.symbol=re.sub("R","L",ii.symbol,1)
                        ii.abb=re.sub("R","L",ii.symbol,1)
                        ii.symmetry=re.sub("R","L",ii.symbol,1)
                    else:
                        print "something wrong"
            dellist.sort()
            dellist.reverse()
            for ii in dellist:
                xx.tensors.tensors.pop(ii)
            xx=xx.updateconnindex()
        return ltc

    def cabstex(self,nprint=0,shiftr12=1,level=0,combineFc=1,sa=0):
        import copy
        import string
        ltc_o=self.tensorcontraction
        ltc_p=[]
        ltc=[]
        if shiftr12:
            xlist=[]
            tex=""
            for xx in ltc_o:
                yy,yytex=xx.pickintermediate(xlist)
                tex+=yytex
                ltc_p.append(yy)
        for xx in ltc_p:
            if not xx.hastlevel(level):
                continue
            ltc.append(copy.deepcopy(xx))
            numall=[]
            cnt2=-1
            for ii in xx.tensors.tensors:
                cnt2+=1
                num=[]
                if not ii.symbol[0]=="R": continue
                cnt=0
                for jj in ii.indices.listindices:
                    if jj.indices[0].comp:
                        cnt+=1
                        num.append(jj.indices[0].num)
                if not cnt==2: 
                    continue
                else:
                    for jj in num:
                        if not jj in numall: numall.append(jj)
            table=maketable(numall)
            for plist in table:
                yy=copy.deepcopy(xx)
                for id in range(len(yy.tensors.tensors)):
                    ii=yy.tensors.tensors[id] 
                    for jj in ii.indices.listindices:
                        if jj.indices[0].num in plist:
                            jj.indices[0].comp=""
                ltc.append(yy)
        tmp=ListTensorContraction(ltc)
        tmp=tmp.delete_rwithpp(short=0,sa=sa)
        ltc=tmp.tensorcontraction

        if combineFc: ltc=ListTensorContraction(ltc).combine_Fc()

        myots=[]
        usedtc=[]
        for xx in ltc:
            bkup=copy.deepcopy(xx) 
            for yy in xx.tensors.tensors:   
                if yy.symbol[0]=="V" or yy.symbol[0]=="B" or\
                   yy.symbol[0]=="P" or yy.symbol[0]=="X":
                    continue
                else: yy.symbol=yy.symbol[0]
                
            xx.tensors=xx.tensors.a2p().analyze()
            bkup=copy.deepcopy(xx)
            for id in range(len(bkup.tensors.tensors)):
                ctensor=bkup.tensors.tensors[id]
                if len(ctensor.symbol)==1:
                    length=0
                    for qq in ctensor.indices.listindices:
                        for WW in qq.indices:
                            length+=1
                    length=length//2
                    ctensor.symbol+=str(length)
                ctensor.symbol=ctensor.symbol.split("_")[0]+"_"+str(id)
            bkup=bkup.updateconnindex()
            myfraction=bkup.tensors.estimatefraction(comp=1)
            
            min_order,minopr=xx.findthebestcontractionorder(nprint,memory=0)
            keys=min_order.keys()
            keys.sort()
            keys.reverse()
            ikey=keys[0]
            ordering=copy.deepcopy(min_order[ikey])

            xx=copy.deepcopy(xx.relabel(ordering))

            tmptensors=[] 
            for ii in range(len(ordering)):
                tmptensors.append(xx.tensors.tensors[ordering[ii]])
            tmptensors.reverse()
 
            xx.tensors=AnalyzedTensorSequence(tmptensors)
            mytarget=xx.tensors.showsummedindices().listindices

            pmytarget=[]
            for ii in mytarget:
                for jj in ii.indices:
                    pmytarget.append(jj)

            for ii in range(len(ordering)):
                ordering[len(ordering)-ii-1]=ii

            save=copy.deepcopy(xx)
                
            mxx=xx.tensors.a2p_abb()
            for pxx in mxx:
                pxx.abb=copy.deepcopy(pxx.symbol)
                pxx.symbol=pxx.symbol.split("_")[0]
            xx.tensors=mxx.analyze(dorelabel=0)
            xx.target.indices.listindices.sort()
            mxx=xx.tensors.a2p_abb()

#           if len(pmytarget)>0:
            mxx=mxx.relabelnum(pmytarget)
            for pxx in mxx:
                pxx.abb=copy.deepcopy(pxx.symbol)
                pxx.symbol=pxx.symbol.split("_")[0]

            xx.tensors=mxx.analyze(dorelabel=0)
            xx.target.indices.listindices.sort()
            for pxx in xx.tensors.tensors:
                pxx.indices.listindices.sort() 
            xx.tensors.tensors.reverse()
            ordering.reverse()

            mysign=xx.tensors.estimatesign(withprojection=1)
            myfactor=Factor(mysign,myfraction)
            xx.factor=myfactor

            xx.sum=xx.tensors.showsumindices()
            xx.permutations=xx.tensors.estimatepermutation()
            xx.ordering=copy.deepcopy(ordering)

            flag=0
            for yy in usedtc:
                if xx.isequalto(yy):
                    flag=1
                    print "::::::::"
                    print xx
                    print yy
                    print "::::::::"
                    break
            if not flag:
                usedtc.append(copy.deepcopy(xx))
        return ListTensorContraction(usedtc)


    def breakdown(self,nprint=0,shiftr12=1,reusable=1,combineFc=1,memory=0,sa=0):
        import copy
        import string
        tmpfn=copy.deepcopy(self.filename)
        reusablelist=[]
        ltc_o=self.tensorcontraction
        ltc_p=[]
        ltc=[]
        #ltc : [TensorContraction,]

        if shiftr12:
            xlist=[]
            tex=""
            for xx in ltc_o:
                yy,yytex=xx.pickintermediate(xlist)
                tex+=yytex
                ltc_p.append(yy)

        # making all conbination of a and a' for P indices
        # we only have to consider of R^{P}{P} type
        for xx in ltc_p:
            ltc.append(copy.deepcopy(xx))
            numall=[]
            cnt2=-1
            for ii in xx.tensors.tensors:
                cnt2+=1
                num=[]
                if not ii.symbol[0]=="R": continue
                cnt=0
                for jj in ii.indices.listindices:
                    if jj.indices[0].comp:
                        cnt+=1
                        num.append(jj.indices[0].num)
                if not cnt==2: 
                    continue
                else:
                    for jj in num:
                        if not jj in numall: numall.append(jj)
            table=maketable(numall)
            for plist in table:
                yy=copy.deepcopy(xx)
                for id in range(len(yy.tensors.tensors)):
                    ii=yy.tensors.tensors[id] 
                    for jj in ii.indices.listindices:
                        if jj.indices[0].num in plist:
                            jj.indices[0].comp=""
                ltc.append(yy)
    
        # tensor contractions containing R(pp) should be deleted
        tmp=ListTensorContraction(ltc)
        tmp=tmp.delete_rwithpp(short=0,sa=sa)
        ltc=tmp.tensorcontraction

        if combineFc: ltc=ListTensorContraction(ltc).combine_Fc()

        outflag=0
        myots=[]
        usedtc=[]
        for xx in ltc:
            for yy in xx.tensors.tensors:   
                if yy.symbol[0]=="V" or\
                   yy.symbol[0]=="B" or\
                   yy.symbol[0]=="P" or\
                   yy.symbol[0]=="X":
                    continue
                else:
                    yy.symbol=yy.symbol[0]
                
            xx.tensors=xx.tensors.a2p().analyze(dorelabel=1)
            bkup=copy.deepcopy(xx)
            for id in range(len(bkup.tensors.tensors)):
                ctensor=bkup.tensors.tensors[id]
                if len(ctensor.symbol)==1:
                    length=0
                    for qq in ctensor.indices.listindices:
                        for WW in qq.indices:
                            length+=1
                    length=length//2
                    ctensor.symbol+=str(length)
                ctensor.symbol=ctensor.symbol.split("_")[0]+"_"+str(id)
            bkup=bkup.updateconnindex()
            myfraction=bkup.tensors.estimatefraction(comp=1)
            # not important, yet

            min_order,minopr=xx.findthebestcontractionorder(nprint,memory=memory)
            keys=min_order.keys()
            keys.sort()
            #keys.reverse()
            ikey=keys[0]
            ordering=copy.deepcopy(min_order[ikey])
            if not len(ordering)==1:
                if not outflag: 
                    maxminopr=minopr
                    outflag=1
                if maxminopr<minopr: maxminopr=minopr

            xx=copy.deepcopy(xx.relabel(ordering))

            tmptensors=[] 
            for ii in range(len(ordering)):
                tmptensors.append(xx.tensors.tensors[ordering[ii]])
            tmptensors.reverse()

#           if len(ordering)==2:
#               tmptensors.sort()
#               tmptensors.reverse()
            if len(ordering)>1:
                aaa=[]
                aaa.append(tmptensors.pop())
                aaa.append(tmptensors.pop())
                aaa.sort()
                aaa.reverse()
                tmptensors=tmptensors+aaa
            
            xx.tensors=AnalyzedTensorSequence(tmptensors)

            mytarget=xx.tensors.showsummedindices().listindices

            pmytarget=[]
            for ii in mytarget:
                for jj in ii.indices:
                    pmytarget.append(jj)

            for ii in range(len(ordering)):
                ordering[len(ordering)-ii-1]=ii

            save=copy.deepcopy(xx)
                
            mxx=xx.tensors.a2p_abb()
            for pxx in mxx:
                pxx.abb=copy.deepcopy(pxx.symbol)
                pxx.symbol=pxx.symbol.split("_")[0]
            xx.tensors=mxx.analyze(dorelabel=0)
            xx.target.indices.listindices.sort()
            mxx=xx.tensors.a2p_abb()

#           if len(pmytarget)>0:
            mxx=mxx.relabelnum(pmytarget,sup=1)
            for pxx in mxx:
                pxx.abb=copy.deepcopy(pxx.symbol)
                pxx.symbol=pxx.symbol.split("_")[0]

            cnt=0
            for ppp in mxx.tensors:
                ppp.abb=ppp.abb.split("_")[0]+"_"+str(cnt)
                cnt+=1
                
            xx.tensors=mxx.analyze(dorelabel=0)
            xx.target.indices.listindices.sort()
            for pxx in xx.tensors.tensors:
                pxx.indices.listindices.sort() 
            xx.tensors.tensors.reverse()
            ordering.reverse()
            
            mysign=xx.tensors.estimatesign(withprojection=1)
            myfactor=Factor(mysign,myfraction)
            xx.factor=myfactor

            xx.sum=xx.tensors.showsumindices()
            xx.permutations=xx.tensors.estimatepermutation()
            xx.ordering=copy.deepcopy(ordering)

            flag=0
            for yy in usedtc:
                if xx.isequalto(yy):
                    flag=1
                    print "::::::::"
                    print xx
                    print yy
                    print "::::::::"
                    break
            if not flag:
                usedtc.append(copy.deepcopy(xx))

        print
        print "$$$$ Operation Cost $$$$  ",maxminopr
        print

        # find the reusable intermediates
        tex="" #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        count=0
        flag=1
        todolist=range(len(usedtc))
        while 1:
            if(not reusable): break
            if(not flag): break
            flag=0
            done=[]
            ntodolist=[]
            for ii in todolist:
                if ii in done: continue
                usednum=[]
                usednum.append(ii)
                flagii=0
                for jj in range(ii+1,len(usedtc)):
                    if jj in done: continue
                    if usedtc[ii].findreusable(usedtc[jj]):
                        usednum.append(jj)
                        flag=1
                        flagii=1
                        ntodolist.append(jj)
                if flagii: ntodolist.append(ii)
                for jj in usednum: done.append(jj)
                if len(usednum)>1:
                    qsymbol="K"+str(count)
                    print usednum,qsymbol,usedtc[ii]
                    #for jj in usednum: print  usedtc[jj]
                    tex+="$\\makebox[20pt][r]{$(\\Xi_{"+str(count)+"})"
                    for jj in usednum:
                        q0=copy.deepcopy(usedtc[jj].tensors.tensors[0])
                        q1=copy.deepcopy(usedtc[jj].tensors.tensors[1])
                        qlist=[]
                        qlist.append(q1)
                        qlist.append(q0)
                        qats=AnalyzedTensorSequence(qlist)
                        qindices=qats.showsummedindices()
                        qtensor=AnalyzedTensor(qsymbol,qindices)
                        qtensor.symmetry=qats.totalsymmetry()
                        qindices.permutable=qindices.getpermutable(\
                            q0.indices.permutable,\
                            q1.indices.permutable)
                        ll=usedtc[jj].tensors.tensors 
                        ll.reverse()
                        ll.pop()
                        ll.pop()
                        rest=copy.deepcopy(ll)
                        qfraction=Fraction()
                        qtensor.fraction*=q0.fraction
                        for kk in rest:
                            if q0.isequalto(kk,comp=1):
                                qtensor.fraction*=Fraction(1,2) 
                            if q1.isequalto(kk,comp=1):
                                qtensor.fraction*=Fraction(1,2)
                        ll.append(copy.deepcopy(qtensor))
                        ll.reverse()
                        usedtc[jj].ordering.pop()

                        #not a good code...
                        abb_backup=[]
                        usedtc[jj].tensors.tensors[0].abb=qsymbol+"_"+str(len(usedtc[jj].tensors.tensors)-1)
                        for ppp in usedtc[jj].tensors.tensors:
                            abb_backup.append(copy.deepcopy(ppp.abb))
                        mxx=usedtc[jj].tensors.a2p_abb()
                        for pxx in mxx:
                            pxx.abb=copy.deepcopy(pxx.symbol)
                            pxx.symbol=pxx.symbol.split("_")[0]
                        usedtc[jj].tensors=mxx.analyze(dorelabel=1)
                        for ppp in usedtc[jj].tensors.tensors:
                            ppp.abb=copy.deepcopy(abb_backup[0])
                            ppp.symbol=ppp.symbol.split("_")[0]
                            abb_backup.pop(0)

                    tex+=qtensor.indices.tex(bracket=1)+"$}="
                    qfraction=qats.estimatefraction()#*q0.fraction
                    qfactor=Factor(Sign(),qfraction)
                    qperm=qats.estimatepermutation()
                    tex+=qfactor.tex()
                    tmpperm=qperm.permutations
                    if len(tmpperm)>0:
                        for jj in tmpperm:
                            kk=copy.deepcopy(jj.extract())
                            tex+="P"+"_{"+str(len(kk.listindices))+"}"
                    tex+=q1.tex()
                    tex+=q0.tex()
                    tex+="$\\\\\n"
                    qsumm=qats.showsumindices()
                    qtensorc=TensorContraction(qtensor,qfactor,qperm,qsumm,qats)
                    
                    reusablelist.append(copy.deepcopy(qtensorc))
                    count+=1
            todolist=copy.deepcopy(ntodolist)
            todolist.sort()
#shio################################################
        nline=0
        for xx in usedtc:
            nline+=1
            tmp=xx.breakdowntooperationtree(xx.ordering,\
                copy.deepcopy(xx.factor),nline)
            myots.append(tmp)

        return ListOperationTree(myots,texheader=tex,filename=tmpfn,reusablelist=reusablelist) 

class ListOperationTree:
    def __init__(self,tree,symbol="",operator=[],pos="",texheader="",filename="",reusablelist=[]):
        self.tree=tree #<- [OperationTree,] 
        self.symbol=symbol
        self.operator=operator
        self.pos=pos
        self.texheader=texheader
        self.filename=filename
        self.code=Code() # for CodeListOperationTree
        self.reusablelist=reusablelist

    def __str__(self):
        return self.show()

    def show(self,indent=""):
        import copy

        space=" "*5
        list=copy.deepcopy(self.tree)
        listdict={}
        id=-1
        for xx in list:
            id+=1
            listdict[str(id).rjust(5)]=xx

        showdict={}
        id=-1
        while 1:
            id+=1
            id2=-1
            tmplistdict={}
            flag=0
            keys=listdict.keys()
            for key in keys:
                xx=listdict[key]
                showtmp=space*id+xx.show(" "*5)
                showdict[key]=showtmp[5:]
                if xx.children:
                    flag=1
                    for yy in xx.children:
                        id2+=1
                        tmplistdict[key+str(id2).rjust(5)]=yy
            listdict=copy.deepcopy(tmplistdict)
            if flag==0:
                break
        keys=showdict.keys()
        keys.sort()
        show=""
        for key in keys:
            show+=showdict[key] 
            show+="\n"
        
        return show

    def texpart(self,nret=2):
        import copy
        import string
        if self.tree:
            output="$\\makebox[20pt][r]{$"+self.symbol+self.tree[0].outindices.tex(bracket=1)+"$}="
        else:
            output="$\\makebox[20pt][r]{$"+self.symbol+self.operator[0].tensor.indices.tex(bracket=1)+"$}="
        count=0
        for ii in range(len(self.operator)):
            #output+=self.operator[ii].factor.sign.show() #### caution ####
            output+=self.operator[ii].factor.tex() #### caution #### shiozaki4
            output+=self.operator[ii].tensor.tex()
            count+=1
        for ii in range(len(self.tree)):
            if count%nret==0 and not count==0:
                output+="$\\\\\n$\\hspace{31pt}" 
            if len(self.tree[ii].operator)==1 and not self.tree[ii].children:
                output+=self.tree[ii].operator[0].factor.sign.show()
                if not self.tree[ii].operation.tensors.tensors[1].fraction==Fraction(): 
                    self.tree[ii].operation.factor.fraction*=\
                    self.tree[ii].operation.tensors.tensors[1].fraction
                output+=self.tree[ii].operation.factor.fraction.tex()
                tmpperm=self.tree[ii].operation.permutations.permutations
                if len(tmpperm)>0:
                    for jj in tmpperm:
                        kk=copy.deepcopy(jj.extract())
                        output+="P"+"_{"+str(len(kk.listindices))+"}"
                output+=self.tree[ii].operation.tensors.tensors[0].tex()
                output+=self.tree[ii].operation.tensors.tensors[1].tex()
            else:
                output+="+"
                output+=self.tree[ii].operation.factor.fraction.tex()
                tmpperm=self.tree[ii].operation.permutations.permutations
                if len(tmpperm)>0:
                    for jj in tmpperm:
                        kk=copy.deepcopy(jj.extract())
                        output+="P"+"_{"+str(len(kk.listindices))+"}"
                output+=self.tree[ii].operation.tensors.tensors[0].tex()\
                        +"(\\xi_{"+self.pos+str(ii)+"})"\
                        +self.tree[ii].operation.tensors.tensors[1].indices.tex(bracket=1)
            count+=1
        output+="$\\\\\n"
        return output

    def tex(self,filename):
        import copy
        import string
        outlist={}
        key=str(0)

        self.symbol="r"
        self.pos=""
        tmplist=[]
        self.operator=[]
        for ii in range(len(self.tree)):
            if len(self.tree[ii].operation.tensors.tensors)==1:
                tmpfactor=Factor(Sign(),Fraction())
                tmpop=LastOperator(copy.deepcopy(self.tree[ii].operation.tensors.tensors[0]),tmpfactor)
                self.operator.append(copy.deepcopy(tmpop))
                tmplist.append(ii)
        tmplist.reverse()
        for ii in tmplist:
            self.tree.pop(ii)
            
        toplist=self.texpart()

        nextgeneration=[]
        generation=[]
        generation.append(copy.deepcopy(self))
        while 1:
            for current in generation:
                for ii in range(len(current.tree)):
                    flag=0
                    if not current.tree[ii].children and len(current.tree[ii].operator)<2:
                        continue
                    listchild=[]
                    listop=[]
                    for xx in current.tree[ii].children:
                        listchild.append(copy.deepcopy(xx))
                    for xx in current.tree[ii].operator:
                        listop.append(copy.deepcopy(xx)) 
                    if not listchild and len(listop)<2:
                        flag=1 
                    mysymbol="(\\xi_{"+current.pos+str(ii)+"})"
                    mylot=ListOperationTree(listchild,mysymbol,listop,\
                                            copy.deepcopy(current.pos)+str(ii)+",")
                    outlist[mylot.pos]=mylot.texpart() 

                    if not flag:
                        nextgeneration.append(copy.deepcopy(mylot))
   
            generation=nextgeneration
            if not nextgeneration:
                break
            nextgeneration=[]
            

        keys=outlist.keys()
        keys.sort()
        keys.reverse()
        output=[]
        for ii in keys:
            output.append(outlist[ii])
        output.append(toplist)
        
        output2=""
        #output2 ="\\documentclass{revtex4}\n"
        #output2+="\\begin{document}\n"
        #output2+="\\begin{eqnarray*}\n"
        output2+=self.texheader
        #output2+="\\\\"
        output2+=string.join(output)
        output2=output2[:-3]
        output2+="\n"
        #output2+="\\end{eqnarray*}\n"
        #output2+="\\end{document}\n"
        outfile=open(filename,'w')
        outfile.write(output2) 
        outfile.close()
        
        return output2 
        

    def factorize(self):
        import copy
        tmpfn=copy.deepcopy(self.filename)
        id=1
        count=0
        output=self.factorizeeach(id,count)
        list=output.tree

        while 1:
            id+=1
            tmplist=[]
            flag=0
            for xx in list:

                if xx.children:
                    flag=1
                    lxxchild=ListOperationTree(xx.children)
                    lxxchild=lxxchild.factorizeeach(id,count)
                    xx.children=[]
                    for yy in lxxchild.tree:
                        xx.children.append(yy)
                        tmplist.append(yy)
            list=tmplist
            if flag==0:
                break
        print output
        newtree=output.tree #<- [OperationTree,] 
        newsymbol=output.symbol
        newoperator=output.operator
        newpos=output.pos
        newtexheader=output.texheader
        newreusablelist=self.reusablelist
        return CodeListOperationTree(newtree,symbol=newsymbol,\
                    operator=newoperator,texheader=newtexheader,filename=tmpfn,reusablelist=newreusablelist)

    def factorizeeach(self,id,count):
        import copy
        output=[]
        used=[]
        for ixx in range(len(self.tree)): 
            xx=self.tree[ixx]
            flag=0
            if ixx in used: continue
            if len(xx.operation.tensors.tensors)==1: 
                output.append(xx)
                continue
            used.append(ixx)
            myop=xx.operation.tensors.tensors[0]
            if not len(xx.operation.tensors.tensors)==1:
                myperm=xx.operation.tensors.tensors[1].indices.permutable
            list1=xx.outindices.listindices
            for iyy in range(len(self.tree)):
                yy=self.tree[iyy]
                if iyy in used:
                    continue
                yourop=yy.operation.tensors.tensors[0]
                if not len(yy.operation.tensors.tensors)==1:
                    yourperm=yy.operation.tensors.tensors[1].indices.permutable
                list2=yy.outindices.listindices
                #print myop.issameas(yourop,list1,list2),myop,yourop
                if myop.issameas(yourop,list1,list2,nonum=0):
                    used.append(iyy)
                    pp=ListAnalyzedIndices(copy.deepcopy(myperm)) 
                    qq=ListAnalyzedIndices(copy.deepcopy(yourperm))
                    myperm=pp.permutable_in_factorize(qq,xx)
                    for zz in yy.children:
                        #zz.permutable=copy.deepcopy(myperm)
                        xx.children.append(zz)
                        flag=1
                    for zz in yy.operator:
                        #zz.permutable=copy.deepcopy(myperm)
                        xx.operator.append(zz)
                        flag=1
            output.append(xx)
            if flag==1:
                xx.operation.tensors.tensors[1].symbol="I"+str(id)+"_"+str(count)
                xx.operation.tensors.tensors[1].indices.permutable=myperm
                #print xx.operation.tensors.tensors[1],ListAnalyzedIndices(myperm)
                for yy in xx.children:
                    yy.permutable=copy.deepcopy(myperm)
                for yy in xx.operator:
                    yy.permutable=copy.deepcopy(myperm)
                    #print yy, ListAnalyzedIndices(yy.permutable) 
                count+=1
        outputtree=ListOperationTree(output,texheader=self.texheader)
        return outputtree

class OperationTree:
    def __init__(self,operation,outindices,symbol,\
                 permutable=[],children=[],operator=[]): 
        self.operation=operation
        self.outindices=outindices
        self.permutable=permutable
        self.symbol=symbol
        self.children=children
        self.operator=operator

    def __str__(self):
        return self.show()

    def show(self,indent="",target=1,showchild=0):
        space=" "*5
        show=indent
        show+=self.showintermediate()
        show+=" = "
        show+=self.operation.show()
        if target:
            if (self.children and showchild) or self.operator:
                show+=space
                show+=" ( "
            if self.operator:
                for xx in self.operator: 
                    show+=xx.show()
                    show+=" + "
            if self.children and showchild:
                for xx in self.children:
                    show+=xx.showintermediate()
                    show+=" + "
            if (self.children and showchild) or self.operator:
                show=show[:-2]
                show+=" ) "
        return show

    def showintermediate(self):
        show=""
        show+=self.symbol
        show+=self.outindices.show(0)
        return show

    def isequalto(self,other):
        import copy
        tmpself=copy.deepcopy(self)
        tmpother=copy.deepcopy(other)

        if not len(self.children) == len(other.children):
            return 0
        
        tmpself.operation.tensors.tensors[0].indices\
            =tmpself.operation.tensors.tensors[0].indices.extract() 
        tmpother.operation.tensors.tensors[0].indices\
            =tmpother.operation.tensors.tensors[0].indices.extract() 
        list1=copy.deepcopy( tmpself.outindices.extract())
        list2=copy.deepcopy(tmpother.outindices.extract())
        if not tmpself.operation.tensors.tensors[0].\
               issameas(tmpother.operation.tensors.tensors[0],list1,list2):
            return 0

        tmpself.outindices=tmpself.outindices.extract()
        tmpother.outindices=tmpother.outindices.extract()
        list1=[]
        list2=[]
        if not tmpself.outindices.issameas(tmpother.outindices,list1,list2):
            #print tmpself.outindices,tmpother.outindices
            return 0
 
        if not len(self.operator) == len(other.operator):
            return 0
        
        if self.operator:
            list1=copy.deepcopy( tmpself.outindices.extract())
            list2=copy.deepcopy(tmpother.outindices.extract())
            tmpself.operator[0].tensor.indices\
                =tmpself.operator[0].tensor.indices.extract()
            tmpother.operator[0].tensor.indices\
                =tmpother.operator[0].tensor.indices.extract()
            if not tmpself.operator[0].issameas(tmpother.operator[0],\
                list1,list2): 
                return 0

        if not len(self.children)==0 and\
           not self.children[0].isequalto(other.children[0]):
           return 0

        return 1

class PrimitiveComputationalCost:
    def __init__(self,indextype,multiplier,factor,comp):
        #indextype  <- string
        #multiplier <- integer
        #factor     <- Fraction
        #comp       <- integer
        self.type  =indextype
        self.multi =multiplier
        self.factor=factor
        self.comp  =comp

    def isthesametype(self,other):
        if not other.type==self.type or\
           not other.comp==self.comp:
            return 0
        return 1
        
    def show(self,verbose=0):
        import string
        if self.type=="particle":
            show="p"
        elif self.type=="hole":
            show="h"
        elif self.type=="general":
            show="g"
        else:
            print "unknown type",self.type
            sys.exit()
        if self.comp:
            show=string.upper(show)

        if verbose:
            show+=" ^ "
        show+=str(self.multi)

        if verbose:
            show=self.factor.show()+"( "+show+" )"
        return show    

    def __mul__(self,other):
        import copy 
        if not isinstance(other,PrimitiveComputationalCost):
            return 0
        if not self.isthesametype(other):
            print "Wrong type",other.type,self.type
            return 0
        
        mymulti =self.multi +other.multi
        myfactor=self.factor*other.factor
        mytype  =copy.deepcopy(self.type)
        mycomp  =copy.deepcopy(self.comp)
        return PrimitiveComputationalCost(mytype,
                                          mymulti,
                                          myfactor,
                                          mycomp)

    def __floordiv__(self,other):
        import copy 
        if not isinstance(other,PrimitiveComputationalCost):
            return 0
        if not self.isthesametype(other):
            print "Wrong type",other.type,self.type
            return 0
        
        mymulti =self.multi -other.multi
        myfactor=self.factor//other.factor
        mytype  =copy.deepcopy(self.type)
        mycomp  =copy.deepcopy(self.comp)
        return PrimitiveComputationalCost(mytype,
                                          mymulti,
                                          myfactor,
                                          mycomp)
        
    def __cmp__(self,other):

        if self.isthesametype(other):
            return 0
        
        # G > P > g > p > h
        if self.comp > other.comp:
            return 1
        elif self.comp < other.comp:
            return -1

        if self.type =="general" or \
           other.type=="hole":
            return 1
        elif self.type =="hole" or \
             other.type=="general":
            return -1
                      
    
class ComputationalCost:
    def __init__(self,cost):
        #cost <- [PrimitiveComputationalCost,]
        self.cost=cost

    def __mul__(self,other):
        # other <- ComputationalCost
        #       -> ComputationalCost
        import copy

        mycost=copy.deepcopy(self.cost)
        
        for oo in other.cost:

            isin=0
            for ii in range(len(mycost)):
                ss=mycost[ii]
                if not ss.isthesametype(oo):
                    continue
                mycost[ii]=ss*oo
                isin=1
                break
            if not isin:
                mycost.append(oo)
        return ComputationalCost(mycost)        

    def __floordiv__(self,other):
        # other <- ComputationalCost
        #       -> ComputationalCost
        import copy

        mycost=copy.deepcopy(self.cost)
        
        for oo in other.cost:

            isin=0
            for ii in range(len(mycost)):
                ss=mycost[ii]
                if not ss.isthesametype(oo):
                    continue
                mycost[ii]=ss//oo
                isin=1
                break
            if not isin:
                print "warinig !!",oo, \
                      "is not in",self.show()
        return ComputationalCost(mycost)        
        
    def __str__(self):
        return self.show()
        
    def show(self,verbose=0):
        import copy
        show=''
        if(not self.cost):
            return show
        mycost=copy.deepcopy(self.cost)
        mycost.sort()
        mycost.reverse()
        for xx in mycost:
            show+=xx.show(verbose)
        return show    

    def roughcost(self):
        #-> integer
        out=1
        for xx in self.cost:
            if xx.comp:
                out*=888**xx.multi
            elif xx.type=="particle":
                out*=232**xx.multi
            elif xx.type=="hole":
                out*=28**xx.multi
            else:
                print "something was wrong in roughcost!!!!!"
        return out

    def __cmp__(self,other):
        import copy
        #print "self",self,self.roughcost()
        #print "other",other,other.roughcost()
        if self.roughcost() > other.roughcost():
            return 1
        elif self.roughcost() < other.roughcost():
            return -1

        slist =copy.deepcopy(self.cost)
        olist=copy.deepcopy(other.cost)

        slist.sort()
        slist.reverse()
        olist.sort()
        olist.reverse()

        inum=min(len(slist),len(olist))
        for ii in range(inum):
            if not slist[ii].isthesametype(olist[ii]):
                #print slist.__cmp__(olist)
                return slist[ii].__cmp__(olist[ii])
            if slist[ii].multi > olist[ii].multi:
                #print slist[ii].multi,olist[ii].multi
                return 1
            elif slist[ii].multi < olist[ii].multi:
                #print slist[ii].multi,olist[ii].multi
                return -1
        if not len(slist)==len(olist):
            print "Something is wrong"
        return 0    

class CodeIndices(AnalyzedIndices):
    def initval(self):
        mytype=self.showtype()
        if mytype=="hole":
            val="0L"
        elif mytype=="particle":
            if not self.showcomp():
                val="z->noab()"
            else:
                val="z->noab()+z->nvab()"
        elif mytpe=="general":
            val="0L" 
        else:
            print "something is wrong!!"
        return val

    def endval(self):
        mytype=self.showtype()
        if mytype=="hole":
            val="z->noab()"
        elif mytype=="particle":
            if not self.showcomp():
                val="z->noab()+z->nvab()"
            else:
                val="z->nab()"
        elif mytpe=="general":
            val="z->nab()"
        else:
            print "something is wrong!!"
        return val

    def valsize(self):
        mytype=self.showtype()
        if mytype=="hole":
            val="z->noab"
        elif mytype=="particle":
            if not self.showcomp(): 
                val="z->nvab()"
            else:
                val="z->ncab()"
        elif mytpe=="general":
            val="z->nab()"
        else:
            print "something is wrong!!"
        return val

    def showtileloop(self):
        import copy
        import string
        myindices=copy.deepcopy(self.indices)
        #myindices.reverse()
        prev=""
        out=""
        oldpointer=""
        for xx in myindices:
            if not prev:
                initval=self.initval()
            else:
                initval=prev
            endval=self.endval()
            variable=xx.show(showdagger=0,incode=1)+"b" 
            newpointer=ListStatements([])
            tloop=Loop(variable,initval,endval,newpointer)
            if out:
                oldpointer.append(tloop)
                #out.append(tloop)
            else:
                out=tloop
            oldpointer=newpointer    
            prev=variable
        return out,newpointer        
            

    def tileaddress(self,show="",suffix="",general=0):

        p_size  ="z->nvab()"
        q_size  ="z->ncab()"
        h_size  ="z->noab()"
        g_size  ="z->nab()"

        #ysize=self.size.showall()    
        mytype=self.showtype()

        gflag=0
        if general==1 or (general==2 and (not self.showdagger()))\
                      or (general==3 and self.showdagger()):
            gflag=1
            size="("+g_size+")"
        else:
            if mytype=="hole":          size=h_size
            elif mytype=="particle":
                if not self.showcomp(): size=p_size
                else:                   size=q_size

        basho=""
        if mytype=="particle" and (not gflag):
            if self.showcomp():
                basho="-"+h_size+"-"+p_size
            else:
                basho="-"+h_size
        #basho+="-1"

        for xx in self.indices:
            if show:
                show="+"+size+"*"+show
                
            myindex=xx.show(showdagger=0,incode=1)
            myindex+="b"+suffix
            show="("+myindex+basho+show+")"
        return show

    def reverse(self):
        import copy
        myindices=copy.deepcopy(self.indices)
        out=[]
        while myindices:
            out.append(myindices.pop())
        return CodeIndices(out,
                           copy.deepcopy(self.symbol) ,
                           copy.deepcopy(self.size)      )

    def multiplicationfactor(self):
        import copy
        # -> [([Comparison],integer)]
        me=copy.deepcopy(self)
        length=len(me)
        out=[]
        for ll in range(length,1,-1):
            equals=GenerateCombination(length,ll)
            for equal in equals:
                noneq=[]
                for ii in range(length):
                    if ii in equal:
                        continue
                    noneq.append(ii)
                #print equal,noneq    
        
                conditions=[]
                for ii in range(ll-1):
                    x1=me.indices[equal[ii  ]].show(showdagger=0,incode=1)+"b"
                    x2=me.indices[equal[ii+1]].show(showdagger=0,incode=1)+"b"
                    xx=Comparison(x1,x2,"==")
                    conditions.append(xx)
                    #print xx.show()
                for ii in range(length-ll):
                    x1=me.indices[equal[ 0]].show(showdagger=0,incode=1)+"b"
                    x2=me.indices[noneq[ii]].show(showdagger=0,incode=1)+"b"
                    xx=Comparison(x1,x2,"/=")
                    #print xx.show()
                    conditions.append(xx)
                #print cond.show()
                out.append( (conditions, factorial(ll) ) )
        return out        
        
class CodeListIndices(ListAnalyzedIndices):
    def restorecondition(self,nprint=0,rev=0):
        # -> [ ([Index,],Conditions),, ]
        import copy
        #myPLI=self.a2list()
        myPLI=self.a2p()
        #orgsign=myPLI.signbycanonicalization()
        #print orgsign
        ii=0
        irests=[]
        #if nprint: print self
        for xx in self.listindices:
            #if nprint: print xx,"xx"
            irestriction=[]
            for jj in range(len(xx)):
                irestriction.append(ii+jj)
            ii+=len(xx)    
            irests.append(irestriction)
        length=ii   
        if not length==len(myPLI):
            print "Something is wrong",length,len(myPLI)

        orders=GenPermutationwith(length,irests)
        out=[]
#       if len(orders)==1:
#           return out
        for order in orders:
            # Conditions
            tmpconditions=[]
            for ii in range(len(order)-1):
                tmpconditions.append([order[ii],order[ii+1]])
            conditions=[]
            for con in tmpconditions:
                approved=1
                for res in irests:
                    if Samearray(con,res):
                        approved=0
                        break
                    if Includearray(con,res):
                        approved=0
                        break
                if approved:
                    conditions.append(con)

            indexorder=[]
            for ii in order:
                indexorder.append(copy.deepcopy(myPLI[ii]))
            #newsign=PrimitiveIndices(indexorder).signbycanonicalization()    
            #print orgsign,newsign

            outconditions=[]
            for con in conditions:
                if rev==1:
                    opr=">="
                elif rev==2:
                    opr="<="
                else:
                    if con[0]<con[1]:
                        opr="<"
                    else:
                        opr="<="
                tCon=Comparison(myPLI[con[0]].show(showdagger=0,incode=1)+"b",
                                myPLI[con[1]].show(showdagger=0,incode=1)+"b",
                                opr)
                outconditions.append(tCon)

            if nprint:
                ishow=""
                for xx in indexorder:
                    ishow+=xx.show()
                    ishow+=" "
                print ishow,Conditions(outconditions,"and").show()

            #out.append((indexorder,Conditions(outconditions,"and")))
            out.append((PrimitiveIndices(indexorder),
                        Conditions(outconditions,"and")))

        return out         
                             
    def collectthesametype(self,select=0,targetpermutable=[]):
        import copy

        out=[]
        aa=copy.deepcopy(self.listindices)
        for xx in self.permutable:
            numlist=[]
            for yy in xx.indices:
                numlist.append(yy.num)

            ai=[]
            ailen=0
            for yy in aa:
                if yy.indices[0].num in numlist: 
                    if (not select) or (not len(numlist)==len(yy.indices)):
                        ai.append(copy.deepcopy(yy))
                    ailen+=len(yy.indices)

            if not len(xx.indices)==ailen: 
                print "collectthesametype"
                #sys.exit("collect the same type")
                    
            if ai:
                lai=ListAnalyzedIndices(ai)
                out.append(lai.a2c())

        if targetpermutable:
            for xx in out:
                usednum=[]
                er=[]
                for iy in range(len(xx.listindices)):
                    if iy in usednum: continue
                    usednum.append(iy)
                    yy=xx.listindices[iy]
                    ynum=yy.indices[0].num
                    for zz in targetpermutable:
                        numlist=[] 
                        for pp in zz.indices:
                            numlist.append(copy.deepcopy(pp.num))
                        if ynum in numlist:
                            break

                    for iz in range(iy+1,len(xx.listindices)):
                        zz=xx.listindices[iz]
                        flag=1
                        for pp in zz.indices:
                            if not pp.num in numlist:
                                flag=0
                                break 
                        if flag:
                            usednum.append(iz)
                            er.append(iz)
                            for pp in zz.indices:
                                yy.indices.append(pp)
                er.reverse()
                for pp in er: xx.listindices.pop(pp)
        return out    

    def tileaccess(self,
                   noconnection=0,
                   nosize=0,
                   rev=0,
                   nprint=0,
                   itarget=-1,
                   targetpermutable=[]):
        # -> [(PermutationTable,Condition)]
        import copy

        listtype=self.collectthesametype(targetpermutable=targetpermutable)

        out=[]
        for xx in listtype:
            cons=xx.restorecondition(nprint=0,rev=rev)

            if not out:
                out+=cons
                continue
            if not cons: continue
                
            tmparray=[]    
            for ii in range(len(out)):    
                for jj in range(len(cons)):
                    
                    tmp0=copy.deepcopy(out[ ii][0])\
                        +copy.deepcopy(cons[jj][0])
                    tmp1=copy.deepcopy(out[ ii][1])\
                        +copy.deepcopy(cons[jj][1])
    
                    tmparray.append((tmp0,tmp1))
            out=tmparray        

        porg=PrimitiveIndices([])
        for xx in listtype:
            porg+=xx.a2p()
            
        out1=[]
        for xx in out:
            xtmp=porg.generatepermutation(xx[0])
            out1.append( (xtmp,xx[1]) )
        return out1
        
    def tileaddress(self,show="",suffix="",general=0):
        myshow=show
        for xx in self.listindices:
            myshow=xx.tileaddress(show=myshow,suffix=suffix,general=general)
        return myshow    

    def showtilespinsymmetry(self,language="Cpp"):

        if not self.listindices:
            pointer=ListStatements([])
            code=ConditionalBranch(Conditions(),pointer)
            return code,pointer 

        porg=self.a2p()

        totalspin=len(porg)*2
        if language=="Cpp":
            condition1="!z->restricted()"
            condition2=""
            for xx in porg:
                condition2+="z->get_spin("
                condition2+=xx.show(showdagger=0,incode=1)
                condition2+="b"
                condition2+=")"
                condition2+="+"
            condition2=condition2[:-1]    
            condition2+="!="
            condition2+=str(totalspin)
            condition2+="L"
            #print condition1
            #print condition2
            condition=Conditions([condition1,condition2],"or")
        #print condition.show()    

        pointer=ListStatements([])
        code=ConditionalBranch(condition,pointer)
        return code,pointer
        
    def showtilespinsymmetry2(self,language="Cpp"):

        if not self.listindices:
            pointer=ListStatements([])
            code=ConditionalBranch(Conditions(),pointer)
            return code,pointer 

        dagg=self.listtermswith(dagger=1)
        nodagg=self.listtermswith(dagger=0)

        if language=="Cpp":
            val1=""
            for xx in dagg.a2p():
                val1+="z->get_spin("
                val1+=xx.show(showdagger=0,incode=1)
                val1+="b)+"
            val1=val1[:-1]    

            val2=""
            for xx in nodagg.a2p():
                val2+="z->get_spin("
                val2+=xx.show(showdagger=0,incode=1)
                val2+="b)+"
            val2=val2[:-1]    
        condition=Comparison(val1,val2,"==")

        pointer=ListStatements([])
        code=ConditionalBranch(condition,pointer)
        return code,pointer


    def totaltilesymmetry(self,language="Cpp"):
        porg=self.a2p()

        if language=="Cpp":
            condition=""
            for ii in range(len(porg)):
                if not ii==len(porg)-1:
                    condition+="(z->get_sym("
                    condition+=porg[ii].show(showdagger=0,incode=1)
                    condition+="b)^"
                else:
                    condition+="z->get_sym("
                    condition+=porg[ii].show(showdagger=0,incode=1)
                    condition+="b)"
            condition+=")"*(len(porg)-1)

        return condition

    def tilesize(self,language="Cpp"):
        porg=self.a2p()

        if language=="Cpp":
            size=""
            for xx in porg:
                size+="z->get_range("
                size+=xx.show(showdagger=0,incode=1)
                size+="b)*"
            size=size[:-1]
        return size    

    def showtileloop(self):
        import copy
        myindices=copy.deepcopy(self.listindices)
        out=""
        if not myindices:
            newpointer=ListStatements([])
            out=Loop("","","",statements=newpointer)
            return out,newpointer
        for xx in myindices:
            myloop,newpointer=xx.showtileloop()
            if not out:
                out=myloop
            else:
                pointer.append(myloop)
            pointer=newpointer    
        #if not out:
        #    out=Liststatements([])
        return out,pointer        

    def reverse(self):
        import copy
        mylistindices=copy.deepcopy(self.listindices)
        out=[]
        while mylistindices:
            xx=mylistindices.pop()
            out.append(xx.reverse())
        return CodeListIndices(out)    


    def showmultfactor(self,language="Cpp"):
        import copy
        code=ListStatements([])
        if language=="Cpp":
            tmp="double factor=1.0;"
            code.append(tmp)
        #print code.show()    
        for ii in range(len(self.listindices)):
            myindices=copy.deepcopy(self.listindices[ii])
            conditions=myindices.multiplicationfactor()
            for xx in conditions:
                cond=Conditions(xx[0],"and")
                tmppointer=ListStatements([])
                tmpcode=ConditionalBranch(cond,tmppointer)

                if language=="Cpp":
                    fact="factor=factor/"+str(xx[1])+".0;"

                
                tmppointer.append(fact)    

                #print tmpcode.show()
                code.append(tmpcode)
        return code    
            
        
class CodeTensor(AnalyzedTensor):
        # symbol  <- String
        # indices <- CodeListIndices
        # abb     <- String
        # symmetry<- [String,]

        
    def showtilesymmetry(self,language="Cpp"):
        import string
        val1=self.indices.totaltilesymmetry(language)
        if not self.indices.listindices: 
            val1="z->irrep_e()"

        if language=="Cpp":
            val2=""
            for ii in range(len(self.symmetry)):
                mysym=self.symmetry[ii][0]
                if   mysym=="X" or mysym=="V" or mysym=="Q" \
                  or mysym=="R" or mysym=="B" or mysym=="P":
                    mysym="e" 
                elif mysym=="S" or mysym=="s": mysym="x"
                elif mysym=="L" or mysym=="l": mysym="y"
                if not ii==len(self.symmetry)-1:
                    val2 += "(z->irrep_"
                    val2 += string.lower(mysym)+"()"
                    val2 += "^"
                else:
                    val2 += "z->irrep_"
                    val2 += string.lower(mysym)+"()"
            val2 += ")"*(len(self.symmetry)-1)

        condition=Comparison(val1,val2,"==")

        pointer=ListStatements([])
        code=ConditionalBranch(condition,pointer)
        return code,pointer
    
    def symindices(self):
        # -> [ String, ]
        import copy
        return copy.deepcopy(self.symmetry)

    
    def restore(self,
                ordering,
                language="Cpp",
                initial="",
                m_initial="",
                indexsuffix="",
                num=1,
                targetpermutable=[],
                onetensor=0):
        ## ordering <- PrimitiveIndices
        # ordering <- CodeListIndices
        import string
        import copy

        bconds=self.indices.tileaccess(noconnection=0,
                                       nosize=0,
                                       rev=0,
                                       nprint=0,
                                       itarget=-1,
                                       targetpermutable=targetpermutable
                                       )

        org_indices=self.indices.a2p()
        code=ListStatements([])

        mygeneral=0
        if   self.symbol.split("_")[0]=="f1" or self.symbol.split("_")[0]=="v2":
            mygeneral=1
        elif self.symbol.split("_")[0]=="Vd2" or self.symbol.split("_")[0]=="fy": #only subscripts are general
            mygeneral=2
        elif self.symbol.split("_")[0]=="Vr2" or self.symbol.split("_")[0]=="fx": #only superscripts are general
            mygeneral=3
        isitelse=0
        for bcon in bconds:
            restoretable=bcon[0]
            condition   =bcon[1]
            #print bcon[0],bcon[1]

            # read the tensor from disk
            
            tmppointer=ListStatements([])
            if condition.condition:
                tmpcode=ConditionalBranch(condition,tmppointer,isitelse=isitelse)
            else:
                tmpcode=tmppointer
            isitelse=1

            restoreindices=self.indices.permute(restoretable).a2c()
 
            if language=="Cpp":
                tmp_initial=string.lower(m_initial)
                if (tmp_initial[0]=="i" or tmp_initial[0]=="k"):
                    if (tmp_initial[1]=="1" and len(tmp_initial)>2 and tmp_initial[2]=="x"):
                        new_initial=tmp_initial[0:3]+"n["+tmp_initial[3:]+"]"
                    else:
                        new_initial=tmp_initial[0]+"n["+tmp_initial[1:]+"]"
                else:
                    new_initial=tmp_initial+"()"
                if (tmp_initial[0]=="i" and tmp_initial[1:]=="0"): new_initial="out"
                elif not (new_initial[0]=="i" or new_initial[0]=="k"): new_initial="z->"+new_initial
                filename   =new_initial
                memaddress ="k_"  +initial
                offsetname =memaddress+"_offset"
                dimension  ="dim" +initial
                tileaddress=restoreindices.tileaddress(suffix=indexsuffix,general=mygeneral)[1:]
                tileaddress=tileaddress[:-1]
                line=Statement(filename+"->get_block("+tileaddress+","+memaddress+");")
                tmppointer.append(line)
                

            restoreordering=restoreindices.a2p().indices
            tmpdict={}
            for ii in range(len(restoreordering)):
                isym=restoreordering[ii].show(showdagger=0)
                #tmpdict[isym]=str(ii+1)
                tmpdict[isym]=str(ii)
            sortorder=[]    
            targetordering=ordering.a2p().indices
            for ii in range(len(targetordering)):
                isym=targetordering[ii].show(showdagger=0)
                sortorder.append(tmpdict[isym])

            sortsign=Sign()
            restoreindices.permutable=self.indices.permutable
            listtype=restoreindices.collectthesametype(select=1)
            for xx in listtype:
                sortsign*=xx.a2p().signbycanonicalization()

            if language=="Cpp":
                line="z->sort_indices"
                line+=str(len(targetordering))
                line+="("+memaddress+","+memaddress+"_sort"
                for xx in restoreordering:
                    line+=","
                    line+="z->get_range("
                    line+=xx.show(showdagger=0,incode=1)
                    line+="b)"
                line+=","
                if (onetensor): sortorder.reverse()
                line+=string.join(sortorder,",")
                line+=","
                line+=sortsign.show()
                line+="1.0,false);"
                tmppointer.append(line)

            code.append(tmpcode)    

        return code        
    
    

    def showallocatesize(self,
                         language="Cpp",
                         initial="",
                         size=""):
        import copy

        if self.indices.listindices:
            if not size:
                size=self.indices.tilesize(language=language)
        else:
            size=str(1)

        if not initial:
            initial=copy.deepcopy(self.abb)

        tmp ="long dim"+initial
        tmp+="="
        tmp+=size+";"
        line=Statement(tmp)

        return line
        
    def showallocate(self,
                     language="Cpp",
                     name="None",
                     initial="",
                     index=0,
                     sort=1,
                     initialize=1):

        if not initial:
            initial=copy.deepcopy(self.symbol)

        out=ListStatements([])
        
        if language=="Cpp":
            tmp ="double* k_"+initial
            if sort:    tmp+="_sort="
            else:       tmp+="="
            tmp+="z->mem()->malloc_local_double(dim"+initial+");"

        out.append(tmp)

        if initialize:
            if language=="Cpp":
                tmp="std::fill(k_"+initial
                if sort: tmp+="_sort"
                tmp+=",k_"+initial
                if sort: tmp+="_sort"
                tmp+="+(size_t)dim"+initial+",0.0);"
            out.append(tmp)
        return out

    def showdeallocate(self,
                     language="Cpp",
                     name="None",
                     initial="",
                     index=0,
                     sort=1):

        if not initial:
            initial=copy.deepcopy(self.symbol)

        out=ListStatements([])
        
        if language=="Cpp":
            tmp ="z->mem()->free_local_double("
            tmp+="k_"+initial
            if sort:
                tmp+="_sort"
            tmp+=");"

        out.append(tmp)

        return out

    def showtcerestricted(self,language="Cpp",suffix=0):
        import string
        pI=self.indices.a2p()
        out=ListStatements([])

        oindices=[]
        for xx in pI:
            oindices.append(xx.show(showdagger=0,incode=1)+"b")

        tmp="long "
        rindices=[]
        for xx in pI:
            tmp+=xx.show(showdagger=0,incode=1)+"b_"+str(suffix)+","
            rindices.append(xx.show(showdagger=0,incode=1)+"b_"+str(suffix))
        tmp=tmp[:-1]+";"
        out.append(tmp)
            
        if language=="Cpp":
            tmp ="z->restricted_"
            tmp+=str(len(pI))
            tmp+="("
            tmp+=string.join(oindices,",")
            tmp+=","
            tmp+=string.join(rindices,",")
            tmp+=");"
            
        out.append(tmp)
        return out

    def offset(self,language="Cpp",initial="a",name="test"):
        import copy
        import string
        code=ListStatements([])

        loopindices=copy.deepcopy(ListAnalyzedIndices(self.indices.permutable).a2c())

        currentpointer=code

        if language=="Cpp":
            tmp_initial=string.lower(initial)
            if (tmp_initial[0]=="i" or tmp_initial[0]=="k"):
                if (tmp_initial[1]=="1" and len(tmp_initial)>2 and tmp_initial[2]=="x"):
                    new_initial=tmp_initial[0:3]+"n["+tmp_initial[3:]+"]"
                else:
                    new_initial=tmp_initial[0]+"n["+tmp_initial[1:]+"]"
            else:
                new_initial=tmp_initial+"()"
            if (tmp_initial[0]=="i" and tmp_initial[1:]=="0"): new_initial="out"
            elif not (new_initial[0]=="i" or new_initial[0]=="k"): new_initial="z->"+new_initial
            filename=new_initial
            k_offset="k_"+initial+"_offset"
            l_offset="l_"+initial+"_offset"

            currentpointer.append("long size=0L;")
        
        tmpcode,tmppointer=loopindices.showtileloop()
        currentpointer.append(tmpcode)
        currentpointer=tmppointer

        tmpcode, tmppointer=loopindices.showtilespinsymmetry2(language)
        currentpointer.append(tmpcode)
        currentpointer=tmppointer

        tmpcode,tmppointer=self.showtilesymmetry(language)
        currentpointer.append(tmpcode)
        currentpointer=tmppointer

        tmpcode, tmppointer=loopindices.showtilespinsymmetry(language)
        currentpointer.append(tmpcode)
        currentpointer=tmppointer
        
        if language=="Cpp":

            tmpline =filename+"->input_offset("
            tmpline+=loopindices.tileaddress()[1:-1]+",size);"
            currentpointer.append(tmpline)

            #tmpline =filename+"->offsets->offset[i]=size;"
            #currentpointer.append(tmpline)
        
            tmpline ="size+="
            tmpline+=loopindices.tilesize(language)+";"
            currentpointer.append(tmpline)

            #currentpointer.append("++i;")

        return code

        
class CodeTensorSequence(AnalyzedTensorSequence):
    def showtilespinsymmetry(self,language="Cpp"):
        outcode=ListStatements([])
        pointer=outcode
        for xx in self.tensors:
            tmpcode,tmppointer=xx.indices.showtilespinsymmetry(language)
            pointer.append(tmpcode)
            pointer=tmppointer
        return outcode,pointer    

    def showtilespinsymmetry2(self,language="Cpp",onlyone=0):
        outcode=ListStatements([])
        pointer=outcode
        if not onlyone:
            for xx in self.tensors:
                tmpcode,tmppointer=xx.indices.showtilespinsymmetry2(language)
                pointer.append(tmpcode)
                pointer=tmppointer
        else:
            tmpcode,tmppointer=self.tensors[0].indices.showtilespinsymmetry2(language)
            pointer.append(tmpcode)
            pointer=tmppointer
        return outcode,pointer    

    def showtcerestricted(self,language="Cpp"):
        outcode=ListStatements([])
        for ii in range(len(self.tensors)):
            tmp=self.tensors[ii].showtcerestricted(language=language,
                                                   suffix=ii)
            outcode.append(tmp)
        return outcode    

    def showallocatesize(self,
                         language="Cpp",
                         initial="",onetensor=0):
        
        outcode=ListStatements([])
        #intlist=[]

        sumindices=self.listindices().showsumindices()
        tmp  ="long dim_common="
        #intlist.append("dim_common")

        if not onetensor:
            tmp+=sumindices.a2c().tilesize(language=language)+";"
        else:
            tmp+="1L;"
        if tmp=="long dim_common=;": tmp="long dim_common=1L;"
        outcode.append(tmp)
        dimlist=[]

        for ii in range(len(self.tensors)):
            if initial:
                myini=initial+str(ii)
            else:
                myini=""
                
            #sort
            sortini=myini+"_sort"
            tmp=self.tensors[ii].indices.unsummedindices(sumindices)
            sortsize=tmp.a2c().tilesize(language=language)
            if not sortsize: sortsize="1L"

            line=self.tensors[ii].showallocatesize(language= language,
                                                   initial = sortini,
                                                   size    = sortsize)
            outcode.append(line)

            #tensor
            tini  = myini
            tsize = "dim_common*"
            tsize+= "dim"+sortini
            line=self.tensors[ii].showallocatesize(language= language,
                                                   initial = tini,
                                                   size    = tsize)
            outcode.append(line)

            tmpcond=Comparison("dim"+tini,"0L",">")
            #tmpcond=Comparison("dim"+tini,"0",">=")
            dimlist.append(tmpcond)

            #intlist+=["dim"+myini,"dim"+myini+"_sort"]
            
        pointer=ListStatements([])    
        cond=Conditions(dimlist,"and")
        outcode.append(ConditionalBranch(cond,pointer))

        return outcode,pointer
        
    def restore(self,
                language="Cpp",
                name="test",
                index=0,
                initial="",initial2="",targetpermutable=[]):
        import copy
        pinitial="a"
        outcode=ListStatements([])
        sumindices=self.listindices().showsumindices()
        psumindices=sumindices.a2p()
        myerrorindex=index

        if(len(self.tensors)==1): onetensor=1
        else: onetensor=0 

        for ii in range(len(self.tensors)):
            if pinitial:
                myini=pinitial+str(ii)
            else:
                myini=copy.deepcopy(self.tensors[ii].abb)
                
            myerrorindex+=1    
            tmpcode=self.tensors[ii].showallocate(language=language,
                                                  name=name,
                                                  index=myerrorindex,
                                                  initial=myini,
                                                  sort=1,
                                                  initialize=0)     
            outcode.append(tmpcode)

            myerrorindex+=1    
            tmpcode=self.tensors[ii].showallocate(language=language,
                                                  name=name,
                                                  index=myerrorindex,
                                                  initial=myini,
                                                  sort=0,
                                                  initialize=0)     
            outcode.append(tmpcode)
                
            out1,out2=self.tensors[ii].indices.classifysumindices(sumindices)
            tsum=[]
            for xx in sumindices.listindices:
                for yy in out1.listindices:
                    if xx.isequalto(yy,itarget=0,nodagger=1,nonum=0,nocon=1):
                        tsum.append(yy)
            #target=PrimitiveIndices(tsum)+out2.a2p()
            target=CodeListIndices(tsum)+out2.a2c()
                    

            #target.indices.reverse()
            #target.a2c().reverse()
            target=target.a2c().reverse()
            target.permutable=self.tensors[ii].indices.permutable
            
            if ii==0:
                m_myini=initial
            else:
                m_myini=initial2
            tmpcode=self.tensors[ii].restore(target,
                                             language=language,
                                             initial=myini,
                                             m_initial=m_myini,
                                             indexsuffix="_"+str(ii),
                                             num=ii,
                                             targetpermutable=targetpermutable,
                                             onetensor=onetensor)
            
            outcode.append(tmpcode)

            myerrorindex+=1    
            tmpcode=self.tensors[ii].showdeallocate(language=language,
                                                    name=name,
                                                    initial=myini,
                                                    index=myerrorindex,
                                                    sort=0)
            outcode.append(tmpcode)

        return outcode    

    def store(self,
              factor=Factor(),
              language="Cpp",
              initial="",
              indexsuffix="",
              targetpermutable=[],onetensor=0,input="",
              lsign=Sign(),lfraction=Fraction(),
              reusable=0,targetblock=0):
        import copy
        import string

        m_initial=initial
        initial="c"
        
        sumindices=self.listindices().showsumindices()
        code=ListStatements([])

        if not onetensor:
            for ii in range(len(self)):
                out1,out2=self.tensors[ii].indices.classifysumindices(sumindices)
                #if not ii:
                if not ii:
                    #outer=out2.a2c()
                    tmp=out2.a2c().reverse()
                    tmp.listindices.reverse()
                    outer=tmp
                else:
                    tmp=out2.a2c().reverse()
                    tmp.listindices.reverse()
                    outer+=tmp
                    #outer+=out2.a2c()
            if self.tensors[1].symbol[0]=='K':
                if not reusable:
                    factor.fraction*=self.tensors[1].fraction 
        else:
            out1,out2=self.tensors[0].indices.classifysumindices(sumindices)
            outer=out2.a2c().reverse()
            outer.listindices.reverse()

            factor.fraction=self.tensors[0].fraction
    
        outer.listindices.reverse()
        outer.permutable=copy.deepcopy(targetpermutable)
        outer=outer.a2c()

        #print outer
        #print ListAnalyzedIndices(outer.permutable),"s"


        for ii in range(len(outer)):
            outer[ii].size=Indexrange(outer[ii].showtype(),
                                      outer[ii].size.comp)
        #print outer.show()   
        mypermutable=self.tensors[0].indices.permutable
        if not onetensor:
            mypermutable+=self.tensors[1].indices.permutable
            mypermutable=ListAnalyzedIndices(mypermutable).removeinternal().listindices
    
        if outer.listindices:
            bconds=outer.tileaccess(noconnection=0,
                                    nosize=1,
                                    rev=1,      
                                    nprint=0,
                                    itarget=1,
                                    targetpermutable=mypermutable)
            for bcon in bconds:
                storetable = bcon[0]
                condition  = bcon[1]
                #print bcon[0],bcon[1]
    
                #print condition.show()
                tmppointer=ListStatements([])
                if condition.condition:
                    tmpcode=ConditionalBranch(condition,tmppointer)
                else:
                    tmpcode=tmppointer
                target=ListAnalyzedIndices(outer.permutable).permute(storetable).a2c()
                #print target.show()
    
                outerordering=outer.a2p().indices
                tmpdict={}
                for ii in range(len(outerordering)):
                    isym=outerordering[ii].show(showdagger=0)
                    #tmpdict[isym]=str(ii+1)
                    tmpdict[isym]=str(ii)
                sortorder=[]
                targetordering=target.a2p().indices
                for ii in range(len(targetordering)):
                    isym=targetordering[ii].show(showdagger=0)
                    sortorder.append(tmpdict[isym])
    
   #            print factor.fraction,lfraction
                storefactor = factor.fraction*lfraction
                reducefactor= self.estimatefraction(norule7=1)
                
                storesign=Sign()
                target.permutable=copy.deepcopy(outer.permutable)
                listtype=target.collectthesametype(select=0)
                for xx in listtype:
                    storesign*=xx.a2p().signbycanonicalization()
                storesign*=lsign
    
                #print sortorder,sortsign
                if language=="Cpp":
                    tmp_initial=string.lower(m_initial)
                    if (tmp_initial[0]=="i" or tmp_initial[0]=="k"):
                        if (tmp_initial[1]=="1" and len(tmp_initial)>2 and tmp_initial[2]=="x"):
                            new_initial=tmp_initial[0:3]+"n["+tmp_initial[3:]+"]"
                        else:
                            new_initial=tmp_initial[0]+"n["+tmp_initial[1:]+"]"
                    else:
                        new_initial=tmp_initial+"()"
                    if (tmp_initial[0]=="i" and tmp_initial[1:]=="0"): new_initial="out"
                    elif not (new_initial[0]=="i" or new_initial[0]=="k"): new_initial="z->"+new_initial
                    filename   =new_initial
                    memaddress ="k_"  +initial
                    offsetname =memaddress+"_offset"
                    dimension  ="dim" +initial
    
                    if not targetblock:
                        line="z->sort_indices"
                    else:
                        line="z->sort_indices_acc"
                    line+=str(len(outerordering))
                    line+="("
                    if not onetensor:
                        tmplines=[memaddress+"_sort",memaddress]
                    else:
                        memaddress2="k_"+input+str(0)
                        tmplines=[memaddress2+"_sort",memaddress]
                    if targetblock:
                        tmplines.pop()
                        tmplines.append("a_i0")
                    line+=string.join(tmplines,",")
                        
                    if (onetensor): outerordering.reverse()
                    for xx in outerordering:
                        line+=","
                        line+="z->get_range("
                        line+=xx.show(showdagger=0,incode=1)
                        line+="b)"
                    line+=","
                    if (onetensor): sortorder.reverse()
                    line+=string.join(sortorder,",")
                    line+=","
                    line+=storesign.show()
                    line+=storefactor.showCpp()
                    if not (reducefactor.denominator==1 and\
                        reducefactor.numerator==1):
                        line+="/"+reducefactor.showCpp()
                    if not targetblock:
                        line+=",false);"
                    else:
                        line+=");"
                    tmppointer.append(line)
    
                    if not targetblock:
                        tileaddress=target.tileaddress(suffix=indexsuffix)[1:]
                        tileaddress=tileaddress[:-1]
                        line=filename+"->add_block("
                        line+=tileaddress+","+memaddress+");"
                        tmppointer.append(line)
    
                code.append(tmpcode)
        else:
            tmpcode=ListStatements([])
            if language=="Cpp":
                tmp_initial=string.lower(m_initial)
                if (tmp_initial[0]=="i" or tmp_initial[0]=="k"):
                    if (tmp_initial[1]=="1" and len(tmp_initial)>2 and tmp_initial[2]=="x"):
                        new_initial=tmp_initial[0:3]+"n["+tmp_initial[3:]+"]"
                    else:
                        new_initial=tmp_initial[0]+"n["+tmp_initial[1:]+"]"
                else:
                    new_initial=tmp_initial+"()"
                if (tmp_initial[0]=="i" and tmp_initial[1:]=="0"): new_initial="out"
                elif not (new_initial[0]=="i" or new_initial[0]=="k"): new_initial="z->"+new_initial
                filename   =new_initial 
                memaddress ="k_"  +initial
                offsetname =memaddress+"_offset"
                dimension  ="dim" +initial

                line="z->sort_indices0"
                line+="("+memaddress+"_sort,"+memaddress+",1.0,false);"
                tmpcode.append(line)

                tileaddress="("+str(0)+")"
                line=filename+"->add_block("
                line+=tileaddress+","+memaddress
                line+=");"
                tmpcode.append(line)

            code.append(tmpcode)
        return code
    
    
class CodeTensorContraction(TensorContraction):

        
    def matrixmultiplication(self,language="Cpp",
                             outinitial="c",
                             initial="a"):
        listindices=self.tensors.listindices()
        sumindices=listindices.showsumindices()
        
        #factor from rule6
        code=sumindices.a2c().showmultfactor(language=language)
#shio
        #print code.show()

        #code=listindices.showsummedindices().a2c().showmultfactor(language=language)
        #print code.show()

        if len(self.tensors)>2:
            print "Sorry now we can treat only binary contraction"

        if language=="Cpp":
            tmp ="z->smith_dgemm("
            tmp+="dim"+initial+str(0)+"_sort"
            tmp+=","
            tmp+="dim"+initial+str(1)+"_sort"
            tmp+=",dim_common,factor,"
            tmp+="k_"+initial+str(0)+"_sort"
            tmp+=",dim_common,"
            tmp+="k_"+initial+str(1)+"_sort"
            tmp+=",dim_common,1.0,"
            tmp+="k_"+outinitial+"_sort"
            tmp+=","
            tmp+="dim"+initial+str(0)+"_sort);"
            code.append(tmp)
        return code    

    def translatetocode(self,
                        language="Cpp",
                        name="test",
                        inputinitial="a",
                        inputinitial2="b",
                        outputinitial="c",
                        initialize=1,
                        onetensor=0,
                        targetpermutable=[],
                        lsign=Sign(),
                        lfraction=Fraction(),
                        reusable=0,targetblock=0):
        import string
        import copy
        errorindex=0
        myname=name
        
        code=ListStatements([]) #returns a pointer
        tmpcode=ListStatements([])
        
        if targetblock:
            tmplistdagger=self.tensors.listindices().listtermswith(dagger=1).listindices
            tmplist      =self.tensors.listindices().listtermswith(dagger=0).listindices
            dellist      =[]
            dellistdagger=[]
            ix=-1
            for xx in tmplist:
                ix+=1
                iy=-1
                for yy in tmplistdagger:
                    iy+=1
                    if xx.isequalto(yy,nodagger=1,nonum=0,nocon=1):
                        dellist.append(ix)
                        dellistdagger.append(iy)
            dellist.sort()
            dellist.reverse()
            dellistdagger.sort()
            dellistdagger.reverse()
            for xx in dellist:          tmplist.pop(xx)
            for xx in dellistdagger:    tmplistdagger.pop(xx)
            tmplist.sort()
            tmplistdagger.sort()

            ii =0
            irests=[]
            for xx in tmplist:
                irestriction=[]
                for jj in range(len(xx)):
                    irestriction.append(ii+jj)
                ii+=len(xx)
                irests.append(irestriction)
            length=ii   
            orders=GenPermutationwith(length,irests)

            ii =0
            irests=[]
            for xx in tmplistdagger:
                irestriction=[]
                for jj in range(len(xx)):
                    irestriction.append(ii+jj)
                ii+=len(xx)
                irests.append(irestriction)
            length=ii   
            ordersdagger=GenPermutationwith(length,irests)
            
            orderings=[]
            for xx in ordersdagger:
                for yy in orders:
                    newordering=copy.deepcopy(xx+yy)
                    for ix in range(len(xx)):
                        newordering[len(xx)+ix]+=len(xx)#+1
                        #newordering[ix]+=1
                    inverse=[]
                    neworderinginverse=[]
                    for zz in range(len(newordering)):
                        inverse.append(zz+1)
                        neworderinginverse.append(0)
                    ix=0
                    for zz in newordering:
                        ix+=1
                        neworderinginverse[zz]=ix
                        
                    orderings.append(neworderinginverse)


            tmp="const long perm["+str(len(orderings))+"]["+str(len(orderings[0]))+"]={"
            for xx in orderings:
                for ii in xx:
                    tmp+=str(ii-1)+"," 
                tmp=tmp[:-1]
                tmp+=", "
            tmp=tmp[:-2]+"};"
            tmpcode.append(tmp)

            tmp="const long t_b["+str(len(orderings[0]))+"]={"
            ix=0
            for xx in self.target.indices.listindices:
                for yy in xx.indices:
                    tmp+="t_"+copy.deepcopy(yy.show(showdagger=0,incode=1))+"b,"
                    ix+=1
            tmp=tmp[:-1]+"};"
            tmpcode.append(tmp) 
            code.append(tmpcode)
            tmpcode=ListStatements([])

            tmppointer=ListStatements([])
            tmploop=Loop("permutation","0L",str(len(orderings))+"L",tmppointer)
            code.append(tmploop)

            ix=0
            for xx in self.target.indices.listindices:
                for yy in xx.indices:
                    tmpcode.append("const long "+yy.show(showdagger=0,incode=1)+"b="+\
                    "t_b[perm[permutation]["+str(ix)+"]];")
                    ix+=1

            tmpcode.append("bool skip=false;")
            tmppointer.append(tmpcode)

            tmppointer2=ListStatements([])
            tmploop=Loop("p_p","0L","permutation",tmppointer2)
            tmp="if("
            ix=0
            for xx in self.target.indices.listindices:
                for yy in xx.indices:
                    if not ix==0: 
                        tmppointer2.append(tmp)
                        tmp=" &&  "
                    tmp+=yy.show(showdagger=0,incode=1)+"b=="+"t_b[perm[p_p]["+str(ix)+"]]"
                    ix+=1
            tmp+=") skip=true;"
            tmppointer2.append(tmp)
            tmppointer.append(tmploop)

            tmpcode=ListStatements([])
            tmpcode.append("if (skip) continue;")
            tmppointer.append(tmpcode)

####

        if not onetensor:
            tmp=copy.deepcopy(self.tensors.tensors[0].indices.permutable)+\
                copy.deepcopy(self.tensors.tensors[1].indices.permutable)
            loopindices=ListAnalyzedIndices(tmp)
            loopindices=loopindices.removeinternal()
            loopindices=loopindices.extractifnecesarry(copy.deepcopy(targetpermutable))
        else:
            tmp=copy.deepcopy(self.tensors.tensors[0].indices.permutable)
            loopindices=ListAnalyzedIndices(tmp)


        loopindices=loopindices.a2c()


        if not targetblock: 
            tmpcode, tmppointer=loopindices.showtileloop()
            code.append(tmpcode)
            currentpointer=tmppointer
        else:
            #tmpcode, tmppointer=ListAnalyzedIndices([]).a2c().showtileloop()
            #code.append(tmpcode)
            currentpointer=tmppointer
        
        # parallel loop
        if language=="Cpp":
            if not targetblock:

                currentpointer.append("long tileoffset;")
                loopindices.permutable=copy.deepcopy(targetpermutable)
                bconds=loopindices.tileaccess(noconnection=1,nosize=1,rev=0,itarget=1,targetpermutable=[])
                targetoffset_=""
                isitelse=0
                for bcond in bconds:
                    tmppointer=ListStatements([])
                    if bcond[1].condition:
                        tmpcode=ConditionalBranch(bcond[1],tmppointer,isitelse=isitelse)
                    else:
                        tmpcode=tmppointer
                    targetoffset_=ListAnalyzedIndices(targetpermutable).permute(bcond[0]).a2c().tileaddress()
                    tmppointer.append("tileoffset="+targetoffset_+";")
                    
                    currentpointer.append(tmpcode)
                    isitelse=1
#workspace

                tmppointer=ListStatements([])
                tmp_initial=string.lower(outputinitial)
                if (tmp_initial[0]=="i" or tmp_initial[0]=="k"):
                    if (tmp_initial[1]=="1" and len(tmp_initial)>2 and tmp_initial[2]=="x"):
                        new_initial=tmp_initial[0:3]+"n["+tmp_initial[3:]+"]"
                    else:
                        new_initial=tmp_initial[0]+"n["+tmp_initial[1:]+"]"
                else:
                    new_initial=tmp_initial+"()"
                if (tmp_initial[0]=="i" and tmp_initial[1:]=="0"): new_initial="out"
                elif not (new_initial[0]=="i" or new_initial[0]=="k"): new_initial="z->"+new_initial
                #tmptileaddress=self.target.indices.tileaddress()
                #tmptileaddress=ListAnalyzedIndices(targetpermutable).a2c().tileaddress()
                if targetoffset_=="": targetoffset_st="(0L)"
                else:                 targetoffset_st="(tileoffset)" 
                condition=Conditions([new_initial+"->is_this_local"+targetoffset_st]) 
                tmpcode=ConditionalBranch(condition,tmppointer)

            else:
                tmppointer=ListStatements([])
                tmpcode=ConditionalBranch(Conditions(),tmppointer)
            #tmpcode=ConditionalBranch(Conditions(),tmppointer)
            currentpointer.append(tmpcode)


            #if not targetblock:
            #    tmp="++count;"
            #    currentpointer.append(tmp)
            currentpointer=tmppointer
            
        # spin symmetry
        tmpcode, tmppointer=loopindices.showtilespinsymmetry(language)
        currentpointer.append(tmpcode)
        #currentpointer=tmppointer

        #tmp="next=z->next_value();"
        #currentpointer.append(tmp)
        currentpointer=tmppointer
        
        tmpcode, tmppointer=loopindices.showtilespinsymmetry2(language)
        currentpointer.append(tmpcode)
        currentpointer=tmppointer

        # spacial symmetry of output intermediate
        tmpcode,tmppointer=self.target.showtilesymmetry(language)
        currentpointer.append(tmpcode)
        currentpointer=tmppointer
        
        # allocate output intermediate
        tmpcode=self.target.showallocatesize(language=language,
                                             initial="c")
                                             #initial=outputinitial)
        currentpointer.append(tmpcode)
        currentpointer=tmppointer

        if not onetensor:
            #tmpcode=self.target.showallocate(initial=outputinitial,
            tmpcode=self.target.showallocate(initial="c",
                                             name=myname,
                                             index=errorindex,
                                             sort=1,
                                             initialize=initialize)
            errorindex+=1
            currentpointer.append(tmpcode)

        outerpointer=currentpointer

        #summation loop
        if not onetensor:
            tmpcode,tmppointer=self.sum.a2c().showtileloop()
            currentpointer.append(tmpcode)
            currentpointer=tmppointer

        # spin symmetry
            tmpcode,tmppointer=self.tensors.showtilespinsymmetry2(language,onlyone=1)
            currentpointer.append(tmpcode)
            currentpointer=tmppointer

        # spacial symmetry of output intermediate
            tmpcode,tmppointer=self.tensors.tensors[0].showtilesymmetry(language)
            currentpointer.append(tmpcode)
            currentpointer=tmppointer
        
        # restriction
        tmpcode=self.tensors.showtcerestricted(language)
        currentpointer.append(tmpcode)
        
        # allocate tensorcontraction
        tmpcode,tmppointer=self.tensors.showallocatesize(language=language,
                                                         initial="a",
                                                         #initial=inputinitial,
                                                         onetensor=onetensor)
        currentpointer.append(tmpcode)
        currentpointer=tmppointer
        
        # restore tensors
        tmpcode = self.tensors.restore(initial=inputinitial,
                                       initial2=inputinitial2,
                                       language=language,
                                       index=errorindex,
                                       name=myname,targetpermutable=targetpermutable)
        currentpointer.append(tmpcode)
        errorindex+=3*len(self.tensors)

        if not onetensor:
            tmpcode = self.matrixmultiplication(language=language,
                                                outinitial="c",
                                                initial="a")
                                                #outinitial=outputinitial,
                                                #initial=inputinitial)
            currentpointer.append(tmpcode)
        
            for ii in range(len(self.tensors)-1,-1,-1):
                tmpcode=self.target.showdeallocate(language=language,
                                                   name=myname,
                                                   initial="a"+str(ii),
                                                   #initial=inputinitial+str(ii),
                                                   index=errorindex,
                                                   sort=1)
                currentpointer.append(tmpcode)
                errorindex+=1
            
            currentpointer=outerpointer

            if not targetblock:
                tmpcode=self.target.showallocate(language=language,
                                                 name=myname,
                                                 index=errorindex,
                                                 initial="c",
                                                 #initial=outputinitial,
                                                 sort=0,
                                                 initialize=0)
                errorindex+=1
                currentpointer.append(tmpcode)

        else:
            #tmpcode=self.target.showallocate(initial=outputinitial,
            tmpcode=self.target.showallocate(initial="c",
                                             name=myname,
                                             index=errorindex,
                                             sort=0,
                                             initialize=0)
            errorindex+=1
            currentpointer.append(tmpcode)
        
        myfraction=Fraction()
        tmpcode = self.tensors.store(factor=self.factor,
                                     initial=outputinitial,
                                     targetpermutable=targetpermutable,
                                     onetensor=onetensor,
                                     input="a",
                                     #input=inputinitial,
                                     lsign=lsign,
                                     lfraction=Fraction(),
                                     reusable=reusable,
                                     targetblock=targetblock)
        currentpointer.append(tmpcode)
        
        if not onetensor:
            if not targetblock:
                tmpcode=self.target.showdeallocate(language=language,
                                                   name=myname,
                                                   initial="c",
                                                   #initial=outputinitial,
                                                   index=errorindex,
                                                   sort=0)
                errorindex+=1
                currentpointer.append(tmpcode)

            tmpcode=self.target.showdeallocate(initial="c",
            #tmpcode=self.target.showdeallocate(initial=outputinitial,
                                               name=myname,
                                               index=errorindex,
                                               sort=1)
            errorindex+=1
            currentpointer.append(tmpcode)
        else:
            tmpcode=self.target.showdeallocate(language=language,
                                               name=myname,
                                               initial="c",
                                               #initial=outputinitial,
                                               index=errorindex,
                                               sort=0)
            errorindex+=1
            currentpointer.append(tmpcode)
            tmpcode=self.target.showdeallocate(initial="a"+str(0),
            #tmpcode=self.target.showdeallocate(initial=inputinitial+str(0),
                                               name=myname,
                                               index=errorindex,
                                               sort=1)
            errorindex+=1
            currentpointer.append(tmpcode)

        #parallel
        if not targetblock:
            tmpcode=ListStatements([])
            tmpcode.append("z->mem()->sync();")
            code.append(tmpcode)
        else:
            tmpcode=ListStatements([])
            #tmpcode.append("}") # enddo of permutation
            #code.append(tmpcode)
        
        #print code.show()
        return code


    def codeheader(self, language="Cpp", name="test", inputinitial="a",
                   outputinitial="c",targetblock=0,filename0="",bool=0):
        import string
        import copy
        
        prologue=ListStatements([])
        epilogue=ListStatements([])
        if language=="Cpp":
            tmp="void "+string.upper(filename0)+"::"
            tmp+=name
            tmp+="("
            varlist=[]
            if bool and not targetblock: varlist.append("Ref<Tensor>& out")

            if targetblock:
                varlist+=["double* a_i0"]
                for xx in self.target.indices.listindices:
                    for yy in xx.indices:
                        varlist.append("const long t_"+copy.deepcopy(yy.show(showdagger=0,incode=1))+"b")
            tmp+=string.join(varlist,",")
            tmp+="){"
            prologue.append(tmp)
                
            epilogue.append("}")

        #print prologue.show()
        #print epilogue.show()
        return prologue,epilogue    

    def codegeneration(self,name="test",language="Cpp",onetensor=0,targetpermutable=[],lsign=Sign(),\
                       lfraction=Fraction(),reusable=0,targetblock=0,filename0="",\
                       inp_initial1="a",inp_initial2="b",out_initial1="c",bool=0):

        inp_initial="a"
        out_initial="c"
        outlist=[]

        code1,code2=self.codeheader(language=language,
                                     name=name,
                                     inputinitial=inp_initial,
                                     outputinitial=out_initial,
                                     targetblock=targetblock,
                                     filename0=filename0,bool=bool)
        outlist+=code1.showlist(language=language)

        tmp="      "
        #tmp+=self.show()
        outlist.append(tmp)

        #tmplist=['#include "what to include"']
        #outlist+=tmplist

        code=self.translatetocode(language=language,
                                  name=name,
                                  inputinitial=inp_initial1,
                                  inputinitial2=inp_initial2,
                                  outputinitial=out_initial1,
                                  onetensor=onetensor,
                                  targetpermutable=targetpermutable,
                                  lsign=lsign,lfraction=lfraction,reusable=reusable,targetblock=targetblock)
        outlist+=code.showlist(language=language)

        outlist+=code2.showlist(language=language)

        #import string
        #print string.join(outlist,"\n")

        return outlist

    #def fortran77(self,name):
    def offset_codeheader(self,
                           language="Cpp",
                           name="test",
                           initial="a",
                           filename0=""):
        import string
        prologue=ListStatements([])
        epilogue=ListStatements([])
        if language=="Cpp":
            tmp="void "+string.upper(filename0)+"::"
            tmp+="offset_"+name
            tmp+="(){"
            #tmp+="(Tensor* d_"+initial+"){"
            prologue.append(tmp)
#           prologue.append("implicit none")
            
            tmp_initial=string.lower(initial)
            if (tmp_initial[0]=="i" or tmp_initial[0]=="k"):
                if (tmp_initial[1]=="1" and len(tmp_initial)>2 and tmp_initial[2]=="x"):
                    new_initial=tmp_initial[0:3]+"n["+tmp_initial[3:]+"]"
                else:
                    new_initial=tmp_initial[0]+"n["+tmp_initial[1:]+"]"
            else:
                new_initial=tmp_initial+"()"
            if (tmp_initial[0]=="i" and tmp_initial[1:]=="0"): new_initial="out"
            elif not (new_initial[0]=="i" or new_initial[0]=="k"): new_initial="z->"+new_initial
            epilogue.append(new_initial+"->set_filesize(size);") 
            epilogue.append(new_initial+"->createfile();") 
            epilogue.append("z->mem()->sync();") 
            epilogue.append("}")

        return prologue,epilogue    

    def offset_codegeneration(self,name="test",language="Cpp",targetpermutable=[],
                              filename0="",initial="a"):
        #initial="a"
        outlist=[]
        code1,code2=self.offset_codeheader(language=language,
                                            name=name,
                                            initial=initial,filename0=filename0)
        outlist+=code1.showlist(language=language)
        outlist.append(" ")
        code=self.target.offset(language=language,
                                initial=initial,
                                name=name)
        outlist+=code.showlist(language=language)
        outlist+=code2.showlist(language=language)

        return outlist 

class CodeListOperationTree(ListOperationTree):

    def checkall(self,i1count=0):
#
# and changing the symbol of the tensors here...
# 
        import copy
        import string
        if i1count: num_i1=0
        listsymbol=[]
        innersymbol=[]
        innersymbol2=[]
        listreusabletc=copy.deepcopy(self.reusablelist)
        for xx in listreusabletc:
            for yy in xx.tensors.tensors:
                if yy.symbol.split("_")[0]=="Q2":
                    compd=0
                    comps=0
                    for zz in yy.indices.listindices:
                        for ww in zz.indices:
                            if ww.comp and ww.dagger: compd+=1
                            if ww.comp and (not ww.dagger): comps+=1
                    if compd==2: yy.symbol="qx"
                    elif compd==1: yy.symbol="qy"
                    else: print "++++++++ something is wrong in checkall ++++++++"
                if yy.symbol.split("_")[0]=="L2":
                    compd=0
                    comps=0
                    for zz in yy.indices.listindices:
                        for ww in zz.indices:
                            if ww.comp and ww.dagger: compd+=1
                            if ww.comp and (not ww.dagger): comps+=1
                    if comps==2: yy.symbol="lx"
                    elif comps==1: yy.symbol="ly"
                    else: print "++++++++ something is wrong in checkall ++++++++"
                if yy.symbol.split("_")[0]=="S2":
                    compd=0
                    comps=0
                    for zz in yy.indices.listindices:
                        for ww in zz.indices:
                            if ww.comp and ww.dagger: compd+=1
                            if ww.comp and (not ww.dagger): comps+=1
                    if compd==2: yy.symbol="sx"
                    elif compd==1: yy.symbol="sy"
                    else: print "++++++++ something is wrong in checkall ++++++++"
                if yy.symbol.split("_")[0]=="R2":
                    compd=0
                    comps=0
                    for zz in yy.indices.listindices:
                        for ww in zz.indices:
                            if ww.comp and ww.dagger: compd+=1
                            if ww.comp and (not ww.dagger): comps+=1
                    if   compd==2 and comps==0: yy.symbol="fx"
                    elif compd==1 and comps==0: yy.symbol="fx"
                    elif compd==0 and comps==2: yy.symbol="fy"
                    elif compd==0 and comps==1: yy.symbol="fy"
                    else: print "++++++++ something is wrong in checkall ++++++++"
                if yy.symbol.split("_")[0]=="t2":
                    compd=0
                    comps=0
                    for zz in yy.indices.listindices:
                        for ww in zz.indices:
                            if ww.showtype()=="hole" and ww.dagger: compd+=1
                            if ww.showtype()=="hole" and (not ww.dagger): comps+=1
                    if   compd==2 and comps==2: yy.symbol="c2"
                if yy.symbol.split("_")[0]=="l2":
                    compd=0
                    comps=0
                    for zz in yy.indices.listindices:
                        for ww in zz.indices:
                            if ww.showtype()=="hole" and ww.dagger: compd+=1
                            if ww.showtype()=="hole" and (not ww.dagger): comps+=1
                    if   compd==2 and comps==2: yy.symbol="lc2"
                if yy.symbol.split("_")[0]=="s2":
                    compd=0
                    comps=0
                    for zz in yy.indices.listindices:
                        for ww in zz.indices:
                            if ww.showtype()=="hole" and ww.dagger: compd+=1
                            if ww.showtype()=="hole" and (not ww.dagger): comps+=1
                    if   compd==2 and comps==2: yy.symbol="sc2"
                if not yy.symbol.split("_")[0] in listsymbol:
                    if not (yy.symbol[0]=="J" or yy.symbol[0]=="I" or yy.symbol[0]=="K"):
                        listsymbol.append(yy.symbol.split("_")[0]) 
                    elif (not ("I"+yy.symbol.split("_")[0][1:]) in innersymbol) and (not yy.symbol[0]=="K"):
                        if not yy.symbol.split("_")[0] in innersymbol:
                            if not (i1count and yy.symbol.split("_")[0][1:]=="1"):
                                innersymbol.append("I"+yy.symbol.split("_")[0][1:])
                            else:
                                bk_yysymb=yy.symbol.split("_")
                                bk_yysymb[0]="I1x"+str(num_i1)
                                yy.symbol=string.join(bk_yysymb,"_")
                                num_i1+=1
                    elif yy.symbol[0]=="K":
                        if not yy.symbol in innersymbol2:
                            innersymbol2.append("K"+yy.symbol.split("_")[0][1:])
                        
        trees=self.tree
        while 1:
            tmptrees=[]
            for xx in trees:
                mytensors=xx.operation.tensors.tensors
                for yy in mytensors:
                    if yy.symbol.split("_")[0]=="Q2":
                        compd=0
                        comps=0
                        for zz in yy.indices.listindices:
                            for ww in zz.indices:
                                if ww.comp and ww.dagger: compd+=1
                                if ww.comp and (not ww.dagger): comps+=1
                        if compd==2: yy.symbol="qx"
                        elif compd==1: yy.symbol="qy"
                        else: print "++++++++ something is wrong in checkall ++++++++"
                    if yy.symbol.split("_")[0]=="L2":
                        compd=0
                        comps=0
                        for zz in yy.indices.listindices:
                            for ww in zz.indices:
                                if ww.comp and ww.dagger: compd+=1
                                if ww.comp and (not ww.dagger): comps+=1
                        if comps==2: yy.symbol="lx"
                        elif comps==1: yy.symbol="ly"
                        else: print "++++++++ something is wrong in checkall ++++++++"
                    if yy.symbol.split("_")[0]=="S2":
                        compd=0
                        comps=0
                        for zz in yy.indices.listindices:
                            for ww in zz.indices:
                                if ww.comp and ww.dagger: compd+=1
                                if ww.comp and (not ww.dagger): comps+=1
                        if compd==2: yy.symbol="sx"
                        elif compd==1: yy.symbol="sy"
                        else: print "++++++++ something is wrong in checkall ++++++++"
                    if yy.symbol.split("_")[0]=="R2":
                        compd=0
                        comps=0
                        for zz in yy.indices.listindices:
                            for ww in zz.indices:
                                if ww.comp and ww.dagger: compd+=1
                                if ww.comp and (not ww.dagger): comps+=1
                        if   compd==2 and comps==0: yy.symbol="fx"
                        elif compd==1 and comps==0: yy.symbol="fx"
                        elif compd==0 and comps==2: yy.symbol="fy"
                        elif compd==0 and comps==1: yy.symbol="fy"
                        else: print "++++++++ something is wrong in checkall ++++++++"
                    if yy.symbol.split("_")[0]=="t2":
                        compd=0
                        comps=0
                        for zz in yy.indices.listindices:
                            for ww in zz.indices:
                                if ww.showtype()=="hole" and ww.dagger: compd+=1
                                if ww.showtype()=="hole" and (not ww.dagger): comps+=1
                        if   compd==2 and comps==2: yy.symbol="c2"
                    if yy.symbol.split("_")[0]=="l2":
                        compd=0
                        comps=0
                        for zz in yy.indices.listindices:
                            for ww in zz.indices:
                                if ww.showtype()=="hole" and ww.dagger: compd+=1
                                if ww.showtype()=="hole" and (not ww.dagger): comps+=1
                        if   compd==2 and comps==2: yy.symbol="lc2"
                    if yy.symbol.split("_")[0]=="s2":
                        compd=0
                        comps=0
                        for zz in yy.indices.listindices:
                            for ww in zz.indices:
                                if ww.showtype()=="hole" and ww.dagger: compd+=1
                                if ww.showtype()=="hole" and (not ww.dagger): comps+=1
                        if   compd==2 and comps==2: yy.symbol="sc2"
                    if not yy.symbol.split("_")[0] in listsymbol:
                        if not (yy.symbol[0]=="J" or yy.symbol[0]=="I" or yy.symbol[0]=="K"):
                            listsymbol.append(yy.symbol.split("_")[0]) 
                        elif (not ("I"+yy.symbol.split("_")[0][1:]) in innersymbol) and (not yy.symbol[0]=="K"):
                            if not yy.symbol.split("_")[0] in innersymbol:
                                if not (i1count and yy.symbol.split("_")[0][1:]=="1"):
                                    innersymbol.append("I"+yy.symbol.split("_")[0][1:])
                                else:
                                    bk_yysymb=yy.symbol.split("_")
                                    bk_yysymb[0]="I1x"+str(num_i1)
                                    yy.symbol=string.join(bk_yysymb,"_")
                                    num_i1+=1
                        elif yy.symbol[0]=="K":
                            if not yy.symbol in innersymbol2:
                                innersymbol2.append("K"+yy.symbol.split("_")[0][1:])
                        
                mytensors=xx.operator
                for yy in mytensors:
                    if yy.tensor.symbol.split("_")[0]=="Q2":
                        compd=0
                        comps=0
                        for zz in yy.tensor.indices.listindices:
                            for ww in zz.indices:
                                if ww.comp and ww.dagger: compd+=1
                                if ww.comp and (not ww.dagger): comps+=1
                        if compd==2: yy.tensor.symbol="qx"
                        elif compd==1: yy.tensor.symbol="qy"
                        else: print "++++++++ something is wrong in checkall ++++++++"
                    if yy.tensor.symbol.split("_")[0]=="S2":
                        compd=0
                        comps=0
                        for zz in yy.tensor.indices.listindices:
                            for ww in zz.indices:
                                if ww.comp and ww.dagger: compd+=1
                                if ww.comp and (not ww.dagger): comps+=1
                        if compd==2: yy.tensor.symbol="sx"
                        elif compd==1: yy.tensor.symbol="sy"
                        else: print "++++++++ something is wrong in checkall ++++++++"
                    if yy.tensor.symbol.split("_")[0]=="L2":
                        compd=0
                        comps=0
                        for zz in yy.tensor.indices.listindices:
                            for ww in zz.indices:
                                if ww.comp and ww.dagger: compd+=1
                                if ww.comp and (not ww.dagger): comps+=1
                        if comps==2: yy.tensor.symbol="lx"
                        elif comps==1: yy.tensor.symbol="ly"
                        else: print "++++++++ something is wrong in checkall ++++++++"
                    if yy.tensor.symbol.split("_")[0]=="R2":
                        compd=0
                        comps=0
                        for zz in yy.tensor.indices.listindices:
                            for ww in zz.indices:
                                if ww.comp and ww.dagger: compd+=1
                                if ww.comp and (not ww.dagger): comps+=1
                        if   compd==2 and comps==0: yy.tensor.symbol="fx"
                        elif compd==1 and comps==0: yy.tensor.symbol="fx"
                        elif compd==0 and comps==2: yy.tensor.symbol="fy"
                        elif compd==0 and comps==1: yy.tensor.symbol="fy"
                        else: print "++++++++ something is wrong in checkall ++++++++"
                    if yy.tensor.symbol.split("_")[0]=="t2":
                        compd=0
                        comps=0
                        for zz in yy.tensor.indices.listindices:
                            for ww in zz.indices:
                                if ww.showtype()=="hole" and ww.dagger: compd+=1
                                if ww.showtype()=="hole" and (not ww.dagger): comps+=1
                        if   compd==2 and comps==2: yy.tensor.symbol="c2"
                    if yy.tensor.symbol.split("_")[0]=="l2":
                        compd=0
                        comps=0
                        for zz in yy.tensor.indices.listindices:
                            for ww in zz.indices:
                                if ww.showtype()=="hole" and ww.dagger: compd+=1
                                if ww.showtype()=="hole" and (not ww.dagger): comps+=1
                        if   compd==2 and comps==2: yy.tensor.symbol="lc2"
                    if yy.tensor.symbol.split("_")[0]=="s2":
                        compd=0
                        comps=0
                        for zz in yy.tensor.indices.listindices:
                            for ww in zz.indices:
                                if ww.showtype()=="hole" and ww.dagger: compd+=1
                                if ww.showtype()=="hole" and (not ww.dagger): comps+=1
                        if   compd==2 and comps==2: yy.tensor.symbol="sc2"
                    if not yy.tensor.symbol.split("_")[0] in listsymbol:
                        yysymb=yy.tensor.symbol
                        if not (yysymb[0]=="J" or yysymb[0]=="I" or yysymb[0]=="K"):
                            listsymbol.append(yysymb.split("_")[0]) 
                        elif (not ("I"+yysymb.split("_")[0][1:]) in innersymbol) and (not yysymb[0]=="K"):
                            if not yysymb.split("_")[0] in innersymbol:
                                if not (i1count and yy.symbol.split("_")[0][1:]=="1"):
                                    innersymbol.append("I"+yy.symbol.split("_")[0][1:])
                                else:
                                    bk_yysymb=yysymb.split("_")
                                    bk_yysymb[0]="I1x"+str(num_i1)
                                    yysymb=string.join(bk_yysymb,"_")
                                    num_i1+=1
                        elif yysymb[0]=="K":
                            if not yysymb in innersymbol2:
                                innersymbol2.append("K"+yysymb.split("_")[0][1:])

                for zz in xx.children: 
                    tmptrees.append(zz)
            if len(tmptrees)==0: break
            trees=copy.deepcopy(tmptrees)

        listsymbol.sort()
        if i1count:
            tmplistsymbol=[]
            for zz in range(num_i1):
                tmplistsymbol.append("I1x"+str(zz))
            listsymbol=tmplistsymbol+listsymbol

        #innersymbol.sort()
        #tentative
        is2max=len(self.reusablelist)
        for zz in range(is2max):
            innersymbol.append("K"+str(zz))

        return listsymbol,innersymbol

    def makecall(self,listsymbol,tmpcode,tmplen,noi=1,noint=1,toggle=0,targetblock=0,header=0):
        import copy
        import string
        arg=[]
        if (not noi) and (not toggle): 
            arg.append("z->in.at(0)")
            arg.append("k_i0_offset")
        for xx in listsymbol:
            bool=0
            if toggle and string.lower(xx[0])=="k":
                if not targetblock:
                    tmp_initial=string.lower(xx)
                    if (tmp_initial[0]=="i" or tmp_initial[0]=="k"):
                        if (toggle and tmp_initial[0:2]=="i1"):
                            new_initial=tmp_initial[0:3]+"n.at("+tmp_initial[3:]+")"
                        else:
                            new_initial=tmp_initial[0]+"n.at("+tmp_initial[1:]+")"
                    else:
                        new_initial=tmp_initial+"()"
                    if (tmp_initial[0]=="i" and tmp_initial[1:]=="0"): 
                        new_initial="out"
                        bool=1
                    elif not (new_initial[0]=="i" or new_initial[0]=="k"): new_initial="z->"+new_initial
                    arg.append(new_initial)
                continue
            if toggle and len(xx)>2:
                continue
#                if xx[0:3]=="I1x":
#                    tmp_initial=string.lower(xx)
#                    if (tmp_initial[0]=="i" or tmp_initial[0]=="k"):
#                        new_initial=tmp_initial[0]+"n["+tmp_initial[1:].split("x")[1]+"]"
#                    else:
#                        new_initial=tmp_initial+"()"
#                    if (tmp_initial[0]=="i" and tmp_initial[1:]=="0"): 
#                        new_initial="out"
#                        bool=1
#                    elif not (new_initial[0]=="i" or new_initial[0]=="k"): new_initial="z->"+new_initial
#                    arg.append(new_initial)
#                    continue 
            if (not noint) and (xx[0]=="I" or xx[0]=="K"): continue
            if targetblock and string.lower(xx)=="i0": continue
            if not targetblock:
                tmp_initial=string.lower(xx)
                if (tmp_initial[0]=="i" or tmp_initial[0]=="k"):
                    if (toggle and tmp_initial[0:2]=="i1"):
                        new_initial=tmp_initial[0:3]+"n.at("+tmp_initial[3:]+")"
                    else:
                        new_initial=tmp_initial[0]+"n.at("+tmp_initial[1:]+")"
                else:
                    new_initial=tmp_initial+"()"
                if (tmp_initial[0]=="i" and tmp_initial[1:]=="0"): 
                    new_initial="out"
                    bool=1
                elif not (new_initial[0]=="i" or new_initial[0]=="k"): new_initial="z->"+new_initial
                arg.append(new_initial)
        if not noi: arg.sort()

        if toggle or targetblock:
            arg=["a_i0"]+arg

        if targetblock:
            for xx in self.tree[0].outindices.listindices:
                for yy in xx.indices:
                    arg.append("t_"+copy.deepcopy(yy.show(showdagger=0,incode=1))+"b")
        if toggle:
            arg.append("toggle")

        if not targetblock:
            tmpstr=""
            icnt=0
            for xx in arg:
                mylen=len(xx)
                if icnt<len(arg)-2:    
                    tmpstr+=xx+","
                    icnt+=1
                else: 
                    tmpstr+=xx+"=>"
            tmpstr=tmpstr[:-2]

            if bool: tmpcode+="out"
            tmpcode+=")"
            if header:
                tmpcode+="{"
            else:
                tmpcode+=";"
            tmpstr=tmpcode+" //"+tmpstr
        else:
            tmpstr=""
            icnt=0
            for xx in arg:
                mylen=len(xx)
                if header:
                    if icnt==0: tmpstr+="double* "
                    else:       tmpstr+="const long "
                if icnt<len(arg)-2:    
                    tmpstr+=xx+","
                    icnt+=1
                else: 
                    tmpstr+=xx+","
            tmpstr=tmpstr[:-1]
            tmpcode+=tmpstr+")"
            if header:
                tmpcode+="{"
            else:
                tmpcode+=";"
            tmpstr=tmpcode
        return tmpstr

    def header(self,classname,targetblock):
        import string
        if(targetblock): tmplist =['#include <vector>']
        tmplist =['#include <algorithm>']
        #tmplist+=['#include <chemistry/qc/ccr12/'+classname.split("_")[0]+'/'+classname+'.h>']
        tmplist+=['#include "'+classname+'.h"']
        #tmplist+=['#include <chemistry/qc/ccr12/tensor.h>']
        tmplist+=['#include "tensor.h"']
        tmplist+=['using namespace sc;']
        tmplist+=['  ']
        tmplist+=['  ']
        tmplist+=[string.upper(classname)+"::"+string.upper(classname)+"(CCR12_Info* info):z(info){};"]
        tmplist+=[string.upper(classname)+"::~"+string.upper(classname)+"(){};"]
        return string.join(tmplist,"\n")

#   def fortran77(self,toggle=0):
    def Cpp(self,toggle=0):
        import copy
        dummy,subroutines=copy.deepcopy(self).translatetocode(toggle=toggle)
        return subroutines
        
    def translatetocode(self,header=1,code="",subroutines="",reusable=0,toggle=0,num_i1=0): 
        import string
        import copy
        pname=self.filename.split(".")[0]
        cline="  "
        
        if not code:
            code=copy.deepcopy(self.code)
            self.code.tag=self.filename.split(".")[0]

        i1count=toggle*header
        listsymbol,innersymbol=self.checkall(i1count)
        com =[]
        com+="//    This is a C++ code generated by SMITH\n"
        com+="//    Copyright (C) University of Florida\n"
        com+="  "
        tmpcode="void "
        tmplen=6
        tmpcode+=string.upper(self.filename.split(".")[0])+"::compute_amp("
        if not toggle: tmpcode+="Ref<Tensor>& out"
        
        if header:
            code.append(cline)
            code.append(string.join(com,""))
            code.append(self.header(pname,i1count)) 
            code.append(cline)
            code.append(cline)
            code.append(cline)
            reusablesymbol=[]
            for xx in innersymbol:
                if xx[0]=="K": reusablesymbol.append(string.lower(xx))

            if not toggle:
                code.append(self.makecall(listsymbol,tmpcode,tmplen,noi=0,noint=0,toggle=toggle,targetblock=i1count,header=1))
            else:
                code.append(self.makecall(listsymbol+reusablesymbol,tmpcode,tmplen,noi=0,noint=0,toggle=toggle,targetblock=i1count,header=1))
            code.append(cline)
            code.append("in.resize(8);")
            code.append("kn.resize(64);")
            if toggle:
                code.append("i1xn.resize(16);")
            code.append(cline)
            subroutines=Subroutines()
 
            #eusablesymbol.sort()
            if not len(reusablesymbol)==len(self.reusablelist):
                print "reusable list ?"
            if toggle:
                code.append("if (toggle==1L) {")
            for ix in range(len(reusablesymbol)):
                xx=reusablesymbol[ix]
                yy=self.reusablelist[ix]
                ffilename="\""+self.filename.split(".")[0]+"_"+xx+"\""
                tmp_initial=string.lower(xx)
                if (tmp_initial[0]=="i" or tmp_initial[0]=="k"):
                    if (toggle and tmp_initial[0:2]=="i1"):
                        new_initial=tmp_initial[0:3]+"n.at("+tmp_initial[3:]+")"
                    else:
                        new_initial=tmp_initial[0]+"n.at("+tmp_initial[1:]+")"
                else:
                    new_initial=tmp_initial+"()"
                if (tmp_initial[0]=="i" and tmp_initial[1:]=="0"): new_initial="out"
                elif not (new_initial[0]=="i" or new_initial[0]=="k"): new_initial="z->"+new_initial
                tmpcode=new_initial+"=new Tensor("+ffilename+",z->mem());"
                code.append(copy.deepcopy(tmpcode))
                tmpcode="offset_"+xx+"();"
                code.append(copy.deepcopy(tmpcode))
                yyoutindices=yy.target.indices
                yysymbol=string.lower(yy.target.symbol)
                yyot=OperationTree(yy,yyoutindices,yysymbol)
                yyt1=yy.tensors.tensors[1]
                yyfactor=Factor(Sign(),Fraction())
                yyot.operator=[LastOperator(yyt1,yyfactor,yyt1.indices.permutable)]
                yyot.permutable=yy.target.indices.permutable
                yyclot=CodeListOperationTree([copy.deepcopy(yyot)])
                yyclot.filename=self.filename
                code,subroutines=yyclot.translatetocode(header=0,
                                                        code=code,
                                                        subroutines=subroutines,
                                                        reusable=1)
                #tmpcode="d_"+xx+"->sync();"
                #code.append(copy.deepcopy(tmpcode))
                name=xx
                tmpcode=yy.a2c().offset_codegeneration(name=name,targetpermutable=yyot.permutable,filename0=self.filename.split(".")[0],initial=xx)
                stmpcode=Code(code=tmpcode,tag=(name+"_offset"))
                subroutines.append(copy.deepcopy(stmpcode))

        for ii in range(len(self.tree)):
            done=0
            tree=self.tree[ii] 
            listtmpcode=[]
            tmpcode=""
            listsymbol=[]
            tensors=tree.operation.tensors.tensors
            if not tree.children:
                if len(tensors)==1:
                    done=1
                    if toggle and header: "please add some lines in translatetocode function"
                    tmpcode+="smith_"
                    tmpcode+=tree.operation.target.symbol[1:]+"("
                    #print tree.operation.target.symbol[1:]
                    tmplen=5+len(tree.operation.target.symbol[1:])
                    listsymbol.append(tensors[0].symbol.split("_")[0])
                    if toggle and tree.operation.target.symbol.split("_")[0][1:]=="0" and len(tree.operation.target.symbol)>5:
                        listsymbol.append("i1x"+str(num_i1))
                    elif len(tree.operation.target.symbol)>5:
                        listsymbol.append("i"+str(int(tree.operation.target.symbol.split("_")[0][1:])+1))
                    else:
                        listsymbol.append("i"+tree.operation.target.symbol.split("_")[0][1:])
                    tmpcode=self.makecall(listsymbol,tmpcode,tmplen) 
                    listtmpcode.append(copy.deepcopy(tmpcode))

                    myctc=tree.operation.a2c() 
                    tmpperm=ListAnalyzedIndices(tree.operation.target.indices.permutable)
                    name="smith_"+tree.operation.target.symbol[1:]
                    if header:
                        print myctc
                        outlist=copy.deepcopy(myctc.codegeneration(name=name,onetensor=1,\
                                          targetpermutable=tmpperm,lsign=tree.operator[0].factor.sign,filename0=self.filename.split(".")[0],\
                                          inp_initial1=listsymbol[0],out_initial1=listsymbol[1],bool=header))
                    else:
                        outlist=copy.deepcopy(myctc.codegeneration(name=name,onetensor=1,\
                                          targetpermutable=tmpperm,lsign=tree.operation.factor.sign,filename0=self.filename.split(".")[0],\
                                          inp_initial1=listsymbol[0],out_initial1=listsymbol[1]))
                    stmpcode=Code(code=outlist,tag=name)
                    subroutines.append(copy.deepcopy(stmpcode))
                    
                elif len(tree.operator)<2:
                    if toggle and header: 
                        code.code.reverse()
                        if code and code.code[0][0:10]=="if (toggle": 
                            code.code.pop(0)
                            code.code.reverse()
                        else:
                            code.code.reverse()
                            code.code.append("}")
                        listtmpcode.append("if (toggle==2L) {")

                    tmpcode+="smith_"
                    if not reusable:
                        tmpcode+=tree.operation.target.symbol[1:]+"("
                        tmplen=6+len(tree.operation.target.symbol[1:])
                    else:
                        tmpcode+=string.lower(tree.operation.target.symbol)+"("
                        tmplen=6+len(tree.operation.target.symbol)
                    listsymbol.append(tensors[0].symbol.split("_")[0])
                    listsymbol.append(tensors[1].symbol.split("_")[0]) 
                    if reusable:
                        listsymbol.append("k"+tree.operation.target.symbol.split("_")[0][1:])
                    elif toggle and tree.operation.target.symbol.split("_")[0][1:]=="1":
                        listsymbol.append("i1x"+str(num_i1))
                    else:
                        listsymbol.append("i"+tree.operation.target.symbol.split("_")[0][1:])
                    tmpcode=self.makecall(listsymbol,tmpcode,tmplen,targetblock=toggle*header) 
                    listtmpcode.append(copy.deepcopy(tmpcode))
                    done=1

                    myctc=tree.operation.a2c() 
                    if not reusable:
                        name="smith_"+tree.operation.target.symbol[1:]
                    else:
                        name="smith_"+string.lower(tree.operation.target.symbol)
                    outlist=copy.deepcopy(myctc.codegeneration(name=name,\
                                          targetpermutable=tree.permutable,lsign=tree.operator[0].factor.sign,reusable=reusable,targetblock=toggle*header,\
                                          filename0=self.filename.split(".")[0],inp_initial1=listsymbol[0],inp_initial2=listsymbol[1],out_initial1=listsymbol[2],
                                          bool=header))
                    stmpcode=Code(code=outlist,tag=name)
                    subroutines.append(copy.deepcopy(stmpcode))
                    if toggle and header: 
                        listtmpcode.append("}")
                        listtmpcode.append("if (toggle==1L) {")
                    
            if not done:
                if tree.children: myctc=tree.children[0].operation.a2c() 
                else: myctc=tree.operator[0].operator2ctc() 
                name="smith_"+tree.operation.target.symbol[1:]
                iinitial="i"+tensors[1].symbol.split("_")[0][1:]
                outlist=myctc.offset_codegeneration(name=name,targetpermutable=tree.permutable,filename0=self.filename.split(".")[0],initial=iinitial)
                stmpcode=Code(code=outlist,tag=(name+"_offset"))
                subroutines.append(copy.deepcopy(stmpcode))
                    
                listsymbol.append(iinitial) 

                ffilename="\""+self.filename.split(".")[0]+"_"+tensors[1].symbol[1:]+"\""
                intsymbol="i"+tensors[1].symbol.split("_")[0][1:]
                tmp_initial=string.lower(intsymbol)
                if (tmp_initial[0]=="i" or tmp_initial[0]=="k"):
                    if (toggle and tmp_initial[0:2]=="i1"):
                        new_initial=tmp_initial[0:3]+"n.at("+tmp_initial[3:]+")"
                    else:
                        new_initial=tmp_initial[0]+"n.at("+tmp_initial[1:]+")"
                else:
                    new_initial=tmp_initial+"()"
                if (tmp_initial[0]=="i" and tmp_initial[1:]=="0"): new_initial="out"
                elif not (new_initial[0]=="i" or new_initial[0]=="k"): new_initial="z->"+new_initial
                tmpcode=new_initial+"=new Tensor("+ffilename+",z->mem());"
                listtmpcode.append(copy.deepcopy(tmpcode))

                tmpcode="offset_"+name+"();"
                listtmpcode.append(copy.deepcopy(tmpcode))

                code.append(string.join(listtmpcode,"\n"))
                listtmpcode=[]

                mytarget=copy.deepcopy(tensors[1])
                mylot=[]
                cnt=0
                for xx in tree.operator:
                    mytensors=AnalyzedTensorSequence([copy.deepcopy(xx.tensor)])
                    myfactor =copy.deepcopy(xx.factor)
                    mypermutations=Permutations()
                    mysum=ListAnalyzedIndices([])
                    myts=TensorContraction(mytarget,myfactor,mypermutations,mysum,mytensors)
                    myoutindices=mytarget.indices
                    mytarget.symbol=tree.operation.target.symbol+"_"+str(cnt)
                    mysymbol=mytarget.symbol
                    
                    cnt+=1
                    myot=OperationTree(myts,myoutindices,mysymbol)
                    mylot.append(copy.deepcopy(myot))
                for xx in tree.children:
                    mylot.append(copy.deepcopy(xx))
                myclot=CodeListOperationTree(mylot)
                myclot.filename=self.filename
                code,subroutines=myclot.translatetocode(header=0,
                                                        code=code,
                                                        subroutines=subroutines,toggle=toggle,num_i1=num_i1)
                    
                #tmpcode="reconcilefile(d_"+intsymbol+")"
                #listtmpcode.append(copy.deepcopy(tmpcode))

                if toggle and header: 
                    if listtmpcode:
                        listtmpcode.reverse()
                        if listtmpcode[0][0:10]=="if (toggle": 
                            listtmpcode.pop(0)
                            listtmpcode.reverse()
                        else:
                            listtmpcode.reverse()
                            listtmpcode.append("}")
                    else:
                        listtmpcode.append("}")
                    listtmpcode.append("if (toggle==2L) {")
                #elif toggle and (not header):
                #    listtmpcode.append(" "*6+"if (toggle.eq.1) then")
                tmpcode="smith_"
                tmpcode+=tree.operation.target.symbol[1:]+"("
                tmplen=6+len(tree.operation.target.symbol[1:])
                listsymbol.append(tensors[0].symbol.split("_")[0])
                listsymbol.reverse()
                if toggle and tree.operation.target.symbol.split("_")[0][1:]=="1":
                    listsymbol.append("i1x"+str(num_i1))
                else:
                    listsymbol.append("i"+tree.operation.target.symbol.split("_")[0][1:])
            
                tmpcode=self.makecall(listsymbol,tmpcode,tmplen,targetblock=toggle*header) 
                listtmpcode.append(copy.deepcopy(tmpcode))
                if toggle and header: 
                    listtmpcode.append("}")
                    listtmpcode.append("if (toggle==1L) {")

                myctc=tree.operation.a2c() 
                name="smith_"+tree.operation.target.symbol[1:]
                outlist=copy.deepcopy(myctc.codegeneration(name=name,targetpermutable=tree.permutable,targetblock=toggle*header,\
                                                           filename0=self.filename.split(".")[0],inp_initial1=listsymbol[0],\
                                                           inp_initial2=listsymbol[1],out_initial1=listsymbol[2],bool=header))
                stmpcode=Code(code=outlist,tag=name)
                subroutines.append(copy.deepcopy(stmpcode))
                    
                if not (toggle and header):
                    tmp_initial=string.lower(intsymbol)
                    if (tmp_initial[0]=="i" or tmp_initial[0]=="k"):
                        if (toggle and tmp_initial[0:2]=="i1"):
                            new_initial=tmp_initial[0:3]+"n.at("+tmp_initial[3:]+")"
                        else:
                            new_initial=tmp_initial[0]+"n.at("+tmp_initial[1:]+")"
                    else:
                        new_initial=tmp_initial+"()"
                    if (tmp_initial[0]=="i" and tmp_initial[1:]=="0"): new_initial="out"
                    elif not (new_initial[0]=="i" or new_initial[0]=="k"): new_initial="z->"+new_initial
                    tmpcode="delete "+new_initial+";"
                    listtmpcode.append(copy.deepcopy(tmpcode))
    
                else:
                    reusablesymbol.append(intsymbol)
                    num_i1+=1 

            for xx in listtmpcode:
                code.append(xx)
            #code.append(string.join(listtmpcode,"\n"))
        if header:
            if toggle and header: 
                code.code.reverse()
                if code.code[0][0:10]=="if (toggle": 
                    code.code.pop(0)
                    code.code.reverse()
                else:
                    code.code.reverse()
                    code.code.append("}")
                code.append("if (toggle==3L) {")
            reusablesymbol.reverse()
            for xx in reusablesymbol:
                tmp_initial=string.lower(xx)
                if (tmp_initial[0]=="i" or tmp_initial[0]=="k"):
                    if (toggle and tmp_initial[0:2]=="i1"):
                        new_initial=tmp_initial[0:3]+"n.at("+tmp_initial[3:]+")"
                    else:
                        new_initial=tmp_initial[0]+"n.at("+tmp_initial[1:]+")"
                else:
                    new_initial=tmp_initial+"()"
                if (tmp_initial[0]=="i" and tmp_initial[1:]=="0"): new_initial="out"
                elif not (new_initial[0]=="i" or new_initial[0]=="k"): new_initial="z->"+new_initial
                tmpcode="delete "+new_initial+";"
                code.append(copy.deepcopy(tmpcode))
    
            if toggle:
                code.code.reverse()
                if code and code.code[0][0:10]=="if (toggle": 
                    code.code.pop(0)
                    code.code.reverse()
                else:
                    code.code.reverse()
                    code.code.append("}")

            #tmpcode="return 0"
            #code.append(tmpcode)
            code.append(cline)
            tmpcode="}"
            code.append(tmpcode)
            subroutines.append(code)
        return code,subroutines

class Code:
    def __init__(self,code=[],tag=""):
        self.tag=tag
        self.code=code
    
    def __str__(self):
        return self.show()

    def append(self,value):
        self.code.append(value)
        return self

    def __cmp__(self,other):
        return cmp(self.tag,other.tag)

    def show(self):
        import string
        return string.join(self.code,"\n")

class Subroutines:
    def __init__(self,subroutines=[]):
        self.subroutines=subroutines

    def __str__(self):
        return self.show()

    def show(self):
        import string
        self.subroutines.sort()
        tmp=[]
        for xx in self.subroutines:
            tmp.append(xx.show())
        filecontent=string.join(tmp,"\n  \n")
        #print filecontent
        return filecontent

    def append(self,value):
        self.subroutines.append(value)
        return self

    def writetofile(self,filename):
        output=self.show()
        outfile=open(filename,'w')
        outfile.write(output) 
        outfile.close()
        
    
class PermutationTable:
    def __init__(self,permutation,sign):
        # permutation <- Indexpairs
        self.permutation=permutation
        self.sign       =sign

    def __str__(self):
        return self.show()

    def show(self):
        # -> string
        show ="Sign : "
        show+=self.sign.show()
        show+=", Permutation :"
        show+=self.permutation.pshow()
        return show
        
    def permute(self,target):
        # target <- Index
        return self.permutation.showpairof(target,key=0)


class Conditions:
    def __init__(self,condition=[],operator="and"):
        # condition <- [Comparison] or [Conditions] or [ str ]
        # operator   <- "and","or"...
        self.condition = condition
        self.operator  = operator

    def __add__(self,other):
        if not self.operator==other.operator:
            print "Cannot operate",self.show,"+",other.show()

        import copy
        myoperator =copy.deepcopy(self.operator)
        mycondition=copy.deepcopy(self.condition) \
                   +copy.deepcopy(other.condition)

        return Conditions(mycondition,myoperator)

    def __str__(self):
        return "Conditions: "+self.show()
    
    def show(self,language="Cpp"):
        if language=="Cpp":
            return self.showCpp()

    def showCpp(self):
        myopr=self.operator
        if myopr=="and":
            opr=" && "
        elif myopr=="or":
            opr=" || "

        if not self.condition:
            return ""
        out="("
        for xx in self.condition:
            #out+=" "
            if isinstance(xx,str):
                out+=xx
            else:
                out+=xx.showCpp(nop=1)
            #out+=" "
            out+=opr
        out=out[:-len(opr)]
        out+=")"

        return out
    
class Comparison:
    def __init__(self,x1,x2,operator):
        # x1,x2 <- String
        # operator <= ">","<",,,
        self.x1      =x1
        self.x2      =x2
        self.operator=operator
        
    def show(self,language="Cpp"):
        if language=="Cpp":
            return self.showCpp()

    def showCpp(self,nop=0):
        import string
        myopr=self.operator
        if myopr==">" or myopr=="gt":
            opr=">"
        elif myopr==">=" or myopr=="ge":
            opr=">="
        elif myopr=="<" or myopr=="lt":
            opr="<"
        elif myopr=="<=" or myopr=="le":
            opr="<="
        elif myopr=="==" or myopr=="eq":
            opr="=="
        elif myopr=="/=" or myopr=="ne":
            opr="!="

        #out=string.join(["(",self.x1,
        #                opr,self.x2,")"])
        if nop:
            out=self.x1+opr+self.x2
        else:
            out="("+self.x1+opr+self.x2+")"

        return out

class Statement:
    def __init__(self,statement=""):
        # statement <- str
        self.statement = statement


    def __add__(self,other):
        tmp=self.statement+other.statement
        return Statement(tmp)
        
    def showlist(self,nowrap=0,language="Cpp",indent=0):
        # -> [String]
        out=[]
        if nowrap:
            show =" "*indent
            show+=self.statement
            out.append(show)
        else:
            aa=self.wrap(language,indent)
            out+=aa
        return out
        
    def show(self,nowrap=0,language="Cpp",indent=0):
        import string
        if nowrap:
            show =" "*indent
            show+=self.statement
        else:
            aa=self.wrap(language,indent)
            show=string.join(aa,"\n")
        return show

    def wrap(self,language="Cpp",indent=0):
        # -> [ String, ]
        import string

        mysentence=self.statement

        if language=="Cpp":
            baseindent  =""
            wrapedindent=""
            linefeed    =""
            wraplen     =500
        elif language=="Fortran90":
            baseindent  =""
            wrapedindent=baseindent
            linefeed    ="&"
            wraplen     =500
        elif language=="Python":
            baseindent  =""
            wrapedindent=baseindent
            linefeed    =""
            wraplen     =90 #not official

        Asentence=mysentence.split()


        listshow=[]
        tmp=baseindent+" "*indent
        for xx in Asentence:
                
            if not wraplen or \
               len(tmp)+len(xx)+len(linefeed)+1<wraplen:
                tmp+=xx
                tmp+=" "
            else:
                tmp+=linefeed
                listshow.append(tmp)
                tmp=wrapedindent+" "*indent
                tmp+=xx
                tmp+=" "
        if tmp:
            listshow.append(tmp)
        return listshow

class ListStatements:
    def __init__(self,statements):
        # statements <- [Statement, Loop, Conditionalbranch..]
        self.statements=statements
        
    def __str__(self):
        return self.show()

    def __len__(self):
        return len(self.statements)

    def __getitem__(self,key):
        return self.statements[key]

    def showlist(self,nowrap=0,language="Cpp",indent=0):
        # -> [String]

        out=[]
        for xx in self.statements:
            out+=xx.showlist(nowrap,language,indent)
        return out
    
    def show(self,nowrap=0,language="Cpp",indent=0):
        # -> String
        import string

        aa=self.showlist(nowrap,language,indent)
        tmp=string.join(aa,"\n")

        return tmp

    def append(self,inp):
        if isinstance(inp,ListStatements):
            self.statements+=inp.statements

        elif isinstance(inp,str):
            tmp=Statement(inp)
            self.statements.append(tmp)
        else:
            self.statements.append(inp)

    
class Loop:
    def __init__(self,variable,initial,final,statements):
        # variable   <- string
        # initial    <- string
        # final      <- string
        # statements <- ListStatements
        self.variable   = variable
        self.initial    = initial
        self.final      = final
        self.statements = statements
        
    def append(self,inp):
        self.statements.append(inp)
    
    def showlist(self,nowrap=0,language="Cpp",indent=0):
        # -> [String]
        out=self.Cpp(nowrap,indent)
        return out

    def show(self,nowrap=0,language="Cpp",indent=0):
        # -> String
        import string
        aa=self.showlist(nowrap,language,indent)
        out=string.join(aa,"\n")
        return out

    def Cpp(self,nowrap=0,indent=0,defint=1):
        # -> [String, ]
        import string
        loopindent=1
        out=[]
        if self.variable:
            tmp="for ("
            if defint: tmp+="long "
            tmp+=self.variable+"="+self.initial+";"+self.variable+"<"+self.final+";++"+self.variable+") {"
            line=Statement(tmp)

            out+=line.showlist(nowrap  =nowrap,
                               language="Cpp",
                               indent  =indent)

            tmpindent=loopindent+indent
        else:
            tmpindent=indent

        out+=self.statements.showlist(nowrap  =nowrap,
                                      language="Cpp",
                                      indent  =tmpindent)
        if self.variable: 
            line=Statement("}")

            out+=line.showlist(nowrap  =nowrap,
                               language="Cpp",
                               indent  =indent)

        return out

        
class ConditionalBranch:
    def __init__(self,conditions,statements,isitelse=0):
        # conditions <- Conditions or str or Comparison(?)
        # statements <- ListStatements
        self.conditions = conditions
        self.statements = statements
        self.isitelse   = isitelse
        
    def append(self,inp):
        self.statements.append(inp)
    
    def showlist(self,nowrap=0,language="Cpp",indent=0):
        # -> [String]
        if language=="Cpp":
            out=self.Cpp(nowrap,indent)
        else:
            print "Not implemented"
        return out

    def show(self,nowrap=0,language="Cpp",indent=0):
        # -> String
        import string
        aa=self.showlist(nowrap,language,indent)
        out=string.join(aa,"\n")
        return out

    def Cpp(self,nowrap=0,indent=0):
        # -> [String, ]
        import string
        conditionindent=1
        #conditionindent=1

        out=[]

        if not (isinstance(self.conditions,Conditions) and (not self.conditions.condition)):
            if not self.isitelse: tmp="if "
            else:                 tmp="else if "
            if isinstance(self.conditions,Conditions):
                tmp+=self.conditions.show(language="Cpp")
            elif isinstance(self.conditions,Comparison):
                tmp+=self.conditions.show(language="Cpp")
            elif isinstance(self.conditions,str):
                tmp+=self.conditions
            else:
                print "type for ",self.conditions,"is not supported in CB"

            tmp+=" {"    
            line=Statement(tmp)

            out+=line.showlist(nowrap  =nowrap,
                               language="Cpp",
                               indent  =indent)

            tmpindent=conditionindent+indent
        else:
            tmpindent=+indent

        out+=self.statements.showlist(nowrap  =nowrap,
                                      language="Cpp",
                                      indent  =tmpindent)
        
        if not (isinstance(self.conditions,Conditions) and (not self.conditions.condition)):
            line=Statement("}")
            out+=line.showlist(nowrap  =nowrap,
                               language="Cpp",
                               indent  =indent)
        
        return out

        
class ListVariables:
    def __init__(self,listvariable=[]):
        # <- [Variables,,]
        self.listvariable=listvariable

    def append(self,other):
        import copy
        if isinstance(other,ListVariables):
            mylist=copy.deepcopy(self.listvariable)
            otherlist=copy.deepcopy(other.listvariable)
            outlist=mylist+otherlist
            self.listvariable=outlist
        else:
            self.listvariable.append(other)


    def simplify(self):
        import copy
        listtype=[]
        for xx in self.listvariable:
            if xx.type in listtype:
                continue
            else:
                listtype.append(xx.type)

        outlist=[]
        for ttype in listtype:
            tmp=""
            for xx in self.listvariable:
                if not xx.type==ttype:
                    continue

                if not tmp:
                    tmp=copy.deepcopy(xx)
                else:
                    tmp+=xx
            outlist.append(tmp)

        outlist2=[]
        for xx in outlist:
            outlist2.append(xx.simplify())
            
        return ListVariables(outlist2)    
            
    def showlist(self,language="Cpp"):
        out=[]
        for xx in self.listvariable:
            out+=xx.showlist(language=language)
        return out    

    def show(self,language="Cpp"):
        import string
        aa=self.showlist(language)
        out=string.join(aa,"\n")
        return out
        
class Variables:
    def __init__(self,variable=[]):
        self.variable = variable
        self.type     ="None"

    def __add__(self,other):
        import copy
        if not self.type==other.type:
            return copy.deepcopy(self)
        out=copy.deepcopy(self)
        out.variable+=copy.deepcopy(other.variable)
        return out

    def append(self,value):
        # <- str,or list
        if isinstance(value,list):
            self.variable+=value
        elif isinstance(value,str):
            self.variable.append(value)
        else:
            print "something is wrong"
            print value
        
    def hasthesametype(self,other):
        return self.type==other.type
        
    def show(self,language="Cpp"):
        import string
        aa=self.showlist(language)
        out=string.join(aa,"\n")
        return out
             
    def simplify(self):
        import copy
        mine=copy.deepcopy(self)
        myvariable=copy.deepcopy(mine.variable)
        out=[]
        while myvariable:
            target=myvariable.pop()
            if target in myvariable:
                continue
            out.append(target)
        out.reverse()    
        mine.variable=out
        return mine

    def showlist(self,language="Cpp"):
        return self.showline(language)

    def showline(self,valname="",language="Cpp"):
        out=[]
        if language=="Cpp":
            out=self.showlineCpp(valname=valname)
        return out    
    
    def showlineCpp(self,valname=""):
        baseindent  ="" 
        wrapedindent=""*(len(valname)+1)
        linefeed    =""
        wraplen     =500
        
        listshow=[]
        tmp=baseindent+valname+" "
        for xx in self.variable:
                
            if not wraplen or \
               len(tmp)+len(xx)+len(linefeed)+2<wraplen:
                tmp+=xx
                tmp+=","
            else:
                tmp+=linefeed
                listshow.append(tmp)
                tmp=wrapedindent
                tmp+=xx
                tmp+=","
        if tmp:
            tmp=tmp[:-1]
            listshow.append(tmp)
        return listshow
        
    
def str2Index(inpindex):
    import copy
    import re
    
    indx=copy.deepcopy(inpindex)

    if re.search(r'\+',indx):
        dagger=1
    else:
        dagger=0
    indx=re.sub(r'\+','',indx)    

    mm=re.search(r'\d+',indx)
    if mm:
        num=int(mm.group())
    else:
        print "Warning !! no index number"
    indx=re.sub(r'\d+','',indx)
    
    comp=""
    if indx=="g":
        type='general'
    elif indx=="p":
        type='particle'
    elif indx=="h":
        type='hole'
    elif indx=="P":
        type='particle'
        comp='complete'
    return Index(type,num,dagger,comp)

#def str2Tensorcontraction(nprint=0):
def str2TensorContraction(line="",nprint=0):
    import re
    import string
    import copy

    if not line:
        #line="- 1 / 2 P ( p4+ / p5+ p6+  ) P ( h1 h2 / h3  ) Sum ( h10 h11 p13 P12 ) v ( h10+ h11+ p13 P12  ) t ( p5+ p6+ p13+ h3 h10 h11  ) R ( p4+ P12+ h1 h2  ) "
        #line="- 1 / 2  Sum ( h10 h11 p13 P12 ) v ( h10+ h11+ p13 P12  ) t ( p5+ p6+ p13+ h3 h10 h11  ) R ( p4+ P12+ h1 h2  ) "
        #line="- 1 / 1 P ( p4+ p5+ / p6+  ) P ( h1 / h2 / h3  ) Sum ( h10 h11 p12 ) v ( h10+ h11+ h3 p12  ) R ( p4+ p5+ h1 h10  ) t ( p12+ h2  ) t ( p6+ h11  ) "
        line="- 1 / 1 P ( p4+ / p5+ p6+  ) P ( h1 h2 / h3  ) Sum ( h10 h11 P12 ) v ( h10+ h11+ h3 P12  ) R ( p4+ P12+ h1 h2  ) t ( p5+ h10  ) t ( p6+ h11  ) "
    if nprint:
        print "o Input line:"
        print line


    match_P=re.compile(r'P\s\(.*?\)')
    inp_P=match_P.findall(line)
    line=match_P.sub("",line)
    #print line

    match_Sum=re.compile(r'(S|s)um\s\(.*?\)')
    mm=match_Sum.search(line)
    inp_Sum=""
    if mm:
        inp_Sum=mm.group()
        line=match_Sum.sub("",line)

    match_tensor = re.compile(r'\S+?\s\(.*?\)')
    inp_tensors  = match_tensor.findall(line)
    inp_factor   = match_tensor.sub("",line)

    if nprint:
        print 
        print "o Input data"
        print "Factor:     ",inp_factor
        print "Permutation:",string.join(inp_P," , ")
        print "Summation:  ",inp_Sum
        print "Tensors:    ",string.join(inp_tensors," , ")

    # Sum
    #----
    tmp=inp_Sum
    tmp=re.sub(r'\('," ",tmp)
    tmp=re.sub(r'\)'," ",tmp)
    tmparray=tmp.split()
    out_Sum=[]
    for xx in tmparray[1:]:
        out_Sum.append(str2Index(xx))
    if nprint:
        print "\no Summation Indices"
        tmp=""
        for xx in out_Sum:
            tmp+=str(xx)
            tmp+=" , "
        tmp=tmp[:-3]
        print tmp
    
    
    # Factor
    #--------
    slash=re.compile(r'\/')
    tmp=slash.sub(" ",inp_factor)
    tmparray=tmp.split()
    out_Fraction=Fraction(int(tmparray[1]),int(tmparray[2]))

    tmpsign=tmparray[0]
    if tmpsign=="-":
        out_Sign=Sign(-1)
    elif tmpsign=="+":
        out_Sign=Sign(1)
    else:
        print "Warning Something is wrong!! in sign"
    out_Factor=Factor(out_Sign,out_Fraction)
    if nprint:
        print "\no Factor"
        print out_Factor
    
    # Permutation
    #-------------
    out_P=[]
    for xx in inp_P:
        tmp=xx
        tmp=re.sub(r'P\s\('," ",tmp)
        tmp=re.sub(r'\)'," ",tmp)
        tmparray=tmp.split("/")
        my_P=[]
        for yy in tmparray:
            tmpindices=yy.split()
            for ii in range(len(tmpindices)):
                myindex=str2Index(tmpindices[ii])
                tmpindices[ii]=myindex
            my_P.append(tmpindices)
        out_P.append(PrimitivePermutation(my_P))
    if nprint:
        print "\no Permutation"
        tmp=""
        for xx in out_P:
            tmp+=str(xx)
            tmp+=" , "
        tmp=tmp[:-3]
        print tmp

    #    
    # tensor
    #-------
    my_Tensors=[]
    for xx in inp_tensors:
        tmp=xx
        tmp=re.sub(r'\('," ",tmp)
        tmp=re.sub(r'\)'," ",tmp)
        tmparray=tmp.split()
        my_symbol=tmparray[0]
        list_Index=[]
        for yy in tmparray[1:]:
            my_Index=str2Index(yy)
            list_Index.append(my_Index)
        my_PTensor=PrimitiveTensor(copy.deepcopy(my_symbol),
                                   copy.deepcopy(list_Index))
        my_Tensors.append(my_PTensor)
    my_TS=PrimitiveTensorSequence(my_Tensors)
    if nprint:
        print "\no Tensors"
        print my_TS
    
    #my_TS = my_TS.relabel(1)
    #my_TS.analyze()
    new_TS=my_TS.analyze(nprint)
    #print new_TS.listindices().show(showcurly=0)
    #print new_TS.listindices()
    #print new_TS.listindices().showsumindices()
    #newli=new_TS.listindices()

    newout=new_TS.showsummedindices()

    pmytarget=[]
    for ii in newout.listindices:
        for jj in ii.indices:
            pmytarget.append(jj)
    mxx=new_TS.a2p_abb()
    for pxx in mxx:
        pxx.abb=copy.deepcopy(pxx.symbol)
        pxx.symbol=pxx.symbol.split("_")[0]
    new_TS=mxx.analyze(dorelabel=0)
    mxx=new_TS.a2p_abb()
#   if len(pmytarget)>0:
#       mxx=mxx.relabelnum(pmytarget)
    mxx=mxx.relabelnum(pmytarget)
    for pxx in mxx:
            pxx.abb=copy.deepcopy(pxx.symbol)
            pxx.symbol=pxx.symbol.split("_")[0]

    new_TS=mxx.analyze(dorelabel=0)

    newout=new_TS.showsummedindices()

    #print newout
    if nprint:
        print "\no Estimated Output Indices"
        print newout.show(showcurly=0)

    tarsymbol="O"
    tarabb   =tarsymbol+str(len(newout.a2list())/2)
    tarsymmetry=new_TS.totalsymmetry()
    newtarget=AnalyzedTensor(tarsymbol,newout,tarabb,tarsymmetry)
    if nprint:
        print "\no New Target"
        print newtarget

    # Summation
    #------------
    newsum=new_TS.showsumindices()
    if nprint:
        print "\no Estimated Summation"
        print newsum.sum_show()

    # Check the consistensy of generated Sum
    #tmp=newsum.a2list()
    tmp=newsum.a2p()
    ierror=0
    isequal=1
    if not len(tmp)==len(out_Sum):
        isequal=0
    else:
        tmp.sort()
        out_Sum.sort()
        for ii in range(len(tmp)):
            #print tmp[ii],out_Sum[ii]
            if not tmp[ii].isequalto(out_Sum[ii]):
                isequal=0
                break
#   if isequal:
#       if nprint:
#           print "Summation is correctly generated"
#   else:
#       ierror+=1
#       print "Warning generated Sum ",tmp[ii], \
#             " is not consistent with ",out_sum[ii]
        
    # Factor
    #--------
    if nprint:    
        print "\no Estimated Factor"
    newfraction=new_TS.estimatefraction(nprint)
    

    if nprint:
        print "\no Sign"
    newsign=new_TS.estimatesign(withprojection=1,nprint=nprint)

    # Total factor
    newfactor=Factor(newsign,newfraction)

    # Check the consistensy of generated Factor
    possiblerule10=0
    if newfactor==out_Factor:
        if nprint:
            print "Factor is correctly generated"
    else:
        ierror+=1
        print "Warning generated Factor ",newfactor, \
              " is not consistent with ",out_Factor
        possiblerule10=1
        
    # Permutation
    #-------------
    newpermutations=new_TS.estimatepermutation()
    if nprint:
        print "\no Permutations"
        print newpermutations
        
    # Check the consistensy of generated Permutation
    isequal=1
    tmp=newpermutations.turn2Primitive()
    if nprint:
        print "Number of Permutation : ",len(tmp)==len(out_P)
    for xx in tmp:
        if nprint:
            print "Generated Permutation ",xx," is in the Original Permutations?"
            print xx in out_P
        if not xx in out_P:
            isequal=0
            break
    if isequal:
        if nprint:
            print "Permutation is correctly generated"
    else:
        ierror+=1
        #print "Warning generated Permutation ",xx, \
        #      " is not contained in the original permutations."
        #if possiblerule10:
        #    print "rule10 possible"

            
    # TensorContraction
    #-------------------
    newTC=TensorContraction(newtarget,
                            newfactor,
                            newpermutations,
                            newsum,
                            new_TS)
    #print newsum.sum_show(restricted=1)
    #print newpermutations.show(restricted=1)
    #print "TS",new_TS.show(restricted=1)
    
    if ierror:
        tmp="Input    :  "+str(out_Factor)
        for xx in out_P:
            tmp+=str(xx)
        if out_Sum:
            tmp+=" Sum ( "
        for xx in out_Sum:
            tmp+=str(xx)
            tmp+=" "
        tmp=tmp[:-1]    
        if out_Sum:
            tmp+=" ) "
        tmp+=str(my_TS)
        print tmp
        print "Analyzed : ",newTC.show(showtarget=0)

    if nprint:
        print newTC
    
    #RnewTC=newTC.restrict()
    #print "restricted : ",RnewTC
    
    return newTC 
    
    #new_TS.estimatesign(withprojection=0,nprint=1)
    #projectionindices=newli.showsummedindices().transpose()
    #projectionindices.sort()
    #projection=AnalyzedTensor("",projectionindices)
    #print projection.show()
    #
    #
    #tmp_TS=AnalyzedTensorSequence([projection])+new_TS
    #nloop=tmp_TS.numberofloops(1)
    #nhole=new_TS.numberofholes(1)
    #print Sign((-1)**(nloop+nhole))

    
    #print new_TS.generateIndexpairs(1)
    #print tmp_TS.generateIndexpairs(1)
    #print tmp_TS.generateIndexpairs(0).findloops(1)
    
    
def factorial(n):
    out=1
    for ii in range(n):
        out*=(ii+1)
    return out

def PrimeFactor(n):
    out=[]
    for ii in range(n):
        if not n%(ii+1):
            out.append(ii+1)
    out.sort()
    out.reverse()
    return out

def GenerateOrdering(n):
    out_ordering=[]
    for jj in range(n):
        for ii in range(jj):
            #print ii,jj
            tmpordering=[]
            tmpordering=GeneratePermutation(n-2)
            element=[]
            for kk in range(n):
                if kk in [ii,jj]:
                    continue
                element.append(kk)
            if not tmpordering:
                out_ordering.append([ii,jj])
                continue
            for xx in tmpordering:
                ordering=[ii,jj]
                for kk in xx:
                    ordering.append(element[kk])
                #print ordering    
                out_ordering.append(ordering)
    return out_ordering            

def GeneratePermutation(n):
    import copy
    
    if n==1:
        return [[0]]
    element=range(n)
    
    out=[]
    for ii in range(len(element)):
        tmpelement=copy.deepcopy(element)
        pp=tmpelement.pop(ii)

        tmplower=GeneratePermutation(n-1)
        for xx in tmplower:
            tmp=[pp]
            for yy in xx:
                tmp.append(tmpelement[yy])
            if tmp:        
                out.append(tmp)
    return out    

def GenerateCombination(nn,ll):
    # -> [[integer,],]
    a=[]
    if (ll==1):
        for ii in range(nn):
            a.append([ii,])
    else:
        for ii in range(nn):
            b=GenerateCombination(ii,ll-1)

            for jj in range(len(b)):
                a.append(b[jj]+[ii,])
    return a

def maketable(numlist):
    import copy
    out=[]
    lenlist=len(numlist)
    maxint=2**lenlist-1
    for ii in range(1,maxint):
        tmplist=[]
        ix=copy.deepcopy(ii)
        cnt=0
        while 1:
            if ix%2: tmplist.append(numlist[cnt])
            if ix<2: break
            ix/=2
            cnt+=1
        out.append(copy.deepcopy(tmplist))
    return out

def GenPermutationwith(length,restrictions):
    # length        <- integer
    # restrictions  <- [[integer,],]

    #length=3
    #restrictions=[[0,1],[2]]

    # caribrate restrictions
    for res in restrictions:
        if min(res)>=0 and  \
           max(res)<length:
            continue
        print res,"is not in the range"

    Perm=GeneratePermutation(length)

    out=[]
    for aa in Perm:
        approved=1
        for res in restrictions:
            tmp=[]
            for xx in aa:
                if not xx in res:
                    continue
                tmp.append(xx)
            #print tmp    
            if not Samearray(tmp,res,nosort=1):
                approved=0
                break
        if approved:
            out.append(aa)
    return out        

#def Samearray(a1,a2):
#    #a1,a2 <- [String,]
#    import copy
#    if not len(a1)==len(a2):
#        return 0
#    tmp1=copy.deepcopy(a1)
#    tmp2=copy.deepcopy(a2)
#    tmp1.sort()
#    tmp2.sort()
#    for ii in range(len(tmp1)):
#        if tmp1[ii]==tmp2[ii]:
#            continue
#        return 0
#    return 1
def Samearray(a1,a2,nosort=0):
    #a1,a2 <- [Object,]
    # __eq__, and/or __cmp__, must be definded in Object
    import copy
    if not len(a1)==len(a2):
        return 0
    tmp1=copy.deepcopy(a1)
    tmp2=copy.deepcopy(a2)
    if not nosort:
        tmp1.sort()
        tmp2.sort()
    for ii in range(len(tmp1)):
        if tmp1[ii]==tmp2[ii]:
            continue
        return 0
    return 1

def Includearray(a1,a2,nosort=0):
    #a1,a2 <- [Object,]
    #a1 is included in a2
    # __eq__, and/or __cmp__, must be definded in Object
    import copy
    if len(a1)>len(a2):
        return 0
    tmp1=copy.deepcopy(a1)
    tmp2=copy.deepcopy(a2)
    if not nosort:
        tmp1.sort()
        tmp2.sort()
    for ii in range(len(tmp1)):
        exist=0
        for jj in range(len(tmp2)):
            if tmp1[ii]==tmp2[jj]:
                exist=1
                continue
        if not exist: 
            return 0
    return 1

def ListMultiplication(a1,a2):
    #a1,a2 <- []
    import copy
    out=[]
    for x1 in a1:
        for x2 in a2:
            out.append(x1+x2)
    return out        
    
def readfromfile(filename,debug=0):
    file=open(filename,"r")

    out=[]
    ii=0
    while 1:
        line=file.readline()

        if not line:
            break
    
        ii+=1
        print "o Term ",ii

        xx=str2TensorContraction(line,debug)
        print xx
        print 
        out.append(xx)
    ListTC=ListTensorContraction(out)
    ListTC.filename=filename

    return ListTC

