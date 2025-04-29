# 간단한 UI 코드 (Streamlit 또는 PyQt용)

from PIL import Image
import streamlit as st
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import time
import json
from streamlit.components.v1 import html

# JSON 파일 불러오기
base_path = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(base_path, "data", "planet_descriptions.json")
with open(data_path, "r", encoding="utf-8")as f:
  planet_descriptions = json.load(f)

# 웨이브 폼 그리기 함수
def plot_waveform(wav_path):
  sample_rate, data = wavfile.read(wav_path)

  # 스테레오(2채널) 파일이면 한쪽 채널만 사용
  if len(data.shape) == 2:
    data = data[:, 0]

  # 정규화: -1 ~ 1 사이로 변환
  if data.dtype == np.int16:
    data = data / 32768.0  # int16 최대값

  duration = len(data) / sample_rate
  time = np.linspace(0., duration, len(data))

  # 다운샘플링 (너무 데이터가 많으면 줄이기)
  max_points = 2500
  if len(data) > max_points:
    factor = len(data) // max_points
    data = data[::factor]
    time = time[::factor]

  fig, ax = plt.subplots(figsize=(15, 4.5))
  ax.plot(time, data, color='cyan', linewidth=0.5)
  ax.set_xlabel("Time [s]")
  ax.set_xlim([0, duration])
  ax.set_ylabel("Amplitude")
  ax.set_title("Waveform")
  ax.grid(True)
  st.pyplot(fig)

# 웨이브 폼 초기화 함수
def reset_waveform_states():
  if st.session_state.get("auto_close_waveform", True):
    st.session_state.toggle_simulation = False
    st.session_state.toggle_nasa = False
    st.session_state.show_simulation_waveform = False
    st.session_state.show_nasa_waveform = False


def main():
  st.set_page_config(page_title="우주의 소리 시뮬레이터", layout="wide")
  st.markdown('<div id="top"></div>', unsafe_allow_html=True)
  st.title("🌌 우주의 소리 시뮬레이터")

  top_col1, top_col2 = st.columns([8, 1.5])
  with top_col1:
    st.write("행성을 선택해서 소리를 들어보세요!")
  with top_col2:
    if "auto_close_waveform" not in st.session_state:
      st.session_state.auto_close_waveform = True
    st.toggle("웨이브폼 자동 닫기", key="auto_close_waveform")
  

  # 세션 상태 초기화
  if "show_simulation_waveform" not in st.session_state:
    st.session_state.show_simulation_waveform = False
  if "show_nasa_waveform" not in st.session_state:
    st.session_state.show_nasa_waveform = False

  # 폴더 경로 세팅
  base_path = os.path.dirname(os.path.dirname(__file__))
  sounds_dir = os.path.join(base_path, "sounds")
  images_dir = os.path.join(base_path, "images")
  nasa_sounds_dir = os.path.join(base_path, "nasa_sounds")

  # sounds 폴더에서 wav 파일 리스트 가져오기
  sound_files = [f for f in os.listdir(sounds_dir) if f.endswith(".wav")]

  if not sound_files:
    st.error("소리 파일이 없습니다! 먼저 소리를 생성하세요.")
    return
  
  # 행성 리스트 순서 정렬
  planet_order = [
    "Sun",
    "Mercury",
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto"
  ]

  # [sound_files를 순서에 맞게 필터링 + [파일 이름에서 확장자(.wav) 빼고 보여주기]]
  planet_names = [name for name in planet_order if name in [os.path.splitext(f)[0] for f in sound_files]]

  # 행성 선택
  selected_planet = st.selectbox("행성 선택", planet_names, key="selected_planet", on_change=reset_waveform_states)

  # 로딩 표시 추가
  with st.spinner("행성 데이터를 불러오는 중..."):
    time.sleep(1)

  if selected_planet:
    image_path = os.path.join(images_dir, selected_planet + ".jpg")
    sound_path = os.path.join(sounds_dir, selected_planet + ".wav")
    nasa_sound_path = os.path.join(nasa_sounds_dir, selected_planet + ".wav")

    # 좌우로 나누기
    col1, col2, col3 = st.columns([2, 2.5, 0.7])

    with col1:
      if os.path.exists(image_path):
        img = Image.open(image_path)
        max_height = 400
        width, height = img.size
        if height > max_height:
          new_width = int((max_height / height) * width)
          img = img.resize((new_width, max_height))
        st.image(img, caption=f"{selected_planet}의 모습", use_container_width=False)

    with col2:
      st.subheader(f"🛰️ {selected_planet} 정보")
      st.write(planet_descriptions.get(selected_planet, "설명이 준비되지 않았습니다."))

    with col3:
      st.write("")

    st.success(f"🎵 {selected_planet}의 소리를 들어보세요!")

    # 소리 재생
    with open(sound_path, "rb") as audio_file:
      audio_bytes = audio_file.read()
      st.audio(audio_bytes, format="audio/wav")

    # 시뮬레이션 웨이브폼 토글
    if st.toggle("시뮬레이션 소리 웨이브폼 보기/닫기", key="toggle_simulation"):
      st.session_state.show_simulation_waveform = True
    else:
      st.session_state.show_simulation_waveform = False

    # 버튼 누르면 웨이브폼 표시
    if st.session_state.show_simulation_waveform:
      st.subheader("📈 소리 웨이브폼 (Waveform)")
      plot_waveform(sound_path)
    
    # NASA 소리 듣기
    st.subheader("🚀 NASA가 녹음한 진짜 우주 소리 듣기")
    if os.path.exists(nasa_sound_path):
      with open(nasa_sound_path, "rb") as f:
        nasa_audio = f.read()
      st.audio(nasa_audio, format="audio/wav")
      
      # NASA 웨이브폼 토글
      if st.toggle("NASA 소리 웨이브폼 보기/닫기", key="toggle_nasa"):
        st.session_state.show_nasa_waveform = True
      else:
        st.session_state.show_nasa_waveform = False

      if st.session_state.show_nasa_waveform:
        st.subheader("📈 NASA 소리 웨이브폼 (Waveform)")
        plot_waveform(nasa_sound_path)
    else:
      st.warning(f"{selected_planet}의 NASA 소리가 준비되지 않았습니다.")

  st.markdown(
    """
    <style>
    #scroll-to-top {
      position: fixed;
      bottom: 30px;
      right: 30px;
      z-index: 1000;
    }
    #scroll-to-top button {
      background-color: #00c0ff;
      color: white;
      border: none;
      padding: 10px 16px;
      border-radius: 50px;
      font-size: 16px;
      font-weight: bold;
      box-shadow: 0 4px 6px rgba(0,0,0,0.3);
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
    #scroll-to-top button:hover {
      background-color: #0099cc;
    }
    </style>
    <div id="scroll-to-top">
      <a href="#top">
        <button>↑ Top</button>
      </a>
    </div>
    """,
    unsafe_allow_html=True
  )

if __name__ == "__main__":
  main()
