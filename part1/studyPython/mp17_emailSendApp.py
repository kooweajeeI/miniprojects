# 이메일 보내기 앱
import smtplib  # 메일전송프로토콜
from email.mime.text import MIMEText

send_email = 'rndhk0123210@naver.com'
send_pass = '123123'        # 비밀번호 입력

recv_email = 'leejw2873@naver.com'

smtp_name = 'smtp.naver.com'
smtp_port = 587

text = '''메일 내용입니다. 긴급입니다. 
조심하세요~ 빨리 연락주세요'''

msg = MIMEText(text)
msg['Subject'] = '메일 제목입니다'
msg['From'] = send_email        # 보내는 메일
msg['To'] = recv_email          # 받는 메일

print(msg.as_string())

mail = smtplib.SMTP(smtp_name, smtp_port)   # SMTP 객체 생성
mail.starttls() # 전송계층보안 시작
mail.login(send_email, send_pass)
mail.sendmail(send_email, recv_email, msg=msg.as_string())
mail.quit()
print('전송완료')