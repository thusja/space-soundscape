# 소리 생성 관련 코드

from pydub.generators import WhiteNoise, Sine

def generate_base_sound(planet_info):
  """행성 정보를 기반으로 기본 소리를 생성한다."""
  duration_ms = 10000  # 기본 10초짜리 소리

  # Sine wave 기본 생성 (베이스 소리)
  base_freq = 200  # 기본 주파수 (Hz)

  # 대기 밀도에 따라 저음 필터 추가
  atmosphere = planet_info.get("atmosphere", "thin")
  if atmosphere == "dense":
    base_freq = 150
  elif atmosphere == "very dense":
    base_freq = 100
  elif atmosphere == "rich":
    base_freq = 250

  base_sound = Sine(base_freq).to_audio_segment(duration=duration_ms).apply_gain(-5)

  # 자기장에 따라 Sine wave 추가
  magnetic_field = planet_info.get("magnetic_field", "weak")

  if magnetic_field == "strong":
    sine = Sine(600).to_audio_segment(duration=duration_ms).apply_gain(-10)
    base_sound = base_sound.overlay(sine)
  elif magnetic_field == "very strong":
    sine = Sine(1000).to_audio_segment(duration=duration_ms).apply_gain(-5)
    base_sound = base_sound.overlay(sine)

  # WhiteNoise 아주 약하게 추가 (배경음 느낌)
  noise = WhiteNoise().to_audio_segment(duration=duration_ms).apply_gain(-25)
  base_sound = base_sound.overlay(noise)

  # 온도에 따라 전체 볼륨 조정
  temperature = planet_info.get("temperature", "moderate")
  if temperature == "very high" or temperature == "extremely high":
    base_sound = base_sound + 3
  elif temperature == "cold" or temperature == "very cold" or temperature == "extremely cold":
    base_sound = base_sound - 5

  # 행성 / 항성별 특수효과 추가
  planet_name = planet_info.get("name", "")

  if planet_name == "Mercury":
    # 수성 : 고주파 삐 소리 추가
    beep = Sine(5000).to_audio_segment(duration=duration_ms).apply_gain(-20)
    base_sound = base_sound.overlay(beep)

  elif planet_name == "Venus":
    # 금성: 두꺼운 대기압 표현 (저음 웅웅거림)
    heavy_air = WhiteNoise().to_audio_segment(duration=duration_ms).low_pass_filter(600).apply_gain(-18)
    base_sound = base_sound.overlay(heavy_air) 

  elif planet_name == "Earth":
    # 지구: 부드러운 백색소음 추가
    soft_noise = WhiteNoise().to_audio_segment(duration=duration_ms).apply_gain(-30)
    base_sound = base_sound.overlay(soft_noise)

  elif planet_name == "Mars":
    # 화성: 건조하고 날카로운 바람 소리
    dry_wind = WhiteNoise().to_audio_segment(duration=duration_ms).high_pass_filter(2000).apply_gain(-20)
    base_sound = base_sound.overlay(dry_wind)

  elif planet_name == "Jupiter":
    # 목성: 번개 효과 삽입
    thunder = WhiteNoise().to_audio_segment(duration=150).apply_gain(5).fade_out(150)
    for t in range(500, duration_ms, 2000):
      base_sound = base_sound.overlay(thunder, position=t)

  elif planet_name == "Saturn":
    # 토성: 고리 회전 느낌의 트릴(trill) 추가
    trill = Sine(1200).to_audio_segment(duration=100).apply_gain(-12)
    for t in range(0, duration_ms, 400):
      base_sound = base_sound.overlay(trill, position=t)

  elif planet_name == "Uranus":
    # 천왕성: 서늘하고 잔잔한 바람 소리
    cold_wind = WhiteNoise().to_audio_segment(duration=duration_ms).low_pass_filter(1500).apply_gain(-22)
    base_sound = base_sound.overlay(cold_wind)

  elif planet_name == "Neptune":
    # 해왕성: 거센 바람 소리
    strong_wind = WhiteNoise().to_audio_segment(duration=duration_ms).high_pass_filter(1000).apply_gain(-12)
    base_sound = base_sound.overlay(strong_wind) 

  elif planet_name == "Pluto":
    # 명왕성: 얼음 깨지는 듯한 메아리 느낌
    echo = WhiteNoise().to_audio_segment(duration=duration_ms).low_pass_filter(3000).apply_gain(-25).fade_in(1000).fade_out(1000)
    base_sound = base_sound.overlay(echo)

  elif planet_name == "Sun":
    # 태양: 강력한 저음 진동 + 에너지 방출
    solar_vibration = Sine(30).to_audio_segment(duration=duration_ms).apply_gain(0)
    base_sound = base_sound.overlay(solar_vibration)

  return base_sound

def save_sound(sound, filename):
  """소리를 파일로 저장한다."""
  sound.export(filename, format="wav")
  