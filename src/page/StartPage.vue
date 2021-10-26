<template>
  <div class="start-page">
    <div class="content-container">
      <img class="catch-copy" src="../assets/catch-copy.svg" alt="" />
      <img class="logo" src="../assets/logo.svg" alt="" />
      <div class="btn-container">
        <div
          class="start-btn rule-make-btn"
          @click="ChangePage('rule_edit_page')"
        >
          <span>ルールを作成する</span>
        </div>
        <div
          class="start-btn rule-use-btn"
          @click="ChangePage('trim_select_page')"
        >
          <span>ルールを適用する</span>
        </div>
      </div>
      <div class="triangle_container">
        <img
          class="triangle"
          src="../assets/rounded-triangle-pink.svg"
          alt=""
        />
        <span class="btn-text" style="color: #e55c6e">使いかたはこちら</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "StartPage",
  data() {
    return {};
  },
  created() {},
  computed: {},
  methods: {
    ChangePage(target) {
      this.$emit("changePage", { page: target });
    },
  },
};
</script>

<style lang="scss" scoped>
.start-page {
  width: 100%;
  height: 100%;
  background-color: #faf9f1;
  background-image: url("../assets/start-bg.svg");
  background-repeat: no-repeat;
  background-position: center;
  // 画像のサイズは 1640.84:928.134 で計算
  background-size: 1350px 762px;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  .content-container {
    width: 320px;
    height: 350px;
    padding-left: 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    position: relative;
    right: 285px;
    .catch-copy {
      width: 280px;
    }
    .logo {
      margin: 20px 0;
      width: 280px;
    }
    .btn-container {
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      position: relative;
      .start-btn {
        cursor: pointer;
        border-radius: 999px;
        padding: 10px 15px;
        span {
          color: #ffffff;
          font-size: 14px;
          font-weight: bold;
        }
      }
      .rule-make-btn {
        margin-right: 7px;
        background-color: #92d4c4;
        &:hover {
          background-color: #5297ac;
        }
      }
      .rule-use-btn {
        margin-left: 7px;
        background-color: #e55c6e;
        &:hover {
          background-color: #ba3636;
        }
      }
    }
    .triangle_container {
      cursor: pointer;
      margin-top: 20px;
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
}
</style>
