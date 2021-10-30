<template>
  <div class="rule-make-loading-page">
    <header-menu @changePage="ParentChangePage($event)" />
    <div class="daruma-container">
      <img src="../assets/daruma_blue_load.svg" alt="" />
      <img src="../assets/daruma_red_load.svg" alt="" />
      <img src="../assets/daruma_green_load.svg" alt="" />
    </div>
    <p>ルールファイルを作成中･･･</p>
    <div class="progress-bar-container">
      <div :style="progress_bar_style" class="progress-bar" />
    </div>
  </div>
</template>

<script>
import HeaderMenu from "../components/HeaderMenu.vue";

export default {
  name: "RuleMakeLoadingPage",
  components: {
    HeaderMenu,
  },
  data() {
    return {
      progress_bar_style: "width:0%;",
    };
  },
  created() {},
  computed: {},
  mounted() {
    new Promise(function (resolve) {
      window.setTimeout(resolve, 10);
    }).then(() => {
      this.progress_bar_style = "width:100%;";
    });
  },
  methods: {
    ParentChangePage(target) {
      this.$emit("changePage", { page: target.page });
    },
  },
};
</script>

<style lang="scss" scoped>
.rule-make-loading-page {
  width: 100%;
  height: 100%;
  background-color: #e5eeeb;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  .daruma-container {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    img {
      margin: 5px 15px;
    }
  }
  p {
    margin-top: 30px;
    font-size: 20px;
  }
  .progress-bar-container {
    width: 300px;
    height: 10px;
    margin-top: 30px;
    border-radius: 5px;
    background-color: #a1a1a1;
  }
  .progress-bar {
    height: 100%;
    border-radius: 5px;
    background-color: #70998f;
    transition: 1s;
  }
}
</style>
