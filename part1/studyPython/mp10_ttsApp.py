# TTS (Text To Speech)
# pip install gTTS
# pip install playsound
from gtts import gTTS
from playsound import playsound

text = '안녕하세요, 이재욱입니다.'

tts = gTTS(text=text, lang='ko', slow = False)
tts.save('./studyPython/output/hi.mp3')
print('생성 완료')

# text ="Hi, everybody. Playing with Python is fun!!!"
# tts = gTTS(text=text, lang='en')
# tts.save("./studyPython/output/helloEN.mp3")


playsound('./studyPython/output/hi.mp3')
print('음성출력 완료')
