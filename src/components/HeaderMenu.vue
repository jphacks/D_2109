<template>
  <div class="header-menu">
    <div class="left-content">
      <img class="logo" src="../assets/logo.svg" alt="" />
      <div class="btn_container">
        <img
          class="triangle"
          src="../assets/rounded-triangle-pink.svg"
          alt=""
        />
        <span class="btn-text" style="color: #e55c6e">使いかた</span>
      </div>
      <div class="btn_container">
        <img
          class="triangle"
          src="../assets/rounded-triangle-bule.svg"
          alt=""
        />
        <span class="btn-text" style="color: #5ca1e5">trimとは</span>
      </div>
    </div>
    <div class="rigth_btn">トップに戻る</div>
  </div>
</template>

<script>
export default {
  name: "HeaderMenu",
  data() {
    return {};
  },
  created() {},
  computed: {},
  methods: {},
};
</script>

<style lang="scss" scoped>
.header-menu {
  background-color: #faf9f1;
  width: 100%;
  height: 80px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  position: absolute;
  top: 0px;
  z-index: 5000;
  .left-content {
    padding-left: 25px;
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    align-items: center;
    .logo {
      height: 50px;
      margin-right: 20px;
    }
    .btn_container {
      cursor: pointer;
      margin: 0 10px;
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      &:hover > .triangle {
        filter: drop-shadow(0px 1px 10px #aaa);
      }
      &:hover > .btn-text {
        filter: drop-shadow(0px 1px 10px #aaa);
      }
      .triangle {
        width: 15px;
        margin-right: 10px;
      }
      .btn-text {
        font-size: 17px;
        font-weight: bold;
      }
    }
  }
  .rigth_btn {
    cursor: pointer;
    background-color: #6f6f6f;
    width: 170px;
    height: 50px;
    border-radius: 999px;
    margin-right: 25px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    color: #ffffff;
    font-size: 17px;
    font-weight: bold;
    &:hover {
      background-color: #434343;
    }
  }
}
</style>
