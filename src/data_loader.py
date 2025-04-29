# 천체 데이터 불러오기

import json
import os

def load_planet_data():
  # 현재 경로 기준으로 data 폴더의 planets.json 경로 생성
  base_path = os.path.dirname(os.path.dirname(__file__))
  file_path = os.path.join(base_path, "data", "planets.json")

  with open(file_path, "r") as f:
    data = json.load(f)
  return data
