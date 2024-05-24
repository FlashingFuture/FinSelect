<template>
  <div>
    <div class="p-3 width-680 mx-auto">
      <p>주변 은행 찾기</p>
    </div>
    <div class="p-3 mx-auto search-map-div">
      <div class="mb-2 search-div p-3 d-flex justify-content-between align-item-center">
        <div class="me-2">
          <p class="me-2">위치 키워드 검색 </p>
          <input type="text" v-model.trim="keyword" @keyup.enter="search">
        </div>
        <div class="d-flex flex-column justify-content-center flex-nowrap">
          <span class="search-div-explain">- 검색된 키워드 위치 주변 은행을 찾아 드려요.</span>
          <span class="search-div-explain">- 잘 검색되지 않는 지역 / 건물은 못 찾을 수도 있어요.</span>
          <span class="search-div-explain">- 검색이 제대로 안되면 '코엑스 삼성역', '서울 금호역'과 같이  &nbsp;&nbsp;지역을 더 특정해 보세요.</span>
        </div>
      </div>
      <div>
        <KakaoMap :lat="target_lat" :lng="target_lng" :level="3" @onLoadKakaoMap="onLoadKakaoMap">
          <KakaoMapMarker
            v-for="(marker, index) in markerList"
            :key="marker.key === undefined ? index : marker.key"
            :lat="marker.lat"
            :lng="marker.lng"
            :image="getMarkerImage(marker.infoWindow.content)"
            :clickable="true"
            @onClickKakaoMapMarker="onClickMapMarker(marker)"
            @mouseOverKakaoMapMarker="mouseOverKakaoMapMarker(marker)"
            @mouseOutKakaoMapMarker="mouseOutKakaoMapMarker(marker)"
          >
            <template v-slot:infoWindow>
              <div style="padding: 2px; font-size: 12px;">
                {{ marker.infoWindow.content.replace(/<\/?[^>]+(>|$)/g, "") }}
              </div>
            </template>
          </KakaoMapMarker>
        </KakaoMap>
      </div>
      <div>
        <div class="info-div">
          <p>- 줌인 / 줌아웃 : 마우스 스크롤</p>
          <p>- 지도 이동 : 클릭 후 마우스 드래그</p>
        </div>
      </div>
    </div>
    <div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { KakaoMap, KakaoMapMarker } from 'vue3-kakao-maps'
import { useStore } from '@/stores/main'

const store = useStore()

const keyword = ref(null)
const target_lat = ref(33.450701)
const target_lng = ref(126.570667)
//라이브러리 사용 방법을 반드시 참고하여 주시기 바랍니다.
const map = ref();
const markerList = ref([]);

const onLoadKakaoMap = (mapRef) => {
  map.value = mapRef;

  // 장소 검색 객체를 생성합니다
  const ps = new kakao.maps.services.Places();
  // 키워드로 장소를 검색합니다
  ps.categorySearch('BK9', placesSearchCB, {
    location: new kakao.maps.LatLng(37.5, 127.1)
  });
};

const search = () => {
  if (map.value) {
    const keywordps = new kakao.maps.services.Places();
    keywordps.keywordSearch(keyword.value, keywordCB)
  }
}

const keywordCB = (data, status) => {
  if (status === kakao.maps.services.Status.OK) {
    // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
    // LatLngBounds 객체에 좌표를 추가합니다
    const bounds = new kakao.maps.LatLngBounds();
    for (let marker of data) {
      bounds.extend(new kakao.maps.LatLng(Number(marker.y), Number(marker.x)));
    }
    // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
    target_lat.value = (bounds.qa + bounds.pa) / 2
    target_lng.value = (bounds.ha + bounds.oa) / 2
    
    // 장소 검색 객체를 생성합니다
    const ps = new kakao.maps.services.Places();
    // 키워드로 장소를 검색합니다
    ps.categorySearch('BK9', placesSearchCB, {
      location: new kakao.maps.LatLng(target_lat.value, target_lng.value)
    });
    map.value.panTo(new kakao.maps.LatLng(target_lat.value, target_lng.value))
    map.value.setLevel(3)
  } else {
    console.log('keyword 실패')
  }
};

// 키워드 검색 완료 시 호출되는 콜백함수 입니다
const placesSearchCB = (data, status) => {
  if (status === kakao.maps.services.Status.OK) {
    // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
    // LatLngBounds 객체에 좌표를 추가합니다
    const bounds = new kakao.maps.LatLngBounds();

    for (let marker of data) {
      const markerItem = {
        lat: marker.y,
        lng: marker.x,
        infoWindow: {
          content: `<div class="info-window">${marker.place_name}</div>`,
          visible: false,
        }
      };
      markerList.value.push(markerItem);
      bounds.extend(new kakao.maps.LatLng(Number(marker.y), Number(marker.x)));
    }
    // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
    map.value?.setBounds(bounds);
  }
};

//마커 클릭 시 인포윈도우의 visible 값을 반전시킵니다
const onClickMapMarker = (markerItem) => {
  if (markerItem.infoWindow?.visible !== null && markerItem.infoWindow?.visible !== undefined) {
    markerItem.infoWindow.visible = !markerItem.infoWindow.visible;
  } else {
    markerItem.infoWindow.visible = true;
  }
};

const mouseOverKakaoMapMarker = (markerItem) => {
  markerItem.infoWindow.visible = true;
};

const mouseOutKakaoMapMarker = (markerItem) => {
  markerItem.infoWindow.visible = false;
};

// 마커 이미지 소스에 은행 이미지 할당하기
const getMarkerImage = (placeName) => {
  let imageSrc = 'http://localhost:5173/assets/images/location.png'
  for (const bank of store.bankData) {
    if (placeName.includes(bank.name)) {
      imageSrc = `http://127.0.0.1:8000${ bank.bank_image }`
      break;
    }
  }

  return {
    imageSrc,
    imageWidth: 44,
    imageHeight: 44,
    imageOption: {
      offset: new kakao.maps.Point(16, 34),
      alt: "마커 이미지 예제",
      shape: "poly",
      coords: "1,20,1,9,5,2,10,0,21,0,27,3,30,9,30,20,17,33,14,33"
    }
  }
}
</script>

<style scoped>

.width-680 {
  width: 680px;
}

.width-680 p {
  font-size: 32px;
}
.search-map-div {
  background-color: rgb(90, 147, 255);
  width: 680px;
  border-radius: 25px;
}

.search-div {
  background-color: #F7E600;
  width: 99%;
  border-radius: 15px;
}

.search-div p {
  color: #3A1D1D;
  font-size: 24px;
}

.search-div input {
  border: 2px solid #3A1D1D;
  border-radius: 5px;
  padding: 10px;
}

.search-div-explain {
  font-size: 14px;
}

.info-div {
  padding-top: 15px;
}
.info-div p {
  font-size: 14px;
  color: white;
}

.info-window {
  padding: 30px;
  background-color: blue;
}
</style>