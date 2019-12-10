
# 一. 基于 TextRank 算法的关键词抽取
***
### jieba.analyse.textrank(sentence, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v')) 直接使用，接口相同，注意默认过滤词性。
+ topK 为返回多少rank最大的关键词
+ withWeight 为是否返回关键词rank值，默认值为 False
+ allowPOS 仅包括指定词性的词，默认值为空
### jieba.analyse.TextRank() 新建自定义 TextRank 实例

## 基本思想:
#### 将待抽取关键词的文本进行分词
#### 以固定窗口大小(默认为5，通过span属性调整)，词之间的共现关系，构建图
#### 计算图中节点的 PageRank，注意是无向带权图

***
+ TextRank
+ PageRank

## PageRank算法
### https://blog.csdn.net/leadai/article/details/81230557
### PageRank是一种由搜索引擎根据网页之间相互的超链接计算的技术
### 核心
+ 如果一个网页被很多其他网页链接到的话，说明这个网页比较重要，PageRank值相对较高
+ 如果一个PageRank值很高的网页链接到一个其他的网页，那么被链接到的网页的PageRank值会相应地提高


## TextRank算法
### https://www.cnblogs.com/en-heng/p/6626210.html
### 原理

+ 如果一个单词出现在很多单词后面的话，那么说明这个单词比较重要
+ 一个TextRank值很高的单词后面跟着的一个单词，那么这个单词的TextRank值会相应地提高

### 共现关系
#### 例：分词结果a/b/c，b/a/f，a/d/c，那么就是ab共现2次，ac共现2次，以此类推。
### Jieba分词中的TextRank：
+ 对每个句子进行分词和词性标注处理
+ 过滤掉除指定词性外的其他单词、停用词、长度小于2的单词
+ 将剩下的单词中循环选择一个单词，将其与其后面4个单词分别组合成4条边。

#### 例1： ['有','媒体', '曝光','高圆圆', '和', '赵又廷','现身', '台北', '桃园','机场','的', '照片']
#### 对于‘媒体‘这个单词，就有（'媒体', '曝光'）、（'媒体', '圆'）、（'媒体', '和'）、（'媒体', '赵又廷'）4条边，且每条边权值为1，当这条边在之后再次出现时，权值再在基础上加1.
#### 例2：

![image.png](attachment:image.png)

#### 例3：宁波有什么特产能在上海世博会占有一席之地呢？
{宁波　特产　上海　世博会　占有　一席之地}，如图
![image.png](attachment:image.png)


```python
#encoding=utf-8
from __future__ import unicode_literals
import sys
sys.path.append("../")

import jieba
import jieba.posseg
import jieba.analyse

print('='*40)
print('关键词提取')

s = "此外，公司拟对全资子公司吉林欧亚置业有限公司增资4.3亿元，增资后，吉林欧亚置业注册资本由7000万元增加到5亿元。吉林欧亚置业主要经营范围为房地产开发及百货零售等业务。目前在建吉林欧亚城市商业综合体项目。2013年，实现营业收入0万元，实现净利润-139.13万元。"


print('-'*40)
print(' TextRank算法')
print('-'*40)

for x, w in jieba.analyse.textrank(s, withWeight=True):
    print('%s %s' % (x, w))

```

    ========================================
    关键词提取
    ----------------------------------------
     TextRank算法
    ----------------------------------------
    吉林 1.0
    欧亚 0.9966893354178172
    置业 0.6434360313092776
    实现 0.5898606692859626
    收入 0.43677859947991454
    增资 0.4099900531283276
    子公司 0.35678295947672795
    城市 0.34971383667403655
    商业 0.34817220716026936
    业务 0.3092230992619838
    在建 0.3077929164033088
    营业 0.3035777049319588
    全资 0.303540981053475
    综合体 0.29580869172394825
    注册资本 0.29000519464085045
    有限公司 0.2807830798576574
    零售 0.27883620861218145
    百货 0.2781657628445476
    开发 0.2693488779295851
    经营范围 0.2642762173558316
    

### jieba自定义的TextRank

####  1. defaultdict
+ defaultdict(function_factory)构建的是一个类似dictionary的对象，其中keys的值，自行确定赋值，但是values的类型，是function_factory的类实例，而且具有默认值。
+ 比如default(int)则创建一个类似dictionary对象，里面任何的values都是int的实例，而且就算是一个不存在的key, d[key] 也有一个默认值，这个默认值是int()的默认值0。

#### 2. enumerate() 
+ 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。

#### 3. frozenset() 
+ 返回一个冻结的集合，冻结后集合不能再添加或删除任何元素。


