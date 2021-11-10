<template>
  <div class="file-code-select-modal">
    <div class="daruma_container">
      <img src="../assets/daruma_blue.svg" alt="" />
      <span> 変更後のコード </span>
    </div>
    <code-viewer class="code-viewer" :code_list="output_python" />
    <div class="close-btn" @click="ShowExpansionModal()">
      <span>拡大表示の終了</span>
      <img src="../assets/close_screen.svg" alt="" />
    </div>
  </div>
</template>

<script>
import CodeViewer from "../components/CodeViewer.vue";

export default {
  name: "FileCodeSelectModal",
  props: {
    output_python: String,
  },
  components: {
    CodeViewer,
  },
  data() {
    return {};
  },
  created() {},
  computed: {},
  methods: {
    ShowExpansionModal() {
      this.$emit("ShowExpansionModal");
    },
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
  background-color: #0e0e0ede;
  background-position: center;
  background-size: contain;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: absolute;
  z-index: 10000;
  .daruma_container {
    margin-bottom: 10px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    span {
      color: #ffffff;
      margin-left: 10px;
    }
  }
  .code-viewer {
    width: 80%;
    height: 70%;
  }
  .close-btn {
    cursor: pointer;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    position: absolute;
    right: 50px;
    bottom: 30px;
    span {
      color: #ffffff;
      font-weight: 400;
      margin-right: 5px;
    }
    img {
      position: relative;
      top: -2px;
    }
  }
}
</style>
