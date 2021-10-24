<template>
  <div id="app">
    <start-page v-if="disp_flag.start_page" />
    <trim-select v-if="disp_flag.trim_select_page" />
    <direct-code-edit v-if="disp_flag.direct_code_edit_page" />
    <loading v-if="disp_flag.loading_page" />
    <code-gen-complete v-if="disp_flag.code_gen_complete_page" />
  </div>
</template>

<script>
import StartPage from "./page/StartPage.vue";
import TrimSelect from "./page/TrimSelect.vue";
import DirectCodeEdit from "./page/DirectCodeEdit.vue";
import Loading from "./page/Loading.vue";
import CodeGenComplete from "./page/CodeGenComplete.vue";

export default {
  name: "App",
  components: {
    StartPage,
    TrimSelect,
    DirectCodeEdit,
    Loading,
    CodeGenComplete,
  },
  data() {
    return {
      disp_code: {
        1: "import math",
        2: "def function ( ) :",
        3: "    return True",
      },
      disp_flag: {
        start_page: false,
        trim_select_page: false,
        direct_code_edit_page: true,
        loading_page: false,
        code_gen_complete_page: false,
        code_viewer: false,
      },
    };
  },
  created() {},
  computed: {},
  methods: {},
};
</script>

<style lang="scss">
#app {
  width: 100vw;
  height: 100vh;
  color: #212020;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
