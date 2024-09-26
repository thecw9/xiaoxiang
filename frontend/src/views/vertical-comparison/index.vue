<script setup>
import { ref, reactive, onMounted, watch, onBeforeUnmount } from "vue";
import { getMeasuresInfo } from "@/api/measures";
import VerticalComparisonDataTable from "@/components/VerticalComparisonDataTable.vue";
import TrainAllButton from "@/components/TrainAllButton.vue";
import { trimNumber } from "@/utils";

const data = ref([]);
const comparison_data = ref([]);

const form = reactive({
  device: "1000kV潇江Ⅰ线高抗",
  phase: "A相",
});

const setComparisonData = async () => {
  const include_info =
    `${form.device}&${form.phase}&油色谱&C|` +
    `${form.device}&${form.phase}&油色谱&总烃|` +
    `${form.device}&${form.phase}&油色谱&H2`;
  const exclude_info = "告警&增量&测量量&速率";
  // console.log("include info", include_info);
  await getMeasuresInfo(include_info, exclude_info).then((res) => {
    if (res.code === 200) {
      // console.log("res_data", res.data);
      comparison_data.value = res.data
        .map((item) => {
          // return item.key;
          return {
            key: item.key,
            path: item.path.split("_")[item.path.split("_").length - 1],
            // time: item.time.replace("T", " ").split(".")[0],
            time: item.service_time?.replace("T", " ").split(".")[0],
            service_time: item.service_time?.replace("T", " ").split(".")[0],
            value: trimNumber(item.value),
            unit: item.unit,
            status:
              item.status === 0
                ? "模型未训练"
                : item.status === 1
                  ? "正常"
                  : item.status === 2
                    ? "预警"
                    : item.status === 3
                      ? "报警"
                      : "未知",
            model_name: item.model_name,
            model_is_trained: item.model_is_trained,
            model_updated_at: item.model_updated_at
              ?.replace("T", " ")
              .split(".")[0],
            model_version: item.model_version,
            train_data_total: item.train_data_total,
          };
        })
        .filter((item) => {
          return item.unit;
        })
        .sort((a, b) => {
          return a.key - b.key;
        });
    }
  });
};

watch(
  () => form,
  () => {
    setComparisonData();
  },
  { deep: true },
);

let interval = null;
onMounted(() => {
  setComparisonData();
  interval = setInterval(() => {
    setComparisonData();
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
        <el-button type="primary" @click="setComparisonData"
          >更新数据</el-button
        >
        <TrainAllButton :data="data" @set-data="setComparisonData" />
      </el-form-item>
    </el-form>
  </div>
  <!-- 数据展示 -->
  <VerticalComparisonDataTable
    :title="`${form.device}${form.phase}油色谱纵向趋势分析`"
    :data="comparison_data"
    @set-comparison-data="setComparisonData"
  />
</template>

<style scoped></style>
