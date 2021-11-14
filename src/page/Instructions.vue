<template>
  <div class="instructions-page">
    <div class="header-menu">
      <div class="left-content">
        <img class="logo" src="../assets/logo.svg" alt="" />
      </div>
      <div class="rigth-btn" @click="ChangePage()">戻る</div>
    </div>
    <div class="instructions-title-container">
      <img class="title-image" src="../assets/instructions_title.svg" alt="" />
      <div class="decoration-border" />
    </div>
    <div class="instructions-content-container">
      <img
        :style="'top:' + sankaku_position + 'px;'"
        class="active-sankaku"
        src="../assets/instructions_sankaku.svg"
        alt=""
      />
      <div class="left-container">
        <div
          class="heading"
          :class="style.first ? 'heading-active' : ''"
          @click="ChangeSection('1')"
        >
          trimとは
        </div>
        <div
          class="heading"
          :class="style.second ? 'heading-active' : ''"
          @click="ChangeSection('2')"
        >
          trimの使い方
        </div>
        <div
          class="heading second-heading"
          :class="style.third ? 'heading-active' : ''"
          @click="ChangeSection('3')"
        >
          I. ルールの作成のしかた
        </div>
        <div
          class="heading second-heading"
          :class="style.fourth ? 'heading-active' : ''"
          @click="ChangeSection('4')"
        >
          II. ルールの適用のしかた
        </div>
      </div>
      <div class="right-container">
        <transition>
          <div class="description" v-if="style.first">
            <div class="description-title">trimとは</div>
            <div class="description-text">
              プログラマーが開発をするときに注意しなければならない、「コーディング規約」や「命名規則」そういった
              <span class="marker-yellow">
                コード上でのエラーではないルールを自動で修正</span
              >してくれる Native/Web アプリケーションです。<br />
              コードに反映するルールはGUIベースのポップなUIで初心者でも簡単に作成できます。<br />
              また、チーム開発の場面ではメンバーごとにあるコーディングのクセや書き方の特徴もチーム単位で綺麗にそろえることで、可読性を高めることができます。
            </div>
            <div class="next-btn-container" @click="ChangeSection('2')">
              <span class="btn-text">「trimの使い方」</span>
              <img
                class="right-arrow-img"
                src="../assets/left_arrow_white.svg"
                alt=""
              />
            </div>
          </div>
          <div class="description" v-if="style.second">
            <div class="description-title">
              trimの使い方は簡単 <span class="marker-yellow">3ステップ</span>
            </div>
            <div class="description-text">
              <div class="list-container">
                <div class="list-number">1.</div>
                <div class="list-text">
                  コードに適用したいルールを選択して、ルールファイルを作成しダウンロード（jsonファイルで出力されます）
                </div>
              </div>
              <div class="border-dash" />
              <div class="list-container">
                <div class="list-number">2.</div>
                <div class="list-text">
                  ダウンロードしたルールファイルを選択 →
                  ルールを適用したいコードを入力。または、適用したいテキストファイルをアップロード
                </div>
              </div>
              <div class="border-dash" />
              <div class="list-container">
                <div class="list-number">3.</div>
                <div class="list-text">
                  ルールファイルに沿って整えられたコードが出力されるのでテキストファイルとしてダウンロード
                </div>
              </div>
            </div>
            <div class="prev-btn-container" @click="ChangeSection('1')">
              <img
                class="left-arrow-img"
                src="../assets/left_arrow_white.svg"
                alt=""
              />
              <span class="btn-text">「trimとは」</span>
            </div>
            <div class="next-btn-container" @click="ChangeSection('3')">
              <span class="btn-text">「trimの使い方」</span>
              <img
                class="right-arrow-img"
                src="../assets/left_arrow_white.svg"
                alt=""
              />
            </div>
          </div>
          <div class="description" v-if="style.third">
            <div class="description-text">
              <img
                src="../assets/Instructions_rule.gif"
                class="image-preview"
              >
              <div class="list-container">
                <div class="list-number">1.</div>
                <div class="list-text">
                  コードに適用したいルールを選択して、ルールファイルを作成しダウンロード（jsonファイルで出力されます）
                </div>
              </div>
              <div class="list-container">
                <div class="list-number">2.</div>
                <div class="list-text">
                  ダウンロードしたルールファイルを選択 →
                  ルールを適用したいコードを入力。または、適用したいテキストファイルをアップロード
                </div>
              </div>
            </div>
            <div class="prev-btn-container" @click="ChangeSection('2')">
              <img
                class="left-arrow-img"
                src="../assets/left_arrow_white.svg"
                alt=""
              />
              <span class="btn-text">「trimの使い方」</span>
            </div>
            <div class="next-btn-container" @click="ChangeSection('4')">
              <span class="btn-text">「ルールの適用」</span>
              <img
                class="right-arrow-img"
                src="../assets/left_arrow_white.svg"
                alt=""
              />
            </div>
          </div>
          <div class="description" v-if="style.fourth">
            <div class="description-text">
              <img
                src="../assets/Instructions_menu.gif"
                class="image-preview"
              >
              <div class="list-container">
                <div class="list-number">1.</div>
                <div class="list-text">
                  作成したルールファイルの中から、適用したいものを選択
                </div>
              </div>
              <div class="list-container">
                <div class="list-number">2.</div>
                <div class="list-text">
                  ルールを適用したコードをテキストファイルで読み込むか、コードをそのまま入力するかを選択
                </div>
              </div>
              <div class="list-container">
                <div class="list-number">3.</div>
                <div class="list-text">
                  整えられたコードが出力されるのでファイルをダウンロード
                </div>
              </div>
            </div>
            <div class="prev-btn-container" @click="ChangeSection('3')">
              <img
                class="left-arrow-img"
                src="../assets/left_arrow_white.svg"
                alt=""
              />
              <span class="btn-text">「ルールの作成」</span>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "InstructionsPage",
  props: {
    open_page: String,
  },
  data() {
    return {
      sankaku_position: 53,
      style: {
        first: true,
        second: false,
        third: false,
        fourth: false,
      },
    };
  },
  created() {},
  computed: {},
  mounted() {},
  methods: {
    ChangePage() {
      this.$emit("changePage", { page: this.open_page });
    },
    ChangeSection(target) {
      if (target === "1") {
        this.style.first = true;
        this.style.second = false;
        this.style.third = false;
        this.style.fourth = false;
        this.sankaku_position = 53;
      } else if (target === "2") {
        this.style.first = false;
        this.style.second = true;
        this.style.third = false;
        this.style.fourth = false;
        this.sankaku_position = 80;
      } else if (target === "3") {
        this.style.first = false;
        this.style.second = false;
        this.style.third = true;
        this.style.fourth = false;
        this.sankaku_position = 105;
      } else if (target === "4") {
        this.style.first = false;
        this.style.second = false;
        this.style.third = false;
        this.style.fourth = true;
        this.sankaku_position = 131;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.instructions-page {
  width: 100%;
  height: 100%;
  background-color: #f7f6e5;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  .header-menu {
    background-color: #faf9f1;
    width: 100%;
    height: 80px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    position: absolute;
    top: 0px;
    z-index: 5000;
    .left-content {
      padding-left: 25px;
      display: flex;
      flex-direction: row;
      justify-content: space-evenly;
      align-items: center;
      .logo {
        height: 50px;
        margin-right: 20px;
      }
      .btn_container {
        cursor: pointer;
        margin: 0 10px;
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
        }
      }
    }
    .rigth-btn {
      font-family: noto-sans-cjk-jp, sans-serif;
      font-weight: 700;
      font-style: normal;
      cursor: pointer;
      background-color: #6f6f6f;
      width: 120px;
      height: 50px;
      border-radius: 999px;
      margin-right: 50px;
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      color: #ffffff;
      font-size: 17px;
      &:hover {
        background-color: #434343;
      }
    }
  }
  .instructions-title-container {
    width: 365px;
    height: 45px;
    margin: 30px 0px 20px 0px;
    position: relative;
    .title-image {
      position: absolute;
      z-index: 1500;
    }
    .decoration-border {
      background-color: #fc9f81;
      width: 180px;
      height: 10px;
      position: absolute;
      z-index: 1000;
      right: -5px;
      bottom: -5px;
    }
  }
  .instructions-content-container {
    width: 800px;
    height: 350px;
    background-image: url("../assets/book_bg.png");
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    position: relative;
    .active-sankaku {
      width: 10px;
      height: 10px;
      position: absolute;
      left: 50px;
      transition: 0.2s;
    }
    .left-container {
      width: 190px;
      height: 270px;
      position: absolute;
      left: 70px;
      .heading {
        cursor: pointer;
        color: #d1c2ba;
        height: 20px;
        margin: 7px 0;
        transition: 0.2s;
      }
      .second-heading {
        font-size: 13px;
        margin-left: 5px;
      }
      .heading-active {
        color: #5e4c43;
      }
    }
    .right-container {
      width: 400px;
      height: 300px;
      position: absolute;
      right: 60px;
      .description {
        width: 100%;
        height: 100%;
        color: #5e4c43;
        .description-title {
          font-size: 18px;
          margin-bottom: 10px;
        }
        .description-text {
          font-size: 12px;
          font-weight: 600;
          line-height: 25px;
          .image-preview {
            width: 400px;
            height: 130px;
            margin-bottom: 10px;
          }
          .list-container {
            display: flex;
            flex-direction: row;
            justify-content: flex-start;
            align-items: flex-start;
            .list-number {
              width: 25px;
            }
            .list-text {
              width: 375px;
            }
          }
          .border-dash {
            width: 100%;
            height: 1px;
            margin: 10px 0;
            border: 1px dashed #8a7469;
          }
        }
        .prev-btn-container {
          cursor: pointer;
          display: flex;
          flex-direction: row;
          justify-content: center;
          align-items: center;
          position: absolute;
          left: -10px;
          bottom: 0px;
          .btn-text {
            color: #8a7469;
            vertical-align: middle;
          }
          .left-arrow-img {
            width: 26px;
            height: 26px;
            padding: 6px;
            border-radius: 999px;
            background-color: #8a7469;
            position: relative;
            top: -2px;
          }
        }
        .next-btn-container {
          cursor: pointer;
          display: flex;
          flex-direction: row;
          justify-content: center;
          align-items: center;
          position: absolute;
          right: -10px;
          bottom: 0px;
          .btn-text {
            color: #8a7469;
            vertical-align: middle;
          }
          .right-arrow-img {
            width: 26px;
            height: 26px;
            padding: 6px;
            border-radius: 999px;
            background-color: #8a7469;
            transform: rotate(180deg);
            position: relative;
            top: -2px;
          }
        }
      }
    }
  }
}
.marker-yellow {
  background: linear-gradient(
    transparent 50%,
    #f6f23a 50%,
    #f6f23a 80%,
    transparent 100%
  );
}

.v-enter-active,
.v-leave-active {
  transition: opacity 0.1s;
}
.v-enter,
.v-leave-to {
  opacity: 0;
}
</style>
