<template>
  <div class="code-gen-complete-page">
    <header-menu @changePage="ChildChangePage($event)" />
    <div class="code-viewer-container">
      <div class="left-viewer">
        <div class="daruma_container">
          <img src="../assets/daruma_red.svg" alt="" />
          <span> 変更前 </span>
        </div>
        <code-viewer class="code-viewer" :code_list="input_python" />
      </div>
      <div class="right-viewer">
        <div class="daruma_container">
          <img src="../assets/daruma_blue.svg" alt="" />
          <span> 変更後 </span>
        </div>
        <code-viewer class="code-viewer" :code_list="output_python" />
      </div>
    </div>
    <div class="btn-container">
      <div
        class="code-input-compleat-btn another-btn"
        @click="ChangePage('trim_select_page')"
      >
        <span>別テキストに適用する</span>
      </div>
      <div
        class="code-input-compleat-btn dl-btn"
        @click.prevent="downloadItem()"
      >
        <span>ファイルをダウンロード</span>
      </div>
    </div>
  </div>
</template>

<script>
import HeaderMenu from "../components/HeaderMenu.vue";
import CodeViewer from "../components/CodeViewer.vue";

export default {
  name: "TrimSelectPage",
  props: {
    input_python: String,
    output_python: String,
  },
  components: {
    HeaderMenu,
    CodeViewer,
  },
  data() {
    return {
      input_code: "",
      output_code: "",
    };
  },
  created() {},
  computed: {},
  methods: {
    downloadItem() {
      this.$emit("downloadItem");
    },
    ChangePage(target) {
      this.$emit("changePage", { page: target });
    },
    ChildChangePage(target) {
      this.$emit("changePage", { page: target.page });
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
.code-gen-complete-page {
  width: 100%;
  height: 100%;
  background-color: #f7f6e5;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  .code-viewer-container {
    margin: 20px 0;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    .code-viewer {
      width: 450px;
      height: 400px;
    }
    .left-viewer {
      margin-right: 20px;
    }
    .right-viewer {
      margin-left: 20px;
    }
    .daruma_container {
      width: 100%;
      margin-bottom: 10px;
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      span {
        margin-left: 10px;
        font-size: 15px;
      }
    }
  }
  .btn-container {
    width: 950px;
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    align-items: center;
    .code-input-compleat-btn {
      font-family: noto-sans-cjk-jp, sans-serif;
      font-weight: 700;
      font-style: normal;
      cursor: pointer;
      border-radius: 999px;
      padding: 10px 30px;
      span {
        color: #ffffff;
        font-size: 14px;
      }
      &:hover {
        background-color: #5297ac;
      }
    }
    .another-btn {
      background-color: #e55c6e;
      margin-right: 10px;
      &:hover {
        background-color: #ba3636;
      }
    }
    .dl-btn {
      background-color: #92d4c4;
      margin-left: 10px;
      &:hover {
        background-color: #5297ac;
      }
    }
  }
}
</style>
