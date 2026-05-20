
import streamlit as st
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

SERVICE_KEY = "여기에_본인_API_KEY"

st.title("천안시 14번 버스 알림 앱")

station_id = st.text_input("정류장 ID 입력", "")

if st.button("버스 도착 확인"):

    url = (
        "http://apis.data.go.kr/1613000/ArvlInfoInqireService/getSttnAcctoArvlPrearngeInfoList"
        f"?serviceKey={SERVICE_KEY}"
        f"&cityCode=34010"
        f"&nodeId={station_id}"
        f"&_type=xml"
    )

    response = requests.get(url)

    root = ET.fromstring(response.content)

    found = False

    for item in root.iter("item"):

        route_no = item.findtext("routeno")

        if route_no == "14":

            found = True

            arr_time = item.findtext("arrtime")

            if arr_time:
                minutes = int(arr_time) // 60

                st.success(f"14번 버스 도착까지 {minutes}분 남음")

                if minutes <= 10:
                    st.warning("⚠️ 10분 이내 도착 예정!")
                else:
                    st.info("아직 여유 있어요")

    if not found:
        st.error("14번 버스를 찾을 수 없습니다")
```

---

