# celery_chain
用celery实现任务链 celery chain

## 需求
在我的工作中，我们把celery分为了4种不同的任务。但是4种不同的任务又需要有一定的调用顺序。   
比如，A任务跑完以后，需要带着A任务的结果去跑B任务。 B任务完成以后，需要带着结果去跑C任务。   
这样一来，我们发现了celery chain

### 代码讲解
tasks.py  

@app.task(name='tasks.add')   
def add(x, y):  
    return x + y   
  
  
@app.task(name='mul.add')  
def mul(x, y):  
    print "x: ",x  
    print "y: ",y  
    return x * y  

@app.task(name='reabc.add')  
def reabc(x, y):  
    return x - y  
      
在tasks代码中，定义三个任务。 tasks.add为加法，mul.add为乘法，reabc.add为减法  


testcelery.py  
#### 导入add,mul,reabc的task
from tasks.tasks import add,mul,reabc  
#### 导入chain包
from celery import chain 
#### 往chain里面传入tasks方法
#### 例子中的任务链是 (2+2)*16-1
res = chain(add.s(2,2),mul.s(16),reabc.s(1))()   
#### 打印结果
print res.get()  


### 启动
tasks.py  
celery -A tasks worker --loglevel=info

我们来看log:
[2018-04-27 08:14:13,341: INFO/MainProcess] Received task: tasks.add[b4c802e7-4016-44f7-bc6f-ffe5a1b1662b]  
[2018-04-27 08:14:13,358: INFO/MainProcess] Received task: mul.add[7eaf1700-10ed-43a2-8494-56c557ce8f89]  
#### add的task完成了 加法操作 结果是 4
[2018-04-27 08:14:13,359: INFO/MainProcess] Task tasks.add[b4c802e7-4016-44f7-bc6f-ffe5a1b1662b] succeeded in 0.0165406509986s: 4   
#### 传入mul乘法操作，我输出了参数，可以看到 x=4 来源于 add的结果
[2018-04-27 08:14:13,360: WARNING/Worker-1] x:  
[2018-04-27 08:14:13,361: WARNING/Worker-1] 4  
[2018-04-27 08:14:13,361: WARNING/Worker-1] y:  
[2018-04-27 08:14:13,361: WARNING/Worker-1] 16  
[2018-04-27 08:14:13,376: INFO/MainProcess] Received task: reabc.add[3f1a7c58-cc6d-4465-a1fd-96d52ec9df0b]  
[2018-04-27 08:14:13,376: INFO/MainProcess] Task mul.add[7eaf1700-10ed-43a2-8494-56c557ce8f89] succeeded in 0.0169673810015s: 64  
#### 减法操作的 x是来源于 mul的结果
[2018-04-27 08:14:13,380: INFO/MainProcess] Task reabc.add[3f1a7c58-cc6d-4465-a1fd-96d52ec9df0b] succeeded in 0.00270992800142s: 63  
