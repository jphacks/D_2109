<template>
  <div id="app">
    <start-page v-if="disp_flag.start_page" @changePage="ChangePage($event)" />
    <file-code-select-modal
      v-if="disp_flag.file_code_select_modal"
      @changePage="ChangePage($event)"
      @fileSelect="RuleFileSelect($event)"
    />
    <trim-select
      v-if="disp_flag.trim_select_page"
      @changePage="ChangePage($event)"
      @fileSelect="PythonFileSelect($event)"
    />
    <direct-code-edit
      v-if="disp_flag.direct_code_edit_page"
      @changePage="ChangePage($event)"
      @codeGen="LoadingWaitTime()"
    />
    <loading v-show="disp_flag.loading_page" />
    <code-gen-complete
      v-if="disp_flag.code_gen_complete_page"
      @changePage="ChangePage($event)"
    />
    <rule-edit v-if="disp_flag.rule_edit_page" @changePage="ChangePage($event)"/>
    <rule-make-loading v-if="disp_flag.rule_make_loading" @changePage="ChangePage($event)"/>
    <rule-gen-complete v-if="disp_flag.rule_gen_complete" @changePage="ChangePage($event)"/>
  </div>
</template>

<script>
import StartPage from "./page/StartPage.vue";
import FileCodeSelectModal from "./page/FileCodeSelectModal.vue";
import TrimSelect from "./page/TrimSelect.vue";
import DirectCodeEdit from "./page/DirectCodeEdit.vue";
import Loading from "./page/Loading.vue";
import CodeGenComplete from "./page/CodeGenComplete.vue";
import RuleEdit from "./page/RuleEdit.vue";
import RuleMakeLoading from "./page/RuleMakeLoading.vue";
import RuleGenComplete from "./page/RuleGenComplete.vue";

export default {
  name: "App",
  components: {
    StartPage,
    TrimSelect,
    FileCodeSelectModal,
    DirectCodeEdit,
    Loading,
    CodeGenComplete,
    RuleEdit,
    RuleMakeLoading,
    RuleGenComplete,
  },
  data() {
    return {
      rule: {},
      input_python: "",
      output_python: "",
      disp_flag: {
        start_page: false,
        file_code_select_modal: false,
        trim_select_page: false,
        direct_code_edit_page: false,
        loading_page: false,
        code_gen_complete_page: false,
        rule_edit_page: false,
        rule_make_loading:true,
        rule_gen_complete: false
      },
    };
  },
  created() {
    // this.ChangePage({ page: "start_page" });
  },
  computed: {},
  methods: {
    PythonFileSelect(file) {
      let json_file = file.file;
      let reader = new FileReader();
      reader.readAsText(json_file);
      reader.onload = function () {
        this.rule = reader.result;
        console.log(this.rule);
      };
    },
    RuleFileSelect(file) {
      let json_file = file.file;
      let reader = new FileReader();
      reader.readAsText(json_file);
      reader.onload = function () {
        this.rule = reader.result;
        console.log(this.rule);
      };
    },
    ChangePage(target) {
      console.log(target);
      this.disp_flag.start_page = false;
      this.disp_flag.file_code_select_modal = false;
      this.disp_flag.trim_select_page = false;
      this.disp_flag.direct_code_edit_page = false;
      this.disp_flag.loading_page = false;
      this.disp_flag.code_gen_complete_page = false;
      this.disp_flag.rule_edit_page = false;
      this.disp_flag.rule_gen_complete = false;
      this.disp_flag.rule_make_loading = false
      this.disp_flag[target.page] = true;
    },
    LoadingWaitTime() {
      console.log("start");
      this.ChangePage({ page: "loading_page" });
      this.sleep(4000).then( (result) =>  {
        console.log(result)
        this.ChangePage({ page: "code_gen_complete_page" });
      });
      console.log("end");
    },
    // 処理を変えるときはここをAPI用の関数に変更
    sleep (time) {
      return new Promise(function (resolve, reject) {
        console.log(reject)
        window.setTimeout(resolve, time);
      });
    },
  },
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

/* A Modern CSS Reset */
*,
*::before,
*::after {
  box-sizing: border-box;
}
body,
h1,
h2,
h3,
h4,
p,
figure,
blockquote,
dl,
dd {
  margin: 0;
}
ul[role="list"],
ol[role="list"] {
  list-style: none;
}
html:focus-within {
  scroll-behavior: smooth;
}
body {
  min-height: 100vh;
  text-rendering: optimizeSpeed;
  line-height: 1.5;
}
a:not([class]) {
  text-decoration-skip-ink: auto;
}
img,
picture {
  max-width: 100%;
  display: block;
}
input,
button,
textarea,
select {
  font: inherit;
}
@media (prefers-reduced-motion: reduce) {
  html:focus-within {
    scroll-behavior: auto;
  }
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
</style>
