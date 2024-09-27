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

const setData = async () => {
  const model_info = await getSingleModelInfo(
    form.device +
      "&" +
      form.phase +
      "&" +
      "局放" +
      "|" +
      form.device +
      "&" +
      form.phase +
      "&" +
      "局部放电",
  );
  const measure_data = await getMeasuresInfo(
    form.device +
      "&" +
      form.phase +
      "&" +
      "局放" +
      "|" +
      form.device +
      "&" +
      form.phase +
      "&" +
      "局部放电",
  );
  const merged_data = mergeArrays(measure_data.data, model_info.data, "key");
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
    .filter((item) => {
      return item.unit;
    })
    .sort((a, b) => {
      return a.key.localeCompare(b.key);
    });
};

watch(
  () => form,
  () => {
    setData();
  },
  { deep: true },
);

let interval = null;
onMounted(() => {
  setData();
  interval = setInterval(() => {
    setData();
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
        <el-select
          v-model="form.device"
          placeholder="请选择区域"
          clearable
          style="width: 270px"
        >
          <el-option label="1000kV潇江Ⅰ线高抗" value="1000kV潇江Ⅰ线高抗" />
          <el-option label="1000kV潇江Ⅱ线高抗" value="1000kV潇江Ⅱ线高抗" />
          <el-option label="1000kV荆潇Ⅰ线高抗" value="1000kV荆潇Ⅰ线高抗" />
          <el-option label="1000kV荆潇Ⅱ线高抗" value="1000kV荆潇Ⅱ线高抗" />
          <el-option label="#2主变" value="#2主变" />
          <el-option label="#3主变" value="#3主变" />
        </el-select>
      </el-form-item>
      <el-form-item label="相位">
        <el-select
          v-model="form.phase"
          placeholder="请选择设备"
          clearable
          style="width: 270px"
        >
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
  <DataTable
    :title="`${form.device}${form.phase}局部放电在线监测评估`"
    :data="data"
    @set-data="setData"
  />
</template>

<style scoped></style>
