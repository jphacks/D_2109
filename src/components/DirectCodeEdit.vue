<template>
  <div class="trim-select-page">
    <header-menu />
    <div class="title-container">
      <img class="daruma_icon" src="../assets/daruma_icon.svg" alt="" />
      <div class="title">
        下のテキストボックスに整えるコードを入力してください
      </div>
    </div>
    <div class="code-editer">
      <code-viewer class="code-viewer" :code_list="input_code" />
      <textarea class="code-input" v-model="input_code"></textarea>
    </div>
    <div class="code-input-compleat-btn">
      <span>コードの入力を完了する</span>
    </div>
  </div>
</template>

<script>
import HeaderMenu from "./HeaderMenu.vue";
import CodeViewer from "./CodeViewer.vue";

export default {
  name: "TrimSelectPage",
  components: {
    HeaderMenu,
    CodeViewer,
  },
  data() {
    return {
      input_code: "// ここにコードを入力してください",
      disp_code: {},
    };
  },
  created() {},
  computed: {},
  methods: {},
};
</script>

<style lang="scss" scoped>
.trim-select-page {
  width: 100%;
  height: 100%;
  background-color: #f7f6e5;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  .title-container {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    .daruma_icon {
      width: 70px;
      height: 70px;
    }
    .title {
      min-width: 500px;
      padding: 20px 20px 20px 30px;
      background-image: url("../assets/hukidashi.svg");
      background-repeat: no-repeat;
      background-position: center;
      background-size: 100% 100%;
      font-weight: bold;
      font-size: 16px;
      display: flex;
      justify-content: center;
      align-items: center;
    }
  }
  .code-editer {
    margin: 50px 0;
    width: 800px;
    height: 300px;
    position: relative;
    .code-viewer {
      width: 100%;
      height: 100%;
      position: absolute;
    }
    .code-input {
      background-color: rgba($color: #ffffff, $alpha: 0);
      color: rgba(255, 255, 255, 0);
      caret-color: #ffffff;
      width: 100%;
      height: 100%;
      overflow: scroll;
      border: none;
      border-radius: 5px;
      padding: 10px 10px 10px 50px;
      line-height: 23px;
      font-size: 15px;
      resize: none;
      outline: none;
      position: absolute;
    }
  }
  .code-input-compleat-btn {
    cursor: pointer;
    border-radius: 999px;
    padding: 10px 30px;
    margin-right: 7px;
    background-color: #92d4c4;
    span {
      color: #ffffff;
      font-size: 14px;
      font-weight: bold;
    }
    &:hover {
      background-color: #5297ac;
    }
  }
}
</style>