```python
from __future__ import absolute_import, unicode_literals
import sys
from operator import itemgetter
from collections import defaultdict
import jieba.posseg
import jieba.analyse
from jieba.analyse.tfidf import KeywordExtractor
from jieba._compat import *

class UndirectWeightedGraph:#定义无向图
    d = 0.85

    def __init__(self):
        self.graph = defaultdict(list)

    def addEdge(self, start, end, weight):#起点词，终点，权重（共现次数）
        # use a tuple (start, end, weight) instead of a Edge object
        self.graph[start].append((start, end, weight))
        self.graph[end].append((end, start, weight))

    def rank(self):
        ws = defaultdict(float)
        outSum = defaultdict(float)

        wsdef = 1.0 / (len(self.graph) or 1.0)
        for n, out in self.graph.items():
            ws[n] = wsdef
            outSum[n] = sum((e[2] for e in out), 0.0)

        # this line for build stable iteration
        sorted_keys = sorted(self.graph.keys())
        for x in xrange(10):  # 10 iters
            for n in sorted_keys:
                s = 0
                for e in self.graph[n]:
                    s += e[2] / outSum[e[1]] * ws[e[1]]
                ws[n] = (1 - self.d) + self.d * s

        (min_rank, max_rank) = (sys.float_info[0], sys.float_info[3])

        for w in itervalues(ws):
            if w < min_rank:
                min_rank = w
            if w > max_rank:
                max_rank = w

        for n, w in ws.items():
            # to unify the weights, don't *100.
            ws[n] = (w - min_rank / 10.0) / (max_rank - min_rank / 10.0)

        return ws


class TextRank(KeywordExtractor):

    def __init__(self):
        self.tokenizer = self.postokenizer = jieba.posseg.dt#词性标注分词
        self.stop_words = self.STOP_WORDS.copy()#停用词
        self.pos_filt = frozenset(('ns', 'n', 'vn', 'v'))#仅包括这四类词性
        self.span = 5 #窗口大小

    def pairfilter(self, wp):
        return (wp.flag in self.pos_filt and len(wp.word.strip()) >= 2  #判断词的词性是否符合及长度是否>2，
                and wp.word.lower() not in self.stop_words)#判断词的全小写格式是否在停用词表

    def textrank(self, sentence, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'), withFlag=False):
        """
        Extract keywords from sentence using TextRank algorithm.
        Parameter:
            - topK: return how many top keywords. `None` for all possible words.
            - withWeight: if True, return a list of (word, weight);
                          if False, return a list of words.
            - allowPOS: the allowed POS list eg. ['ns', 'n', 'vn', 'v'].
                        if the POS of w is not in this list, it will be filtered.
            - withFlag: if True, return a list of pair(word, weight) like posseg.cut
                        if False, return a list of words
        """
        
        self.pos_filt = frozenset(allowPOS)#停用词表
        g = UndirectWeightedGraph()# 定义无向有权图      
        cm = defaultdict(int)#创建一个共现词典 #创建一个dict，value都为int型，默认值为0
        words = tuple(self.tokenizer.cut(sentence))#对内容分词
        
        # 依次遍历词
        for i, wp in enumerate(words):
            if self.pairfilter(wp): # 是否满足过滤条件
                for j in xrange(i + 1, i + self.span):#self.span=5
                    if j >= len(words):
                        break
                    if not self.pairfilter(words[j]):#不满足跳过该词
                        continue
                    # 词i，j为key，出现次数value，添加到共现词典cm中，每共现一次value+1
                    
                    if allowPOS and withFlag: #withFlag=False仅返回词,True返回（词，权值）对
                        cm[(wp, words[j])] += 1
                    else:
                        cm[(wp.word, words[j].word)] += 1

        # 遍历共现词典的元素，将词i，词j作为一条边起点和终点，共现次数边的权重
        for terms, w in cm.items():
            g.addEdge(terms[0], terms[1], w)
        nodes_rank = g.rank()
        
        # 排序
        if withWeight:#True返回（词，权重）列表
            tags = sorted(nodes_rank.items(), key=itemgetter(1), reverse=True)
        else:#False返回词表
            tags = sorted(nodes_rank, key=nodes_rank.__getitem__, reverse=True)

        if topK:
            return tags[:topK]
        else:
            return tags

    extract_tags = textrank
```


```python
#停用词表 例：
STOP_WORDS = frozenset(('a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'can',
                        'for', 'from', 'have', 'if', 'in', 'is', 'it', 'may',
                        'not', 'of', 'on', 'or', 'tbd', 'that', 'the', 'this',
                        'to', 'us', 'we', 'when', 'will', 'with', 'yet',
                        'you', 'your', '的', '了', '和'))

```

***
***
***
# 二. 词性标注
***
### jieba.posseg.POSTokenizer(tokenizer=None) 新建自定义分词器，tokenizer 参数可指定内部使用的 jieba.Tokenizer 分词器。jieba.posseg.dt 为默认词性标注分词器。
### 标注句子分词后每个词的词性，采用和 ictclas 兼容的标记法。


```python
print('='*40)
print('词性标注')
print('-'*40)

words = jieba.posseg.cut("我爱北京天安门")
for word, flag in words:
    print('%s %s' % (word, flag))

print('='*40)
print('Tokenize: 返回词语在原文的起止位置')
print('-'*40)
print(' 默认模式')
print('-'*40)

result = jieba.tokenize('永和服装饰品有限公司')
for tk in result:
    print("word %s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))

print('-'*40)
print(' 搜索模式')
print('-'*40)

result = jieba.tokenize('永和服装饰品有限公司', mode='search')
for tk in result:
    print("word %s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))
```

    ========================================
    词性标注
    ----------------------------------------
    我 r
    爱 v
    北京 ns
    天安门 ns
    ========================================
    Tokenize: 返回词语在原文的起止位置
    ----------------------------------------
     默认模式
    ----------------------------------------
    word 永和		 start: 0 		 end:2
    word 服装		 start: 2 		 end:4
    word 饰品		 start: 4 		 end:6
    word 有限公司		 start: 6 		 end:10
    ----------------------------------------
     搜索模式
    ----------------------------------------
    word 永和		 start: 0 		 end:2
    word 服装		 start: 2 		 end:4
    word 饰品		 start: 4 		 end:6
    word 有限		 start: 6 		 end:8
    word 公司		 start: 8 		 end:10
    word 有限公司		 start: 6 		 end:10
    

# 三. 问题
+ 定义的rank函数没太看懂
+ 窗口
+ 不懂算法的数学公式，影响读jieba自定义的TextRank实例
