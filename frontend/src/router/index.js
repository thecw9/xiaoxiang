import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/LoginView.vue"),
  },
  {
    path: "/index",
    name: "index",
    redirect: "/home",
    component: () => import("@/views/IndexView.vue"),
    children: [
      {
        path: "/home",
        name: "home",
        meta: { title: "首页", icon: "menu" },
        component: () => import("@/views/home/index.vue"),
      },
      {
        path: "/monitor/oil-chromatography",
        name: "oil-chromatography",
        meta: { title: "油色谱监测评估", icon: "menu" },
        component: () => import("@/views/oil-chromatography/index.vue"),
      },
      {
        path: "/monitor/part-discharge",
        name: "part-discharge",
        meta: { title: "局放监测评估", icon: "menu" },
        component: () => import("@/views/part-discharge/index.vue"),
      },
      {
        path: "/monitor/iron-core",
        name: "iron-core",
        meta: { title: "铁芯夹件监测评估", icon: "menu" },
        component: () => import("@/views/iron-core/index.vue"),
      },
      // {
      //   path: "/monitor/sf6",
      //   name: "sf6",
      //   meta: { title: "SF6气体监测", icon: "menu" },
      //   component: () => import("@/views/sf6/index.vue"),
      // },
      // {
      //   path: "/monitor/sound",
      //   name: "sound",
      //   meta: { title: "声音监测", icon: "menu" },
      //   component: () => import("@/views/sound/index.vue"),
      // },
      {
        path: "/monitor/overall",
        name: "overall",
        meta: { title: "综合监测评估", icon: "menu" },
        component: () => import("@/views/overall/index.vue"),
      },
      {
        path: "/model-management",
        name: "model-management",
        meta: { title: "实时预警", icon: "menu" },
        children: [
          {
            path: "/model-management/single-model",
            name: "single-model",
            meta: { title: "自适应模型", icon: "menu" },
            component: () => import("@/views/model-management/SingleModel.vue"),
          },
          {
            path: "/model-management/expert-model",
            name: "expert-model",
            meta: { title: "融合模型", icon: "menu" },
            component: () => import("@/views/model-management/ExpertModel.vue"),
          },
        ],
      },
      {
        path: "/alarm-management",
        name: "alarm-management",
        meta: { title: "历史预警", icon: "menu" },
        children: [
          {
            path: "/alarm-management/single-alarm",
            name: "single-alarm",
            meta: { title: "自适应模型", icon: "menu" },
            component: () => import("@/views/alarm-management/SingleAlarm.vue"),
          },
          {
            path: "/alarm-management/expert-alarm",
            name: "expert-alarm",
            meta: { title: "融合模型", icon: "menu" },
            component: () => import("@/views/alarm-management/ExpertAlarm.vue"),
          },
        ],
      },
      // {
      //   path: "/train_logs",
      //   name: "train_logs",
      //   meta: { title: "训练日志", icon: "menu" },
      //   component: () => import("@/views/train_logs/index.vue"),
      // },
      {
        path: "/comparison-monitor",
        name: "comparison-monitor",
        meta: { title: "趋势分析", icon: "menu" },
        children: [
          {
            path: "/comparison-monitor/horizontal-comparison",
            name: "horizontal-comparison",
            meta: { title: "横向趋势", icon: "menu" },
            component: () => import("@/views/horizontal-comparison/index.vue"),
          },
          {
            path: "/comparison-monitor/vertical-comparison",
            name: "vertical-comparison",
            meta: { title: "纵向趋势", icon: "menu" },
            component: () => import("@/views/vertical-comparison/index.vue"),
          },
        ],
      },
      // {
      //   path: "/monitor/video",
      //   name: "video",
      //   meta: { title: "视频监测", icon: "menu" },
      //   component: () => import("@/views/video/index.vue"),
      // },
      // {
      //   path: "/report",
      //   name: "report",
      //   meta: { title: "预警报告", icon: "menu" },
      //   component: () => import("@/views/report/index.vue"),
      // },
      {
        path: "/test-model",
        name: "test-model",
        meta: { title: "模型测试", icon: "menu" },
        component: () => import("@/views/test-model/index.vue"),
      },
      {
        path: "/user",
        name: "user",
        meta: { title: "用户管理", icon: "menu" },
        component: () => import("@/views/user/index.vue"),
      },
      {
        path: "/about",
        name: "about",
        meta: { title: "关于", icon: "menu" },
        component: () => import("@/views/about/index.vue"),
      },
    ],
  },
  {
    path: "/:pathMatch(.*)*", // 404
    name: "NotFound",
    component: () => import("@/views/NotFoundView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory("/xiaoxiang/csust/"),
  routes,
});

export default router;
