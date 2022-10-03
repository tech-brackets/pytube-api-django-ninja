from django.shortcuts import render

from ninja import NinjaAPI
from pydantic import ConfigError

from pytube import YouTube as yt
from v1.schema import ErrorSchema
# Create your views here.

app = NinjaAPI(title="Pytube API", version=1)

@app.get('audio-only',)
def audio_only(request, link):
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
        "audio-only":{
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
        "audio-only":{
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
