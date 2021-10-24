<template>
  <div class="loading-page">
    <header-menu />
    <img src="../assets/ninja_icon.svg" alt="">
    <p>コードを生成中･･･</p>
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
    };
  },
  created() {},
  computed: {},
  methods: {
    
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
  p{
    margin-top: 30px;
    font-size: 20px;
    font-weight: bold;
  }
}
</style>
