<template>
  <div id="app">
    <code-viewer :code_list="disp_code" />
  </div>
</template>

<script>
import CodeViewer from "./components/CodeViewer.vue";

export default {
  name: "App",
  components: {
    CodeViewer,
  },
  data() {
    return {
      disp_code: {
        1: "import math",
        2: "def function ( ) :",
        3: "    return True",
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
