환경 
* centos
* python 3.5
* tensorflow 1.4

순서
  1. pip install requirement.txt
  2. python preprocess.py
  -  dataset 폴더에 txt파일들 생성됨
    질문|a면 answer, pa면 plausible answer|answer|시작글자index|끝글자index|시작문자index|끝문자index|문장index
  3. python parse.py

