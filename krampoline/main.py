import uvicorn
from fastapi import FastAPI, APIRouter
import time
import datetime # datetime 라이브러리 import
from pathlib import Path
import json
import subprocess
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas_datareader as pdr
import pandas as pd
from json import loads, dumps

prefix_router = APIRouter(prefix="/k4facd99def2ba")



app = FastAPI(
    docs_url=None, # Disable docs (Swagger UI)
    redoc_url=None, # Disable redoc
)




app.mount("/templates/forder1", StaticFiles(directory="templates/forder1"), name="forder1")
templates = Jinja2Templates(directory="templates/forder1")


from multiprocessing import Process, Queue

def work(id, start, end, result):
    total = 0
    for i in range(start, end):
        print( id, i )
        total += i
    
    result.put(total)
    return

def test_process():
    START, END = 0, 1000
    result = Queue()
    th1 = Process(target=work, args=(1, START, END, result))
    th2 = Process(target=work, args=(2, START, END, result))
    th3 = Process(target=work, args=(3, START, END, result))
    
    th1.start()
    th2.start()
    th3.start()
    th1.join()
    th2.join()
    th3.join()

    result.put('STOP')
    total = 0
    while True:
        tmp = result.get()
        if tmp == 'STOP':
            break
        else:
            total += tmp
    print(f"Result: {total}")


def checkTime():
    start = time.time()
    time.sleep(1) # 수행시간 측정하고자 하는 코드 부분
    sec = time.time()-start # 종료 - 시작 (걸린 시간)

    times = str(datetime.timedelta(seconds=sec)) # 걸린시간 보기좋게 바꾸기
    short = times.split(".")[0] # 초 단위 까지만
    return times


@app.on_event("startup")
async def startup_event() :
    '''on_event로 지정하면 request 올 때마다 해당 함수를 실행시킬 수 있다'''
    #https://hbase.tistory.com/341 subprocess 정보
    with subprocess.Popen(["ls", "-al"], stdout=subprocess.PIPE) as proc:
        print(proc.stdout.read().decode("utf-8"))   

from fastapi import Response
import json




#https://wendys.tistory.com/174
@prefix_router.get("/")
#async def root():
async def read_item(request: Request):
    r = dict( request )
    # print(r)
    # for a in r:
    #     print( "------------------------------------------" )
    #     print( r )
    #     print( r[ a ] )
    # test_process()
    #a = pdr.get_data_fred('GS10')
    a = pdr.DataReader('105840', 'naver', start="20230301", end="20230401")
    b = a.to_dict()
    print( b )
    
    #result = a.to_json(orient="split")
    #parsed = loads(result)
    #b = dumps(parsed, indent=4)  
    #print(b)
    #json_str = json.dumps(a, indent=4, default=str)
    #return Response(content=json_str, media_type='application/json')  
    df = pd.DataFrame(a)
    return templates.TemplateResponse("index.html", {"request": r, "time": df.to_html(classes='ui compact table celled')})
    #return {"message": "Hello World", "time" : checkTime()}

#https://psystat.tistory.com/151
#pandas_datareader
@prefix_router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# Now add the router to the app
app.include_router(prefix_router)

#uvicorn main:app --reload --host=0.0.0.0 --port=3000
if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=3000, reload=True, access_log=True, log_config="log.yaml", reload_excludes="api.log" )
    #uvicorn.run('main:app', host="0.0.0.0", port=3000, reload=True, access_log=True )