<template>
  <div class="rule-edit-modal">
    <div class="main-container">
      <div class="modal-title">スタイルに関するルール</div>
      <div class="setting-content-container"></div>
      <div class="modal-btn-container">
        <div class="reset-btn">デフォルト値に戻す</div>
        <div class="save-btn">変更を保存する</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "RuleEditModal",
  components: {},
  data() {
    return {
      tile_style: {
        grid: true,
        line: false,
      },
      grig_card_data: {
        1: {
          title: "スタイルに関するルール",
          items: [
            {
              image: require("../assets/def_height.svg"),
              title: "関数間の行間隔",
              description: "関数間の行間隔を決めます。",
              value: "2",
              unit: "行",
            },
            {
              image: require("../assets/methods_height.svg"),
              title: "メソッド間の行間隔",
              description: "メソッド間の行間隔を決めます。",
              value: "1",
              unit: "行",
            },
            {
              image: require("../assets/methods_height.svg"),
              title: "メソッド間の行間隔",
              description: "メソッド間の行間隔を決めます。",
              value: "1",
              unit: "行",
            },
            {
              image: require("../assets/class_height.svg"),
              title: "クラス間の行間隔",
              description: "クラス間の行間隔を決めます。",
              value: "2",
              unit: "行",
            },
          ],
        },
      },
    };
  },
  created() {},
  computed: {},
  methods: {
    ChangeGridLine(target) {
      this.tile_style.grid = false;
      this.tile_style.line = false;
      this.tile_style[target] = true;
    },
    ChangePage(target) {
      this.$emit("changePage", { page: target });
    },
    ChildChangePage(target) {
      this.$emit("changePage", { page: target.page });
    },
    CodeSubmit() {
      this.$emit("codeGen");
    },
  },
};
</script>

<style lang="scss" scoped>
.rule-edit-modal {
  width: 100vw;
  height: 100vh;
  background-color: #58585866;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: absolute;
  z-index: 10000;
  .main-container {
    width: 80%;
    min-width: 800px;
    height: 600px;
    background-color: #e8e4d9;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: absolute;
    .modal-title {
      width: 250px;
      height: 50px;
      padding-left: 40px;
      color: #7c5510;
      font-size: 15px;
      background-image: url("../assets/husen.svg");
      background-repeat: no-repeat;
      background-position: center;
      background-size: contain;
      display: flex;
      justify-content: flex-start;
      align-items: center;
      position: absolute;
      left: 40px;
      top: 20px;
    }

    .setting-content-container {
      width: 80%;
      min-width: 600px;
      height: 400px;
      border-radius: 10px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      box-shadow: inset 5px 5px 10px #c5c2b8, inset -5px -5px 10px #fffffa;
    }

    .modal-btn-container {
      width: 500px;
      height: 50px;
      display: flex;
      justify-content: center;
      align-items: center;
      position: absolute;
      bottom: 20px;
      .reset-btn {
        cursor: pointer;
        background-color: #6f6f6f;
        padding: 10px 15px;
        margin: 0 20px;
        border-radius: 999px;
        color: #ffffff;
        font-size: 14px;
        display: flex;
        justify-content: center;
        align-items: center;
        &:hover {
          background-color: #434343;
        }
      }
      .save-btn {
        cursor: pointer;
        background-color: #fc9f81;
        padding: 10px 15px;
        margin: 0 20px;
        border-radius: 999px;
        color: #ffffff;
        font-size: 14px;
        display: flex;
        justify-content: center;
        align-items: center;
        &:hover {
          background-color: #ba3636;
        }
      }
    }
  }
}
</style>
