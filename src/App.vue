<template>
  <div id="app">
    <start-page v-if="disp_flag.start_page" />
    <header-menu v-if="disp_flag.header_menu" />
    <code-viewer v-if="disp_flag.code_viewer" :code_list="disp_code" />
  </div>
</template>

<script>
import StartPage from "./components/StartPage.vue";
import CodeViewer from "./components/CodeViewer.vue";
import HeaderMenu from "./components/HeaderMenu.vue";

export default {
  name: "App",
  components: {
    StartPage,
    CodeViewer,
    HeaderMenu,
  },
  data() {
    return {
      disp_code: {
        1: "import math",
        2: "def function ( ) :",
        3: "    return True",
      },
      disp_flag: {
        start_page: true,
        header_menu: false,
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
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
