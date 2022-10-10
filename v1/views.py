# Import internal function from django
from django.shortcuts import render

# Import depedencies from external library
from ninja import NinjaAPI, Form
from pydantic import ConfigError
from pytube import YouTube as yt

# Import modules from app files
# from v1.schema import ErrorSchema //Unused//

# Create your views here.
app = NinjaAPI(title="Pytube Youtube Downloader API", version=0.1)

@app.post('audio-only',tags=['For Audio Only'])
def audio_only(request, link: str = Form(...)):
  try:
    url = link
    yu = yt(url)
    name = "&title="+yu.title.replace(" ","").replace(",","").replace("''","")
    res = []
    [res.append(i) for i in yu.streams.filter(only_audio=True)]
    if None in res:
      return {
        "success":True,
        "status_code":200,
        "message":"success",
        "title":yu.title,
        "result":{
          "m4A":res[3].url+name,
          "mp3":res[4].url+name
        }
      }
    else:
      return {
        "success":True,
        "status_code":200,
        "message":"success",
        "title":yu.title,
        "result":{
            "m4A":res[2].url+name,
            "m4B":res[3].url+name,
            "mp3":res[4].url+name
          }
      }
  except Exception as E:
    return {
      "success":False,
      "message":"link undefined",
      "error":str(E),
      "inLine":E.__traceback__.tb_lineno
    }

@app.post('video-with-audio', tags=['For Video Downloader'])
def video_with_audio(request, link:str = Form(...)):
    try:
        url = link
        yu = yt(url)
        res=[]
        name = yu.title.replace(" ", "").replace(",","").replace("'","")
        [res.append(i) for i in yu.streams.filter(progressive=True)]
        print(len(res))
        if len(res) == 2:
            return {
                "success":True,
                "title":name,
                "message":"success",
                "result": {
                            "144p":res[0].url+"&title="+name,
                            "360p":res[1].url+"&title="+name
                          }
                        }
        else:
            return {
                "success":True,
                "title":name,
                "message":"success",
                "result":{
                    "114p":res[0].url+"&title="+name,
                    "360p":res[1].url+"&title="+name,
                    "720p":res[2].url+"&title="+name
                }
            }
    except Exception as E:
        return {
            "success":False,
            "message":"link-undefined",
            "error":str(E),
            "inLine":E.__traceback__.tb_lineno
            }
