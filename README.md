# 🌌 우주의 소리 시뮬레이터  
> 태양계 행성을 선택하면 해당 천체의 환경을 기반으로 생성된 사운드를 감상하고, NASA가 수집한 실제 우주 소리도 들어볼 수 있는 웹 앱입니다.

A | B | C  
--|--|--  
![시뮬레이션1](url) | ![시뮬레이션2](url) | ![시뮬레이션3](url)  

<br>

## 🔗 Links  
- [🌐 사이트 바로가기](https://space-soundscape-simulator.streamlit.app/)  
- [📘 작업 로그(노션)]()  

---

## 📘 프로젝트 개요  
- 기간: 2025.04.25 ~ 2025.04.29  
- 목적: 천체 환경을 기반으로 한 음향 시뮬레이션 및 NASA 실제 사운드 데이터 시각화

### 🎯 제작 배경  
천체에 따라 소리가 다르게 들린다면 어떤 느낌일까?  
지구 외 다른 행성들의 대기, 자기장, 온도 정보를 바탕으로 각기 다른 음향을 생성하고 NASA에서 수집한 실제 사운드와 비교해볼 수 있도록 구성했습니다.

### 🛠 기술 스택  
- `Python`  
- Library : `Streamlit`,`pydub`, `scipy`, `matplotlib`, `Pillow`, `numpy`, `json`  
- 배포: Streamlit Community Cloud

---

## ✨ 주요 기능  
1. 행성 선택에 따른 시뮬레이션 사운드 생성  
2. NASA가 수집한 실제 우주 소리 감상  
3. 웨이브폼(파형) 시각화 (matplotlib 기반)  
4. 행성별 특수효과(예: 목성-번개음, 해왕성-바람음)  
5. 자동/수동 웨이브폼 닫기 토글 기능  

---

## 🧱 프로젝트 구조

### 🖼 레이아웃 구성  
- 상단: 행성 선택 및 웨이브폼 자동닫기 토글
- 좌측: 행성 이미지  
- 우측: 행성 설명  
- 하단: 사운드 플레이어 및 웨이브폼 출력  

### 📁 폴더 구조  
space-soundscape/
├── .streamlit/
├── data/
│ ├── planets.json
│ └── planet_descriptions.json
├── images/
├── nasa_sounds/
├── sounds/
├── src/
│ ├── main.py
│ ├── ui.py
│ ├── data_loader.py
│ └── sound_engine.py
├── requirements.txt
└── README.md

### 📜 주요 코드 파일  
- `ui.py`: 전체 Streamlit UI 구성  
- `sound_engine.py`: 사운드 생성 로직  
- `data_loader.py`: 천체 JSON 데이터 로딩 모듈  
- `main.py`: 우주의 소리 시뮬레이터 시작 실행 메인 파일

---

## ✅ 추후 작업 및 이슈
- 🔊 실제 오디오 기반 스펙트럼 시각화 (FFT) 추가
- 📤 사용자 사운드 업로드 및 비교 기능

---

## 🔗 참고자료
- [NASA Sound Library](https://www.youtube.com/@vishalm1537)  NASA 공식홈페이지는 현재 지원하지 않음
- [pydub Documentation](https://pydub.com/)  
- [Streamlit Docs](https://docs.streamlit.io/)  
