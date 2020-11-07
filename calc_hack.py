import sys
import random
import re
texfile=sys.argv[1]
xmlfile=(texfile.split('.'))[0]+'-moodle.xml'
outputfile=(texfile.split('.'))[0]+'-moodle-calc.xml'


def findcalculated(file_name):
    with open(file_name, "r") as a_file:
      count=0
      calculated=[]
      digitsdic={}
      p=0
      digits=0
      for draftline in a_file:
        line = draftline.strip().replace(" ","")
        if line[0:13]=="\\begin{multi}" or line[0:17]=="\\begin{numerical}":
            count=count+1
        if digits==1:
            dig=line.rstrip('\\')
            digitsdic[count]=eval(dig)
            digits=0

        if line[0:6]=='digits':
            p=0
            digits=1
        if p==1:
            u=line.split(':',1)
            var=u[0]
            vals=u[1].rstrip('\\').rstrip(',')
            if vals[0]=="r":
                seq=''
                L=eval(vals)
                for i in L:
                    seq=seq+','+ str(i)
                vals=seq.lstrip(',')
            calculated.append([count,[var,set(eval('['+ vals+']'))]])
        if line[0:6]=='params':
            p=1
    indices=[]

    for item in calculated:
        indices.append(item[0])
    indices=list(set(indices))
    dict={}
    for index in indices:
        L=[]
        for elems in calculated:
            if elems[0]==index:
                L.append(elems[1])
        dict[index]=L
    return [dict,digitsdic]

def preparetolerance(dig):
     return '<tolerance>'+str(pow(10,-dig))+'</tolerance>\n'+\
    '<tolerancetype>1</tolerancetype>\n<correctanswerformat>1</correctanswerformat>\n'+\
    '<correctanswerlength>'+str(dig)+'</correctanswerlength>\n'


def preparedataset(varname,s,size):
    string='<dataset_definition>\n\
      <status><text>private</text>\n\
    </status>\n\
      <name><text>'+varname+'</text>\n\
    </name>\n\
      <type>calculatedsimple</type>\n\
      <distribution><text>uniform</text>\n\
    </distribution>\n\
      <minimum><text>'+str(min(s))+'</text>\n\
    </minimum>\n\
      <maximum><text>'+str(max(s))+'</text>\n\
    </maximum>\n\
      <decimals><text>0</text>\n\
    </decimals>\n\
    <itemcount>'+str(size)+'</itemcount>\n\
    <dataset_items>\n'
    for i in range(size):
        v=(random.sample(s,1))[0]
        string=string+\
          '<dataset_item>\n\
             <number>'+str(i+1)+'</number>\n\
             <value>'+str(v)+'</value>\n\
          </dataset_item>\n'
    string=string+'</dataset_items>\n\
    </dataset_definition>\n'

    return string

def preparedatasets(L):
    string='<dataset_definitions>\n'
    for item in L:
        string=string+preparedataset(item[0],item[1],100)
    string=string+'</dataset_definitions>\n'
    return string


##exercises gets the exercises text in a list
def exercises(tex_file):
    file=open(tex_file)
    text=file.read()
    file.close()
    p1=re.compile('\\\\begin{numerical}|\\\\begin{multi}')
    list1=p1.split(text)
    list1=list1[1:len(list1)]
    p2=re.compile('\\\\end{numerical}|\\\\end{multi}')
    list2=[]
    for item in list1:
        aux=p2.split(item)
        list2.append(aux[0])
    return list2
##the following function "answers" reads the answers to the various questions and puts them in
## a list of formatted answers, ready to be copied in the xml file.

def answers(exercise):
    p=re.compile('\\\\item')
    list=p.split(exercise)
    question=list[0]
    r=[]
    for a in list[1:len(list)]:
        r.append('<text><![CDATA[<p>'+a.lstrip('\*| ').replace('\n','')+'</p>]]></text>')
    return r

def newxml(dict,digitsdic,inputxml,inputtex,output_name):
    ex=exercises(inputtex)
    f=open(output_name,"w")
    with open(inputxml, "r") as a_file:
        count=0## counts the exercise number
        acount=0##acount will be 1 if we are writing an answer to a calc question
        rcount=0 ##will count the answer's number (r for response)
        indices=list(dict.keys())
        for draftline in a_file:
            line = draftline.strip()
            #print(line)
            if line=="<question type=\"multichoice\">":
                count=count+1
            if line=="<question type=\"numerical\">":
                count=count+1
            if line=="<question type=\"multichoice\">" and count in indices:
                f.write("<question type=\"calculatedmulti\">\n")
            elif line=="<question type=\"numerical\">" and count in indices:
                f.write("<question type=\"calculatedsimple\">\n")

            elif line=="</answer>" and count in indices:
                dig=digitsdic[count]
                f.write(preparetolerance(dig))
                f.write("</answer>\n")
            elif line=="</question>" and count in indices:
                rcount=0
                f.write(preparedatasets(dict[count]))
                f.write('</question>\n')
            elif acount==1 and line[0:5]=='<text':
                #f.write(line.replace('<p>','').replace('</p>','')+'\n')
                exo=ex[count-1]
                f.write(answers(exo)[rcount-1].replace('<p>','').replace('</p>','')+'\n')
            else:
                 f.write(line+'\n')

            if count in indices and line[0:8]in ['<answer ','<answer>'] :
                rcount=rcount+1
                acount=1
            if count in indices and line[0:7]=='</answe':
                acount=0

    f.close()

def fixmoodleset(filename):
    p=re.compile('\\\\moodleset \{[^}]*\}[^}]*\}')
    with open(filename, 'r') as file:
        file_as_string= file.read()
        new_string=re.sub(p,'',file_as_string)
    with open(filename, "w") as a_file:
        a_file.write(new_string)



#exo=exercises(texfile)[0]
#print(answers(exo))
u=findcalculated(texfile)
newxml(u[0],u[1],xmlfile,texfile,outputfile)
fixmoodleset(outputfile)
