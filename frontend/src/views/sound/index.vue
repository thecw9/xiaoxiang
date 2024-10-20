<script setup>
import { ref, reactive, onMounted, watch, onBeforeUnmount, provide } from "vue";
import { getMeasuresInfo } from "@/api/measures";
import { getSingleModelInfo } from "@/api/singleModel";
import { trimNumber, mergeArrays, alarmCodeToStatus } from "@/utils";
import DataTable from "@/components/DataTable.vue";
import TrainAllButton from "@/components/TrainAllButton.vue";

const data = ref([]);
const form = reactive({
  device: "1000kV潇江Ⅰ线高抗",
  phase: "A相",
});
const urls = ref([]);

const setURLs = async () => {
  const now = new Date();
  now.setMinutes(now.getMinutes() - 2); // 2分钟前
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  const hour = String(now.getHours()).padStart(2, "0");
  const minute = String(now.getMinutes()).padStart(2, "0");

  const baseUrl = "/minio-api/power-prophet";

  // 清除所有URL
  urls.value = [];

  urls.value.push({
    name: `Waveform: ${year}年${month}月${day}日 ${hour}时${minute}分`,
    url: `${baseUrl}/waveform/${year}-${month}-${day}/${hour}-${minute}_测试地址.png`
  })
  urls.value.push({
    name: `FFT: ${year}年${month}月${day}日 ${hour}时${minute}分`,
    url: `${baseUrl}/fft/${year}-${month}-${day}/${hour}-${minute}_测试地址.png`
  })
  console.log(urls.value)
};

const setData = async () => {
  // const measure_data = await getMeasuresInfo(
  //   form.device + "&" + form.phase + "&" + "声纹",
  // );
  // const model_info = await getSingleModelInfo(
  //   form.device + "&" + form.phase + "&" + "声纹",
  // );
  const measure_data = await getMeasuresInfo(
    "声纹",
  );
  const model_info = await getSingleModelInfo(
    "声纹",
  );
  const merged_data = mergeArrays(measure_data.data, model_info.data, "key");
  console.log(merged_data);
  data.value = merged_data
    .map((item) => {
      return {
        key: item.key,
        // path: item.path.split("_")[item.path.split("_").length - 1],
        path: item.path.split("/")[item.path.split("/").length - 1],
        time: item.time?.replace("T", " ").split(".")[0],
        value: trimNumber(item.value),
        unit: item.unit,
        status: alarmCodeToStatus(item.status),
        message: item.message?.split(" ")[item.message.split(" ").length - 1],
        report_path: item.report_path,
      };
    })
    // .filter((item) => {
    //   return item.unit;
    // })
    .sort((a, b) => {
      return a.key.localeCompare(b.key);
    });
  console.log(data.value);
};

watch(
  () => form,
  () => {
    setData();
    setURLs();
  },
  { deep: true },
);

let interval = null;
onMounted(() => {
  setData();
  setURLs();
  interval = setInterval(() => {
    setData();
    setURLs();
  }, 10000);
});

onBeforeUnmount(() => {
  clearInterval(interval);
});
</script>

<template>
  <!-- 搜索框 -->
  <div class="input_box">
    <el-form :inline="true" :model="form">
      <el-form-item label="设备">
        <el-select v-model="form.device" placeholder="请选择区域" clearable style="width: 270px">
          <el-option label="1000kV潇江Ⅰ线高抗" value="1000kV潇江Ⅰ线高抗" />
          <el-option label="1000kV潇江Ⅱ线高抗" value="1000kV潇江Ⅱ线高抗" />
          <el-option label="1000kV荆潇Ⅰ线高抗" value="1000kV荆潇Ⅰ线高抗" />
          <el-option label="1000kV荆潇Ⅱ线高抗" value="1000kV荆潇Ⅱ线高抗" />
          <el-option label="#2主变" value="#2主变" />
          <el-option label="#3主变" value="#3主变" />
        </el-select>
      </el-form-item>
      <el-form-item label="相位">
        <el-select v-model="form.phase" placeholder="请选择设备" clearable style="width: 270px">
          <el-option label="A相" value="A相" />
          <el-option label="B相" value="B相" />
          <el-option label="C相" value="C相" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="setData">更新数据</el-button>
        <TrainAllButton :data="data" @set-data="setData" />
      </el-form-item>
    </el-form>
  </div>
  <!-- 数据展示 -->
  <DataTable :title="`${form.device}${form.phase}油色谱在线监测评估`" :data="data" @set-data="setData" />
  <div class="spectrogram">
    <el-row gutter="20">
      <el-col
        v-for="item in urls"
        :key="item.name"
        :span="12"
        style="margin-bottom: 30px"
      >
        <span style="font-size: 20px; display: flex; justify-content: center">{{
          item.name
        }}</span>
        <el-image
          style="width: 100%; height: 100%"
          :src="item.url"
          fit="contain"
        ></el-image>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped></style>
