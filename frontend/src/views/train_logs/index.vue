<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { ElMessageBox, ElNotification } from "element-plus";
import { getTrainLogsList } from "@/api/trainlogs";

const dialogVisible = ref(false);
const dialogVisibleContent = ref("");
const trainlogs = ref([]);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

const handleClose = () => {
  ElMessageBox.confirm("确认关闭？")
    .then(() => {
      dialogVisible.value = false;
    })
    .catch(() => {});
};

const tableRowClassName = ({ row, rowIndex }) => {
  if (row.state === "SUCCESS") {
    return "success-row";
  } else if (row.state === "FAILURE") {
    return "error-row";
  }
  return "warning-row";
};

// get train logs list data
const setTrainLogsListData = async () => {
  const res = await getTrainLogsList(
    null,
    null,
    currentPage.value,
    pageSize.value,
  );
  trainlogs.value = res.data
    .map((item) => {
      return {
        id: item.task_id,
        task_name:
          item.task_name.split(".")[item.task_name.split(".").length - 1],
        state: item.state,
        result: item.result,
        start_time: item.start_time?.replace("T", " ").split(".")[0],
        end_time: item.end_time?.replace("T", " ").split(".")[0],
        args: item.args,
        kargs: item.kargs,
        runtime: item.runtime,
        error_traceback: item.error_traceback,
      };
    })
    .sort((a, b) => b.start_time - a.start_time);
  total.value = res.total;
};

const handleOpenDialog = (row) => {
  dialogVisibleContent.value = JSON.stringify(row, null, 4);
  dialogVisible.value = true;
};

onMounted(() => {
  setTrainLogsListData();
});

const handleCurrentChange = (val) => {
  currentPage.value = val;
  setTrainLogsListData();
};

const interval = setInterval(() => {
  setTrainLogsListData();
}, 1000);

onUnmounted(() => {
  clearInterval(interval);
});
</script>

<template>
  <div>
    <!-- 新增用户弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      title="训练日志详情"
      width="80%"
      :before-close="handleClose"
    >
      <pre>{{ dialogVisibleContent }}</pre>
      <template #footer>
        <span class="dialog-footer">
          <el-button class="cancel-btn" @click="dialogVisible = false"
            >Cancel</el-button
          >
          <el-button type="primary" @click="dialogVisible = false">
            Confirm
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 用户列表 -->
    <div class="table-box">
      <el-table
        :data="trainlogs"
        style="width: 100%"
        :row-class-name="tableRowClassName"
      >
        <!-- <el-table-column prop="id" label="ID" /> -->
        <el-table-column
          prop="task_name"
          label="任务名称"
          align="center"
          width="400"
        />
        <el-table-column prop="state" label="状态" align="center" width="200" />
        <el-table-column prop="start_time" label="开始时间" />
        <el-table-column prop="end_time" label="结束时间" />
        <!-- <el-table-column prop="args" label="参数" width="300"> -->
        <!--   <template #default="{ row }"> -->
        <!--     <pre>{{ JSON.stringify(row.args, null, 2) }}</pre> -->
        <!--   </template> -->
        <!-- </el-table-column> -->
        <el-table-column
          prop="runtime"
          label="运行时间"
          width="90"
          align="center"
        />
        <el-table-column label="操作" fixed="right" width="100" align="center">
          <template #default="{ row }">
            <el-button type="primary" @click="handleOpenDialog(row)"
              >详情</el-button
            >
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          background
          :total="total"
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 30, 50]"
          layout="prev, pager, next, sizes"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.json-text {
  white-space: pre-line;
  font-family: monospace;
  /* 其他样式可以根据需要添加 */
}

.el-input {
  width: 300px;
  margin-right: 15px;
}
</style>
