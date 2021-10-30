<template>
  <div class="rule-edit-page">
    <header-menu @changePage="ParentChangePage($event)" />
    <div class="title-container">
      <img class="daruma_icon" src="../assets/daruma_blue_icon.svg" alt="" />
      <div class="title">以下の中から適用するルールを選択してください</div>
      <!-- <div class="tile-menu">
        <div class="grid-line-container">
          <img
            :class="tile_style.grid ? 'active' : 'nonactive'"
            class="grid"
            src="../assets/grid_active.svg"
            alt=""
          />
          <img
            :class="tile_style.grid ? 'nonactive' : 'active'"
            class="grid"
            src="../assets/grid_nonactive.svg"
            alt=""
            @click="ChangeGridLine('grid')"
          />
        </div>
        <div class="divider" />
        <div class="grid-line-container line">
          <img
            :class="tile_style.line ? 'active' : 'nonactive'"
            class="line"
            src="../assets/line_active.svg"
            alt=""
          />
          <img
            :class="tile_style.line ? 'nonactive' : 'active'"
            class="line"
            src="../assets/line_nonactive.svg"
            alt=""
            @click="ChangeGridLine('line')"
          />
        </div>
      </div> -->
    </div>
    <div class="rule-list-container">
      <div class="grid-list-container" v-if="tile_style.grid">
        <div
          class="grid-card"
          v-for="card_data in grig_card_data"
          :key="card_data.id"
        >
          <img class="card-bg" :src="card_data.bg_image" alt="" />
          <div class="card-description">
            <p class="card-title">{{ card_data.title }}</p>
            <div class="description-img-container">
              <div
                class="img-container"
                v-for="image in card_data.images"
                :key="image.id"
              >
                <img :src="image.path" alt="" />
                <p class="img-text">{{ image.text }}</p>
              </div>
            </div>
            <p class="etc-text">
              {{ card_data.etc_text }}
            </p>
          </div>
        </div>
      </div>
      <div class="line-list-container" v-else>
        <!-- タイトル -->
        <span class="card-title">スタイルに関するルール</span>
        <!-- カード -->
        <div class="card-container">
          <div class="image-container">
            <img class="card-image-bg" src="../assets/card_blue.svg" alt="" />
            <img
              class="card-image"
              src="../assets/line_count_small.svg"
              alt=""
            />
          </div>
          <div class="description-container">
            <p class="title">一行あたりの文字数</p>
            <p class="description">一行あたりの文字数を決めます。</p>
          </div>
          <div class="input-container">
            <input
              type="number"
              v-model="rule_json.style_check.count_word.length"
            />
            <p>文字</p>
          </div>
        </div>
        <div class="card-container">
          <div class="image-container">
            <img class="card-image-bg" src="../assets/card_blue.svg" alt="" />
            <img class="card-image" src="../assets/methods_height.svg" alt="" />
          </div>
          <div class="description-container">
            <p class="title">クラス・グローバル関数間の間隔</p>
            <p class="description">
              クラス・グローバル関数ブロックの上下を2行空けるかを決めます。
            </p>
          </div>
          <div class="input-container">
            <input
              type="checkbox"
              v-model="
                rule_json.style_check.line_space.class_or_global_func.action
              "
            />
            <p></p>
          </div>
        </div>
        <div class="card-container">
          <div class="image-container">
            <img class="card-image-bg" src="../assets/card_blue.svg" alt="" />
            <img class="card-image" src="../assets/def_height.svg" alt="" />
          </div>
          <div class="description-container">
            <p class="title">メソッドブロック間の間隔</p>
            <p class="description">
              メソッドブロックの上下を1行空けるかを決めます。
            </p>
          </div>
          <div class="input-container">
            <input
              type="checkbox"
              v-model="rule_json.style_check.line_space.method.action"
            />
            <p></p>
          </div>
        </div>
        <!-- タイトル -->
        <span class="card-title">importに関するルール</span>
        <!-- カード -->
        <div class="card-container">
          <div class="image-container">
            <img class="card-image-bg" src="../assets/card_red.svg" alt="" />
            <img class="card-image" src="../assets/grouping_small.svg" alt="" />
          </div>
          <div class="description-container">
            <p class="title">グルーピング</p>
            <p class="description">
              インポートを種類によって、振り分けを行う機能です。
            </p>
          </div>
          <div class="input-container">
            <input type="checkbox" v-model="rule_json.import_check.grouping" />
          </div>
        </div>
        <div class="card-container">
          <div class="image-container">
            <img class="card-image-bg" src="../assets/card_red.svg" alt="" />
            <img class="card-image" src="../assets/alphabet.svg" alt="" />
          </div>
          <div class="description-container">
            <p class="title">アルファベット順並び替え</p>
            <p class="description">アルファベット順に並び替える機能です。</p>
          </div>
          <div class="input-container">
            <input type="checkbox" v-model="rule_json.import_check.sorting" />
          </div>
        </div>
        <!-- タイトル -->
        <span class="card-title">空白に関するルール</span>
        <!-- カード -->
        <div class="card-container">
          <div class="image-container">
            <img class="card-image-bg" src="../assets/card_yellow.svg" alt="" />
            <img class="card-image" src="../assets/margin.svg" alt="" />
          </div>
          <div class="description-container">
            <p class="title">予約語や変数間の空白</p>
            <p class="description">
              classや関数、演算子前後を空白で整形する機能です。
            </p>
          </div>
          <div class="input-container">
            <input
              type="checkbox"
              v-model="rule_json.style_check.blank_format.action"
            />
          </div>
        </div>
        <!-- タイトル -->
        <span class="card-title">命名規則に関するルール</span>
        <!-- カード -->
        <div class="card-container">
          <div class="image-container">
            <img class="card-image-bg" src="../assets/card_green.svg" alt="" />
            <img class="card-image" src="../assets/cap_snake.svg" alt="" />
          </div>
          <div class="description-container">
            <p class="title">classの命名規則</p>
            <p class="description">classの命名規則を決めます。</p>
            <p class="description">
              チェック時：CapWords | 未チェック時：Snake
            </p>
          </div>
          <div class="input-container">
            <input
              type="checkbox"
              v-model="rule_json.naming_check.class_case.snake"
            />
          </div>
        </div>
        <div class="card-container">
          <div class="image-container">
            <img class="card-image-bg" src="../assets/card_green.svg" alt="" />
            <img class="card-image" src="../assets/cap_snake.svg" alt="" />
          </div>
          <div class="description-container">
            <p class="title">関数の命名規則</p>
            <p class="description">関数の命名規則を決めます。</p>
            <p class="description">
              チェック時：CapWords | 未チェック時：Snake
            </p>
          </div>
          <div class="input-container">
            <input
              type="checkbox"
              v-model="rule_json.naming_check.method_case.snake"
            />
          </div>
        </div>
        <div class="card-container">
          <div class="image-container">
            <img class="card-image-bg" src="../assets/card_green.svg" alt="" />
            <img class="card-image" src="../assets/cap_snake.svg" alt="" />
          </div>
          <div class="description-container">
            <p class="title">変数の命名規則</p>
            <p class="description">変数の命名規則を決めます。</p>
            <p class="description">
              チェック時：CapWords | 未チェック時：Snake
            </p>
          </div>
          <div class="input-container">
            <input
              type="checkbox"
              v-model="rule_json.naming_check.value_case.snake"
            />
          </div>
        </div>
      </div>
    </div>
    <div class="rule-input-compleat-btn" @click="CodeSubmit()">
      <span>ルールの選択を完了する</span>
    </div>
  </div>
