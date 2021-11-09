<template>
  <div class="loading-page">
    <header-menu
      @changePage="ChildChangePage($event)"
      @OpenInstructions="OpenInstructions()"
    />
    <img src="../assets/ninja_loading.gif" alt="" />
    <p>コードを生成中･･･</p>
    <div class="progress-bar-container">
      <div :style="progress_bar_style" class="progress-bar" />
    </div>
  </div>
</template>

<script>
import HeaderMenu from "../components/HeaderMenu.vue";

export default {
  name: "TrimSelectPage",
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
    ChildChangePage(target) {
      this.$emit("changePage", { page: target.page });
    },
    OpenInstructions() {
      this.$emit("OpenInstructions");
    },
  },
};
</script>

<style lang="scss" scoped>
.loading-page {
  width: 100%;
  height: 100%;
  background-color: #f7f6e5;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  p {
    margin-top: 20px;
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
    background-color: #e55c6e;
    transition: 2s;
  }
}
</style>
