<template>
  <div class="rule-make-loading-page">
    <header-menu @changePage="ParentChangePage($event)"/>
    <div class="daruma-container">
      <img src="../assets/daruma_blue_load.svg" alt="">
      <img src="../assets/daruma_red_load.svg" alt="">
      <img src="../assets/daruma_green_load.svg" alt="">
    </div>
    <p>ルールファイルを作成中･･･</p>
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
    return {};
  },
  created() {},
  computed: {},
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
  background-color: #f7f6e5;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  .daruma-container{
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    img{
      margin: 5px 15px;
    }
  }
  p {
    margin-top: 30px;
    font-size: 20px;
    font-weight: bold;
  }
}
</style>
