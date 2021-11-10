<template>
  <div class="file-code-select-modal">
    <div class="modal-description">
      <div class="description-text-contaienr">
        <img src="../assets/daruma_modal.svg" alt="" />
        <p>ようこそ。trimへ</p>
        <p>まずは、コードを整えるためのルールファイルを選択してください。</p>
        <p>
          まだ、ルールを作成していない人は右下のボタンからルールの作成画面へ飛んでください。
        </p>
      </div>
    </div>
    <div class="selector-container">
      <div class="title">メニュー</div>
      <div class="btn-container go-top" @click="ChangePage('start_page')">
        <div class="left-pin" />
        <div class="right-pin" />
        <div class="btn-title">トップへ戻る</div>
        <div class="img-container go-top-img">
          <img src="../assets/home_back.svg" alt="" />
          <img class="img-active" src="../assets/home_back_hover.svg" alt="" />
        </div>
      </div>
      <label class="btn-container select-file">
        <div class="left-pin" />
        <div class="right-pin" />
        <div class="btn-title">ルールファイルを選択</div>
        <div class="img-container select-file-img">
          <img src="../assets/rule_select.svg" alt="" />
          <img
            class="img-active"
            src="../assets/rule_select_hover.svg"
            alt=""
          />
        </div>
        <input type="file" @change="FileSelect" accept=".json" />
      </label>
      <div
        class="btn-container make-rule"
        @click="ChangePage('rule_edit_page')"
      >
        <div class="left-pin" />
        <div class="right-pin" />
        <div class="btn-title">ルールを作成する</div>
        <div class="img-container make-rule-img">
          <img src="../assets/rule_create.svg" alt="" />
          <img
            class="img-active"
            src="../assets/rule_create_hover.svg"
            alt=""
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FileCodeSelectModal",
  components: {},
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
  },
};
</script>

<style lang="scss" scoped>
.file-code-select-modal {
  width: 100vw;
  height: 100vh;
  background-color: #3030301a;
  background-image: url("../assets/modal_bg.svg");
  background-position: center;
  background-size: contain;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: absolute;
  z-index: 10000;
  .modal-description {
    width: 100%;
    height: 200px;
    background-image: url("../assets/green_bg.svg");
    background-position: center;
    background-repeat: no-repeat;
    background-size: 100% auto;
    display: flex;
    justify-content: center;
    align-items: center;
    .description-text-contaienr {
      height: 100%;
      max-width: 600px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: flex-start;
      position: relative;
      img {
        width: 100px;
        height: 106.34px;
        margin-top: 25px;
        position: absolute;
        top: 0px;
        left: -130px;
      }
      p {
        margin: 3px 0;
        font-size: 19px;
      }
    }
  }
  .selector-container {
    background-color: #d7be96;
    width: 750px;
    height: 280px;
    margin-top: 20px;
    border-radius: 15px;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    .title {
      width: 150px;
      height: 58px;
      padding-left: 20px;
      color: #7c5510;
      background-image: url("../assets/mini_husen.svg");
      background-repeat: no-repeat;
      background-position: center;
      background-size: contain;
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      position: absolute;
      top: 20px;
      left: 40px;
    }
    .btn-container {
      cursor: pointer;
      background-color: #e8e1d7;
      border: 3px solid #ffffff00;
      border-radius: 10px;
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      position: absolute;
      transition: 0.2s;
      .left-pin {
        width: 15px;
        height: 15px;
        border-radius: 999px;
        background-color: #d0b546;
        position: absolute;
        top: 6px;
        left: 6px;
      }
      .right-pin {
        width: 15px;
        height: 15px;
        border-radius: 999px;
        background-color: #d0b546;
        position: absolute;
        top: 6px;
        right: 6px;
      }
      .btn-title {
        color: #7b685c;
        font-size: 15px;
        position: absolute;
        top: 25px;
        transition: 0.2s;
      }
      .img-container {
        display: flex;
        justify-content: center;
        align-items: center;
        position: absolute;
        img {
          position: absolute;
          transition: 0.2s;
        }
        .img-active {
          opacity: 0;
        }
      }
      &:hover {
        border: 3px solid #f5f397;
        background-color: #fbfcec;
      }
      &:hover > .btn-title {
        color: #000000;
      }
      &:hover > .img-container > .img-active {
        opacity: 1;
      }
      input[type="file"] {
        display: none;
      }
    }
    .go-top {
      width: 160px;
      height: 170px;
      top: 90px;
      left: 30px;
      .go-top-img {
        width: 100px;
        height: 100px;
        top: 50px;
      }
    }
    .select-file {
      width: 230px;
      height: 200px;
      top: 60px;
      left: 230px;
      .select-file-img {
        width: 200px;
        height: 100px;
        top: 70px;
      }
    }
    .make-rule {
      width: 230px;
      height: 200px;
      top: 60px;
      right: 30px;
      .make-rule-img {
        width: 140px;
        height: 120px;
        top: 70px;
      }
    }
  }
}
</style>