</template>

<script>
import HeaderMenu from "../components/HeaderMenu.vue";

export default {
  name: "RuleEditPage",
  components: {
    HeaderMenu,
  },
  data() {
    return {
      rule_json: {
        style_check: {
          blank_format: {
            action: true,
          },
          indent: {
            type: " ",
            num: 4,
            tab_num: 4,
          },
          count_word: {
            action: true,
            length: 80,
          },
          line_space: {
            class_or_global_func: {
              action: true,
            },
            method: {
              action: true,
            },
          },
        },
        naming_check: {
          class_case: {
            snake: true,
            CapWords: false,
          },
          method_case: {
            snake: true,
            CapWords: false,
          },
          value_case: {
            snake: false,
            CapWords: true,
          },
        },
        import_check: {
          grouping: true,
          sorting: true,
        },
      },
      tile_style: {
        grid: false,
        line: true,
      },
      // grig_card_data: [
      //   {
      //     bg_image: require("../assets/card_blue.svg"),
      //     title: "スタイルに関するルール",
      //     images: [
      //       {
      //         path: require("../assets/line_count_small.svg"),
      //         text: "1行の文字数",
      //       },
      //       {
      //         path: require("../assets/class_height_small.svg"),
      //         text: "クラス間隔",
      //       },
      //     ],
      //     etc_text: "など",
      //   },
      //   {
      //     bg_image: require("../assets/card_red.svg"),
      //     title: "importに関するルール",
      //     images: [
      //       {
      //         path: require("../assets/grouping_small.svg"),
      //         text: "グルーピング",
      //       },
      //       {
      //         path: require("../assets/alphabet_small.svg"),
      //         text: "アルファベット順",
      //       },
      //     ],
      //     etc_text: "",
      //   },
      //   {
      //     bg_image: require("../assets/card_yellow.svg"),
      //     title: "空白に関するルール",
      //     images: [
      //       {
      //         path: require("../assets/margin.svg"),
      //         text: "空白チェック",
      //       },
      //     ],
      //     etc_text: "",
      //   },
      //   {
      //     bg_image: require("../assets/card_green.svg"),
      //     title: "命名規則に関するルール",
      //     images: [
      //       {
      //         path: require("../assets/capwords.svg"),
      //         text: "CapWords形式",
      //       },
      //       {
      //         path: require("../assets/snake_case.svg"),
      //         text: "スネークケース",
      //       },
      //     ],
      //     etc_text: "",
      //   },
      //   {
      //     bg_image: require("../assets/card_orange.svg"),
      //     title: "インデントに関するルール",
      //     images: [
      //       {
      //         path: require("../assets/tab_indent.svg"),
      //         text: "Tabキー",
      //       },
      //       {
      //         path: require("../assets/space_indent.svg"),
      //         text: "半角スペース",
      //       },
      //     ],
      //     etc_text: "",
      //   },
      // ],
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
    ParentChangePage(target) {
      this.$emit("changePage", { page: target.page });
    },
    CodeSubmit() {
      this.JsonValidation();
      this.$emit("ruleGen", { rule: this.rule_json });
    },
    JsonValidation() {
      this.rule_json.naming_check.class_case.CapWords =
        !this.rule_json.naming_check.class_case.snake;
      this.rule_json.naming_check.method_case.CapWords =
        !this.rule_json.naming_check.method_case.snake;
      this.rule_json.naming_check.value_case.CapWords =
        !this.rule_json.naming_check.value_case.snake;
    },
  },
};
</script>

<style lang="scss" scoped>
.rule-edit-page {
  width: 100%;
  height: 100%;
  background-color: #dce7e4;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  .title-container {
    margin-bottom: 20px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    position: relative;
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
    .tile-menu {
      height: 60px;
      width: 120px;
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      position: absolute;
      right: -170px;
      .grid-line-container {
        width: 60px;
        height: 60px;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        img {
          cursor: pointer;
          width: 30px;
          height: 30px;
          position: absolute;
        }
        .active {
          opacity: 1;
        }
        .nonactive {
          opacity: 0;
        }
      }
      .divider {
        width: 2px;
        height: 30px;
        background-color: #000000;
        border-radius: 999px;
      }
    }
  }
  .rule-list-container {
    width: 80%;
    min-width: 750px;
    height: 400px;
    border-radius: 7px;
    box-shadow: inset 5px 5px 10px #cdd7d4, inset -5px -5px 10px #ebf7f4;
    .grid-list-container {
      width: 100%;
      height: 100%;
      overflow: scroll;
      padding: 5px;
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      flex-wrap: wrap;
      .grid-card {
        margin: 10px;
        width: 300px;
        height: 180px;
        position: relative;
        .card-bg {
          width: 100%;
          height: 100%;
          position: absolute;
          z-index: 1000;
        }
        .card-description {
          cursor: pointer;
          width: 100%;
          height: 100%;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          position: absolute;
          z-index: 2000;
          &:hover {
            box-shadow: 0px 7px 10px -5px rgba(0, 0, 0, 0.6);
          }
          .card-title {
            color: #7c5510;
            margin-top: 10px;
            font-size: 15px;
          }
          .description-img-container {
            width: 100%;
            height: 100px;
            margin: 9px 0 1px 0;
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            .img-container {
              margin: 0 10px;
              display: flex;
              flex-direction: column;
              justify-content: center;
              align-items: center;
              .img-text {
                color: #313131;
                margin-top: 5px;
                font-size: 15px;
              }
            }
          }
          .etc-text {
            width: 100%;
            height: 22px;
            color: #7c5510;
            font-size: 15px;
            padding-right: 20px;

            display: flex;
            justify-content: flex-end;
            align-items: center;
          }
        }
      }
    }
    .line-list-container {
      width: 100%;
      height: 100%;
      overflow: scroll;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      align-items: center;
      .card-title {
        color: #7c5510;
        font-size: 15px;
        padding: 25px 0 10px 0;
      }
      .card-container {
        width: 90%;
        min-width: 650px;
        height: 130px;
        margin: 10px;
        background-color: #fbfcec;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        box-shadow: 0px 3px 7px #0000001a;
        .image-container {
          width: 220px;
          height: 130px;
          display: flex;
          justify-content: center;
          align-items: center;
          position: relative;
          .card-image-bg {
            width: 200px;
            height: 120px;
            position: absolute;
          }
          .card-image {
            width: 150px;
            height: 90px;
            position: absolute;
          }
        }
        .description-container {
          width: 370px;
          height: 130px;
          display: flex;
          flex-direction: column;
          justify-content: flex-start;
          align-items: flex-start;
          .title {
            font-size: 17px;
            margin: 15px 0;
          }
          .description {
            font-size: 15px;
          }
        }
        .input-container {
          width: 130px;
          height: 130px;
          display: flex;
          justify-content: center;
          align-items: center;
          input[type="number"] {
            width: 60px;
            height: 70px;
            font-size: 20px;
            text-align: right;
            outline: none;
            border: 2px solid #b0b0b0;
            border-radius: 10px;
          }
          input[type="checkbox"] {
            cursor: pointer;
            width: 20px;
            height: 20px;
            border-radius: 999px;
            font-size: 20px;
            text-align: right;
            outline: none;
            border: 2px solid #b0b0b0;
            border-radius: 10px;
          }
          p {
            font-size: 15px;
            margin-left: 10px;
          }
        }
      }
    }
  }
  .rule-input-compleat-btn {
    font-family: noto-sans-cjk-jp, sans-serif;
    font-weight: 700;
    font-style: normal;
    cursor: pointer;
    border-radius: 999px;
    padding: 10px 30px;
    position: absolute;
    bottom: 90px;
    background-color: #92d4c4;
    span {
      color: #ffffff;
      font-size: 14px;
    }
    &:hover {
      background-color: #5297ac;
    }
  }
}
</style>
