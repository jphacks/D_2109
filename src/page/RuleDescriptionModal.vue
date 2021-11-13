<template>
  <div class="rule-descriptiont-modal">
    <div class="description-card-container">
      <div class="title-container">
        <img :src="title_bg_path" class="title-bg" />
        <span class="title-text">
          {{ title }}
        </span>
      </div>
      <div class="description-scroll-container">
        <div
          class="description-container"
          v-for="desctiption in desctiptions"
          :key="desctiption.id"
        >
          <img :src="desctiption.image_path" alt="" class="description-img" />
          <div class="description-text-container">
            <div class="description-header">
              {{ desctiption.title }}
            </div>
            <div class="description-text" v-html="desctiption.text">
              <!-- {{ desctiption.text }} -->
            </div>
          </div>
        </div>
      </div>
      <div class="code-preview-container">
        <div class="content-container">
          <span>before</span>
          <code-viewer class="code-viewer" :code_list="code_before" />
        </div>
        <div class="content-container">
          <span>after</span>
          <code-viewer class="code-viewer" :code_list="code_after" />
        </div>
      </div>
      <div class="close-btn" @click="RuleDescriptionModal('0')">
        <img src="../assets/close_button.svg" alt="" />
        <span>閉じる</span>
      </div>
    </div>
  </div>
</template>

<script>
import CodeViewer from "../components/CodeViewer.vue";

export default {
  name: "RuleDescriptiontModal",
  props: {
    title: String,
    title_bg_path: String,
    desctiptions: Array,
    code_before: String,
    code_after: String,
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
    RuleDescriptionModal(target) {
      this.$emit("RuleDescriptionModal", { index: target });
    },
  },
};
</script>

<style lang="scss" scoped>
.rule-descriptiont-modal {
  width: 100vw;
  height: 100vh;
  background-color: #0e0e0ede;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: absolute;
  z-index: 10000;
  .description-card-container {
    width: 800px;
    height: 500px;
    padding: 30px;
    border-radius: 7px;
    background-color: #e8e4d9;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: relative;
    .title-container {
      width: 100%;
      height: 50px;
      margin-bottom: 15px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: flex-start;
      position: relative;
      .title-bg {
        width: 280px;
        height: 75px;
        position: absolute;
      }
      .title-text {
        padding-left: 45px;
        color: #7c5510;
        font-size: 14px;
        font-weight: 600;
        position: absolute;
      }
    }
    .description-scroll-container {
      width: 100%;
      height: 90px;
      overflow-y: scroll;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      align-items: center;
      .description-container {
        width: 100%;
        height: 105px;
        margin: 10px 0;
        padding-right: 10px;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        .description-img {
          width: 115px;
          height: 70px;
        }
        .description-text-container {
          width: 620px;
          height: 70px;
          margin-left: 25px;
          color: #313131;
          flex-direction: row;
          justify-content: flex-start;
          align-items: flex-start;
          .description-header {
            font-weight: 600;
          }
          .description-text {
            font-size: 12px;
          }
        }
      }
    }
    .code-preview-container {
      width: 100%;
      height: 250px;
      margin-top: 10px;
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      align-items: center;
      .content-container {
        width: 49%;
        height: 250px;
        margin-top: 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        span {
          width: 100%;
          margin: 5px;
          display: flex;
          justify-content: flex-start;
          align-items: center;
        }
        .code-viewer {
          width: 100%;
          height: 100%;
        }
      }
    }
    .close-btn {
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      position: absolute;
      right: -70px;
      top: 0px;
      span {
        color: #ffffff;
        margin-top: 5px;
        font-size: 15px;
      }
    }
  }
}
</style>
