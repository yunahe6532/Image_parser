# -*- coding: utf-8 -*-
import struct

Header = { #이미지 시그니처 해더 저장용 디렉터리
    0xFFD8FFE0: "JPG",
    0x89504E47: "PNG",
    0x47494638: "GIF",
}
Footer = {
    0xFFD9: "JPG",
    0x4945: "PNG",
    0x003B: "GIF",
}
reverse_H = {
    "JPG": "FFD8FFE0",
    "PNG": "89504E47",
    "GIF": "47494638",   
}
reverse_F ={
    "JPG": "FFD9",
    "PNG": "4945",
    "GIF": "003B",     
}

def SzieCalc(num): #파일 크기 변환 함수
    str_size = ['B', 'KB', 'MB', 'GB']
    t = size = (num)
    for i in range(4):
        t = t / 1024
        if int(t) > 0:
            size = size / 1024
        else:
            break
    return ('%.2f %s' % (size, str_size[i]))

def File_info(part): # 파일 정보 출력 함수
    for i in range (len(part)):
        print("<----------------Img File Information %d ------------------->\n" % (i+1))
        print("*Img Type      =  %s" % part[i][0])
        print("*Img Size      =  %s" % part[i][1])
        print("*Img Header    =  %s" % ("0x"+part[i][2]))
        print("*Img Footer    =  %s" % ("0x"+part[i][3]))
        print("*Img start No. =  %d" % part[i][4])
        print("*Img end No.   =  %d" % part[i][5])
        
def find_Header(sign,i): #파일 시그니처 해더 찾는 함수
    while(1):
        for hd in Header: 
            cmp = format((struct.unpack('>L',sign[i:i+4])[0]),'X')
            if reverse_H[Header[hd]] == cmp:
                F_type = Header[hd]
                start = i
                return (F_type,cmp,start,i)
        i = i + 1
         
def img_carve(name,part,n): #이미지 추출 함수
    while(1):
        try:
            n = int(input("\nEnter image number to extract. [exit = 0]  "))-1 #배열은 0부터 시작하나 사용자에게 보여주는 값은 1부터 시작
            if n == -1:             #사용자에게 0을 입력받으면 종료 (n-1 을 했기 때문에 n이 -1이면 종료)
                break
            f = open(name, "rb")    #파일 오픈
            f.seek(part[n][4])      #이미지 시작 위치 지정
            img = f.read(part[n][5])#이미지 끝 위치까지 읽기
            f.close() #파일 닫기
            f = open(str(n+1)+"."+part[n][0],'wb') #파일 생성 (ex 1.jpg)
            f.write(img)                            #jpg 정보 출력
            f.close()                               #파일 닫기
            print("Img File",n+1,"Carve Success")
            
        except Exception as e:    # 예외가 발생했을 때 실행됨
            print(e)
            print("Please enter a valid list number")
            pass
           
    
    
def find_footer(sign): #파일 시그니처 푸터 찾는 함수
    part = []
    start = 0
    i = 0
    F_type,hd,start, i = find_Header(sign,i)
    for i in range(i,len(sign)):
        try:
            cmp = format((struct.unpack('>H',sign[i:i+2])[0]),'X')
            if reverse_F[F_type] == cmp:
                size = SzieCalc(i-start)
                part.extend([[F_type,size,hd,cmp,start,i]])
                break
                
        except Exception as e:    # 예외가 발생했을 때 실행됨
           pass
    return part
     

if __name__ == '__main__':  #첫 실행 함수 (메인함수)
    name = "laptop.png" #숨겨진 파일을 찾을 파일 설정 (추후에 입력해서 찾거나 드래그엔 드롭으로 바로 찾게끔 
    f = open(name, "rb")   #변경 예정)
    f.seek(0)               #파일 맨 첫번째 위치로 이동
    sign = f.read()         #전체 파일 정보 저장
    part = find_footer(sign)#footer 찾는 함수로 이동
    if len(part) > 0:       #part (파일 정보가 담겨있는 배열)가 비어 있자 않다면
        File_info(part)     #파일 정보 출력 함수로 이동
        f.close()           #파일 닫기
        
        img_carve(name,part,len(part)) #이미지 추출 함수로 이동
    else:
        print("IMG NOT Found..") #이미지를 못찾았으면 종료