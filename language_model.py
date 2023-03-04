import re
from collections import Counter
import random
import sys

ORDER = int(sys.argv[1])
D = 0.75

def tokenisation(text,removepunc):
  split_text = re.split("\s",text)
  tokenised = []
  for word in split_text:
    if re.search(r"^#[\w\W]",word):
      tokenised.append("<HASHTAG>")
    elif re.search(r"^@[\w\W]",word):
      tokenised.append("<MENTION>")
    elif re.search(r"^http",word):
      tokenised.append("<URL>")
    elif re.search(r'^\d+%',word):
      tokenised.append("<PERCENTAGE>")
    elif re.search(r'^\d+',word):
      tokenised.append("<NUMEXP>")
    else:
      if(removepunc):
        new_word = re.sub(r"[^'\w]", "", word)
      else:
        new_word = re.sub(r'(\W)\1{1,}', r'\1', word)
      new_word_list = re.findall(r"\w+|\W",new_word)
      tokenised = tokenised + new_word_list

  return tokenised


def cleaned_output(text):
  text = re.sub(r"^#[\w\-\_]+|\s#[\w\-\_]+"," <HASHTAG>",text)
  text = re.sub(r"^@[\w\-\_]+|\s@[\w\-\_]+"," <MENTION>",text)
  text = re.sub(r"http[^\s]+","<URL>",text)
  text = re.sub(r"^\d+%|\s\d+%"," <PERCENTAGE>",text)
  text = re.sub(r"^\d+[^\s]*|\s\d+[^\s]*"," <NUMEXP>",text)
  text = re.sub(r'(\W)\1{1,}', r'\1', text)

  return text

# file = open("general-tweets.txt","r")
# text = file.read()
# print(cleaned_output(text))

file = open(sys.argv[3],"r")
textlist = file.readlines()

random.shuffle(textlist)
trainlist = textlist

tokenisedlist = []
for line in trainlist:
  addline = tokenisation(line.lower(),True)
  addline = ['<s>'] + addline + ['</s>']
  tokenisedlist.append(addline)

def createNgrams(splitlist,k):
  n_grams = []
  for n in range(0,k):
    n_grams.append(Counter())
  for n in range(0,k):
    for line in splitlist:
      for i in range(0,len(line)-n):
        n_grams[n][" ".join(line[i:i+1+n])] += 1
  return n_grams

def createContext(k,n_grams):
  context_n_grams = []
  next_n_grams = []
  for n in range(0,k-1):
    context_n_grams.append(Counter())
    next_n_grams.append(Counter())

  for n in range(0,k-1):
    for key in n_grams[n+1].keys():
      context_n_grams[n][" ".join(key.split()[1:])] += 1
      next_n_grams[n][" ".join(key.split()[:-1])] += 1

  return context_n_grams,next_n_grams


def calculate_pkn(n_grams,searchgram,k,context_n_grams,next_n_grams,SUM_N):
  count = 0
  prevcount = 0
  prevsearchgram = " ".join(searchgram.split()[:-1])
  nextsearchgram = " ".join(searchgram.split()[1:])
  if k == 1:
    count = 0
    if k == ORDER:
      return ((max(n_grams[k-1][searchgram]-D,0)/sum(n_grams[k-1].values())) + ( D / sum(n_grams[k-1].values()) ))

    count = context_n_grams[k-1][searchgram]
    return ((max(count-D,0)/SUM_N) + ( D / SUM_N))

  if(n_grams[k-1][searchgram] == 0):
    return calculate_pkn(n_grams,nextsearchgram,k-1,context_n_grams,next_n_grams,SUM_N)

 
  count = n_grams[k-1][searchgram]
  prevcount = n_grams[k-2][prevsearchgram]

  nextcount = next_n_grams[k-2][prevsearchgram]
  
  return ((max(count-D,0)/prevcount) + (( D * nextcount/ prevcount)*(calculate_pkn(n_grams,nextsearchgram,k-1,context_n_grams,next_n_grams,SUM_N))))
    

