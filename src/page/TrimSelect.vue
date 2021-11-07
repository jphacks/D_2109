<template>
  <div class="trim-select-page">
    <header-menu @changePage="ChildChangePage($event)" />
    <div class="back-btn-container" @click="ChangePage('trim_select_page')">
      <img class="back-btn-image" src="../assets/left_arrow_white.svg" alt="" />
      <span>ルールファイルの選択へ</span>
    </div>
    <div class="title-container">
      <img class="daruma_icon" src="../assets/daruma_icon.svg" alt="" />
      <div class="title">
        まずは整えるコードのアップロード法を選択してください
      </div>
    </div>
    <div class="select-container">
      <div class="trim-content text-file">
        <label>
          <img src="../assets/textfile_icon.svg" alt="" />
          <input type="file" @change="FileSelect" accept=".py" />
        </label>
        <span> テキストファイルで </span>
      </div>
      <div class="trim-content direct-code">
        <img
          src="../assets/code_icon.svg"
          alt=""
          @click="ChangePage('direct_code_edit_page')"
        />
        <span> そのままコードで </span>
      </div>
    </div>
    <div class="trim-description">
      <div class="arrow-container">
        <img src="../assets/red_arrow.svg" alt="" />
        <img src="../assets/green_arrow.svg" alt="" />
      </div>
      <span>trim（トリム）</span
      >は個人間でバラバラになりがちなプログラムを自身や<br />
      チームの中で決めたルールに自動で書き換えてくれるアプリケーションです。
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
    return {};
  },
  created() {},
  computed: {},
  methods: {
    FileSelect(target) {
      target.preventDefault();
      let files = target.target.files;
      this.$emit("fileSelect", { file: files[0] });
    },
    ChangePage(target) {
      this.$emit("changePage", { page: target });
    },
    ChildChangePage(target) {
      this.$emit("changePage", { page: target.page });
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

      font-size: 16px;
      display: flex;
      justify-content: center;
      align-items: center;
    }
  }
  .select-container {
    margin: 40px 0;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    img {
      cursor: pointer;
      width: 125px;
      height: 125px;
      &:hover {
        filter: drop-shadow(0px 2px 5px rgba(0, 0, 0, 0.6));
      }
    }
    span {
      margin-top: 20px;
      font-size: 17px;
    }
    .text-file {
      margin-right: 35px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      input[type="file"] {
        display: none;
      }
    }
    .direct-code {
      margin-left: 35px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }
  }
  .trim-description {
    padding: 10px 10px 10px 30px;
    font-size: 16px;

    line-height: 30px;
    background-color: #ffffff;
    border: solid 2px #ffc6b4;
    border-radius: 10px;
    position: relative;
    .arrow-container {
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      position: absolute;
      left: -15px;
      top: -12px;
      img {
        margin: 0 5px;
      }
    }
  }
}
</style>
