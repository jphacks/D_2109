<template>
  <div class="trim-select-page">
    <header-menu @changePage="ParentChangePage($event)" />
    <div class="back-btn-container" @click="ChangePage('trim_select_page')">
      <img class="back-btn-image" src="../assets/left_arrow_white.svg" alt="" />
      <span>前のステップへ</span>
    </div>
    <div class="title-container">
      <img class="daruma_icon" src="../assets/daruma_icon.svg" alt="" />
      <div class="title">
        下のテキストボックスに整えるコードを入力してください
      </div>
    </div>
    <div :style="input_area_height" class="code-editer">
      <code-viewer class="code-viewer" :code_list="input_code" />
      <textarea
        :style="input_area_height"
        class="code-input"
        v-model="input_code"
        @input="ChangeHeight"
      />
    </div>
    <div class="code-input-compleat-btn" @click="CodeSubmit()">
      <span>コードの入力を完了する</span>
    </div>
  </div>
</template>

<script>
import HeaderMenu from "../components/HeaderMenu.vue";
import CodeViewer from "../components/CodeViewer.vue";

export default {
  name: "TrimSelectPage",
  components: {
    HeaderMenu,
    CodeViewer,
  },
  data() {
    return {
      input_code: "",
      input_area_height: "height:300px;",
    };
  },
  created() {},
  computed: {},
  methods: {
    ChangePage(target) {
      this.$emit("changePage", { page: target });
    },
    ParentChangePage(target) {
      this.$emit("changePage", { page: target.page });
    },
    CodeSubmit() {
      this.$emit("codeGen", { code: this.input_code });
    },
    ChangeHeight() {
      console.log(this.input_area_height);
      let over_line = this.input_code.split(/\r?\n/g).length - 13;
      console.log(over_line);
      if (over_line > 0) {
        this.input_area_height = "height:" + (300 + over_line * 22.95) + "px;";
      }
    },
  },
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
  .back-btn-container {
    cursor: pointer;
    border-radius: 999px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 120px;
    left: 50px;
    &:hover > .back-btn-image {
      background-color: #868686;
    }
    &:hover > span {
      color: #868686;
    }
    .back-btn-image {
      cursor: pointer;
      width: 25px;
      height: 25px;
      border-radius: 999px;
      background-color: #595959;
      padding: 7px;
    }
    span {
      margin-left: 10px;
      font-weight: bold;
      color: #595959;
    }
  }
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
    min-height: 300px;
    max-height: 800px;
    position: relative;
    .code-viewer {
      width: 800px;
      min-height: 300px;
      max-height: 800px;
      position: absolute;
    }
    .code-input {
      background-color: rgba($color: #ffffff, $alpha: 0);
      color: rgba(156, 53, 53, 0);
      caret-color: #ffffff;
      width: 800px;
      min-height: 300px;
      max-height: 800px;
      border: none;
      border-radius: 5px;
      padding: 10px 10px 10px 50px;
      line-height: 23px;
      font-weight: bold;
      font-size: 13px;
      letter-spacing: 0.2px;
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