def KN_smoothing(trainset,k,testset):
  n_grams = createNgrams(trainset,k)
  context_n_grams,next_n_grams = createContext(k,n_grams)
  avg_perplexity = 0
  numberofsen = 0
  SUM_N = 0
  if k > 1:
    SUM_N = sum(n_grams[1].values())
  for testline in testset:
    line = testline.lower()
    line = tokenisation(line,True)
    if len(line) == 0:
      line = ["."]
    newline = ["<s>"] + line + ["</s>"]
    perp_score = 1
    prob_count = 0
    for i in range(0,len(newline)-k + 1):
      searchgram = " ".join(newline[i:i+k])
      probability = calculate_pkn(n_grams,searchgram,k,context_n_grams,next_n_grams,SUM_N)
      perp_score = perp_score * probability
      prob_count += 1
    for i in range(2,k):
      searchgram = " ".join(newline[0:i])
      ngramorder = i
      probability = calculate_pkn(n_grams,searchgram,ngramorder,context_n_grams,next_n_grams,SUM_N)
      perp_score = perp_score * probability
      prob_count += 1
    
    print(perp_score)
    avg_perplexity += perp_score
    numberofsen += 1

    
def createNextgrams(k,n_grams):
  next_n_grams = []
  for n in range(0,k-1):
    next_n_grams.append(Counter())

  for n in range(0,k-1):
    for key in n_grams[n+1].keys():
      next_n_grams[n][" ".join(key.split()[:-1])] += 1
        

  return next_n_grams


def calculate_pwn(n_grams,searchgram,k,next_n_grams,abs_bigrams):

  prevsearchgram = " ".join(searchgram.split()[:-1])
  nextsearchgram = " ".join(searchgram.split()[1:])
  count = n_grams[k-1][searchgram]
  prevcount = n_grams[k-2][prevsearchgram]

  if k == 1:
    return ((n_grams[0][searchgram] + 1)/(len(n_grams[0].keys()) + sum(n_grams[0].values())))
  if k == 2:
    if prevcount == 0:
      return ((n_grams[0][nextsearchgram] + 1)/(len(n_grams[0].keys()) + sum(n_grams[0].values())))
    elif count == 0:
      return ((n_grams[0][prevsearchgram])/(abs_bigrams[prevsearchgram]*(prevcount + n_grams[0][prevsearchgram])))
    else:
      return (count/(prevcount + n_grams[0][prevsearchgram]))

  if prevcount == 0:
    return calculate_pwn(n_grams,nextsearchgram,k-1,next_n_grams,abs_bigrams)

  nextcount = next_n_grams[k-2][prevsearchgram]
  return ( (count + (nextcount * calculate_pwn(n_grams,nextsearchgram,k-1,next_n_grams,abs_bigrams))) / (prevcount + nextcount))

def create_abs_bigrams(test_n_grams,n_grams):
  abs_bigrams = Counter()
  for gram in test_n_grams[1].keys():
    if n_grams[1][gram] == 0:
      abs_bigrams[(gram.split())[0]] += test_n_grams[1][gram]

  return abs_bigrams
  
def WB_smoothing(trainset,k,testset):
  n_grams = createNgrams(trainset,k)
  next_n_grams = createNextgrams(k,n_grams)

  tokenisedtestlist = []
  for newline in testset:
    addline = tokenisation(newline.lower(),True)
    if len(addline) == 0:
      addline = ["."]
    addline = ['<s>'] + addline + ['</s>']
    tokenisedtestlist.append(addline)

  test_n_grams = createNgrams(tokenisedtestlist,2)
  abs_bigrams = ""
  if k > 1:
    abs_bigrams = create_abs_bigrams(test_n_grams,n_grams)

  avg_perplexity = 0
  numberofsen = 0

  for testline in testset:
    line = testline.lower()
    line = tokenisation(line,True)
    newline = ["<s>"] + line + ["</s>"]
    perp_score = 1
    num_prob = 0
    for i in range(0,len(newline)-k + 1):
      searchgram = " ".join(newline[i:i+k])
      probability = calculate_pwn(n_grams,searchgram,k,next_n_grams,abs_bigrams)
      perp_score = perp_score * probability
      num_prob += 1
    for i in range(2,k):
      searchgram = " ".join(newline[0:i])
      probability = calculate_pwn(n_grams,searchgram,i,next_n_grams,abs_bigrams)
      perp_score = perp_score * probability
      num_prob += 1
    
    print(perp_score)
    avg_perplexity += perp_score
    numberofsen += 1


if(sys.argv[2] == 'k'):
  testlist = input("input sentence: ")
  testlist = [testlist]
  KN_smoothing(tokenisedlist,ORDER,testlist)
elif(sys.argv[2] == 'w'):
  testlist = input("input sentence: ")
  testlist = [testlist]
  WB_smoothing(tokenisedlist,ORDER,testlist)
else:
  print("invalid")



