# 실행 메인 파일

from data_loader import load_planet_data
from sound_engine import generate_base_sound, save_sound
import os

def main():
  data = load_planet_data()

  print("우주의 소리 시뮬레이터 시작")

  sounds_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sounds")
  os.makedirs(sounds_dir, exist_ok=True)

  for planet, info in data.items():
    print(f"\n🌍 {planet}")
    for key, value in info.items():
      print(f"  - {key}: {value}")

    # 소리 생성
    sound = generate_base_sound(info)
    filename = os.path.join(sounds_dir, f"{planet}.wav")
    save_sound(sound, filename)
    print(f"🎵 {filename} 저장 완료!")

if __name__ == "__main__":
  main()
