# 암호해제 App (무차별대입공격)
import itertools
import time
import zipfile

passwd_string = '0123456789'        # 패스워드에 영문자도 들어있으면
# passwd_string = '0123456789abcdefghijklmn...xyzABCDEF...XYZ'

file = zipfile.ZipFile('./studyPython/password.zip')
isFind = False  # 암호를 찾았는지

for i in range(4, 5):       # 4자리 (0000~9999) : (4, 5)
    attempts = itertools.product(passwd_string, repeat = i)
    for attempt in attempts:
        try_pass = ''.join(attempt)
        print(try_pass)
        # time.sleep(0.1)

        try:
            file.extractall(pwd=try_pass.encode(encoding='utf-8'))
            print(f'암호는 {try_pass}입니다')
            isFind = True; break
                            
        except:
            pass
    
    if isFind == True: break