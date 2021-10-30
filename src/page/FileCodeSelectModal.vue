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
    <div class="switch-btn-container">
      <div class="btn-container go-top-btn">
        <img src="../assets/home.svg" alt="" />
        <span class="go-top-text btn-text" @click="ChangePage('start_page')"
          >トップに戻る</span
        >
      </div>
      <div class="btn-container pc-btn">
        <img src="../assets/pc_file.svg" alt="" />
        <label class="pc-text btn-text">
          <input type="file" @change="FileSelect" accept=".json" />
          ファイルを選択する
        </label>
      </div>
      <div class="btn-container rule-make-btn">
        <img src="../assets/rule_make.svg" alt="" />
        <span
          class="rule-make-text btn-text"
          @click="ChangePage('rule_edit_page')"
          >ルールを作成する</span
        >
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
  .switch-btn-container {
    width: 100%;
    height: 300px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    .btn-container {
      height: 240px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      border-radius: 30px;
      .btn-text {
        font-family: noto-sans-cjk-jp, sans-serif;
        font-weight: 700;
        font-style: normal;
        cursor: pointer;
        color: #ffffff;
        margin: 20px 0 10px 0;
        padding: 5px 20px;
        font-size: 16px;
        border-radius: 999px;
      }
    }
    .go-top-btn {
      background-color: #313131;
      padding: 25px 25px 0px 25px;
      .go-top-text {
        background-color: #6f6f6f;
        &:hover {
          background-color: #434343;
        }
      }
    }
    .pc-btn {
      background-color: #efed95;
      margin: 0 40px 0 40px;
      padding: 25px 45px 0px 45px;
      .pc-text {
        background-color: #e55c6e;
        &:hover {
          background-color: #ba3636;
        }
        input[type="file"] {
          display: none;
        }
      }
    }
    .rule-make-btn {
      background-color: #ffb49c;
      padding: 25px 25px 0px 25px;
      .rule-make-text {
        background-color: #92d4c4;
        &:hover {
          background-color: #5297ac;
        }
      }
    }
  }
}
</style>
