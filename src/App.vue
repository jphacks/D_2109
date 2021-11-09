<template>
  <div id="app">
    <start-page
      v-if="disp_flag.start_page"
      @changePage="ChangePage($event)"
      @OpenInstructions="OpenInstructions()"
    />
    <file-code-select-modal
      v-if="disp_flag.file_code_select_modal"
      @changePage="ChangePage($event)"
      @fileSelect="RuleFileSelect($event)"
    />
    <trim-select
      v-if="disp_flag.trim_select_page"
      @changePage="ChangePage($event)"
      @fileSelect="PythonFileSelect($event)"
      @OpenInstructions="OpenInstructions()"
    />
    <direct-code-edit
      v-if="disp_flag.direct_code_edit_page"
      @changePage="ChangePage($event)"
      @codeGen="CodeGenLoading($event)"
      @OpenInstructions="OpenInstructions()"
    />
    <loading
      v-if="disp_flag.loading_page"
      @changePage="ChangePage($event)"
      @OpenInstructions="OpenInstructions()"
    />
    <code-gen-complete
      v-if="disp_flag.code_gen_complete_page"
      @changePage="ChangePage($event)"
      @downloadItem="PythonFileDownload($event)"
      :input_python="input_python"
      :output_python="output_python"
      @OpenInstructions="OpenInstructions()"
    />
    <rule-edit
      v-if="disp_flag.rule_edit_page"
      @changePage="ChangePage($event)"
      @ruleGen="RuleGenLoading($event)"
      @OpenInstructions="OpenInstructions()"
    />
    <rule-make-loading
      v-if="disp_flag.rule_make_loading"
      @OpenInstructions="OpenInstructions()"
      @changePage="ChangePage($event)"
    />
    <rule-gen-complete
      v-if="disp_flag.rule_gen_complete"
      @changePage="ChangePage($event)"
      @downloadItem="RuleFileDownload($event)"
      @OpenInstructions="OpenInstructions()"
    />
    <instructions
      v-if="disp_flag.instructions"
      @changePage="ChangePage($event)"
      :open_page="instructions_data"
    />
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
import Instructions from "./page/Instructions.vue";

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
    Instructions,
  },
  data() {
    return {
      rule_flag: false,
      rule_file: {},
      input_rule: {},
      python_name: "",
      input_python: "",
      output_python: "",
      instructions_data: "",
      disp_flag: {
        start_page: false,
        file_code_select_modal: false,
        trim_select_page: false,
        direct_code_edit_page: false,
        loading_page: false,
        code_gen_complete_page: false,
        rule_edit_page: false,
        rule_make_loading: false,
        rule_gen_complete: false,
        instructions: false,
      },
    };
  },
  created() {
    this.ChangePage({ page: "start_page" });
  },
  computed: {},
  methods: {
    OpenInstructions() {
      if (this.disp_flag.start_page) {
        this.instructions_data = "start_page";
      } else if (this.disp_flag.file_code_select_modal) {
        this.instructions_data = "file_code_select_modal";
      } else if (this.disp_flag.trim_select_page) {
        this.instructions_data = "trim_select_page";
      } else if (this.disp_flag.direct_code_edit_page) {
        this.instructions_data = "direct_code_edit_page";
      } else if (this.disp_flag.loading_page) {
        this.instructions_data = "loading_page";
      } else if (this.disp_flag.code_gen_complete_page) {
        this.instructions_data = "code_gen_complete_page";
      } else if (this.disp_flag.rule_edit_page) {
        this.instructions_data = "rule_edit_page";
      } else if (this.disp_flag.rule_make_loading) {
        this.instructions_data = "rule_make_loading";
      } else if (this.disp_flag.rule_gen_complete) {
        this.instructions_data = "rule_gen_complete";
      }
      this.ChangePage({ page: "instructions" });
    },
    GetAPIResult() {
      this.axios
        .post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_API_URL_KEY,
          {
            code_lst: this.input_python.split(/\r?\n/g),
            op: this.input_rule,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        )
        .then((response) => {
          let response_python = "";
          console.log(response);
          let python_array = response.data.code_lst;
          python_array.forEach((element) => {
            response_python += element;
          });
          this.output_python = response_python;
          this.ChangePage({ page: "code_gen_complete_page" });
        })
        .catch((error) => {
          for (let key of Object.keys(error)) {
            console.log(key);
            console.log(error[key]);
          }
          this.output_python = "入力されたソースコードにエラーがあります。";
          this.ChangePage({ page: "code_gen_complete_page" });
        });
    },
    PythonFileDownload() {
      const blob = new Blob([this.output_python], {
        type: "text/plain",
        endings: "native",
      });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "trimed" + this.python_name + ".py";
      link.click();
    },
    RuleFileDownload() {
      const blob = new Blob([JSON.stringify(this.rule_file, null, "\t")], {
        type: "application/json",
      });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "rule.json";
      link.click();
    },
    PythonFileSelect(file) {
      this.ChangePage({ page: "loading_page" });
      let json_file = file.file;
      console.log(json_file.name);
      this.python_name = "_" + json_file.name.slice(0, -3);
      let python_reader = new FileReader();
      python_reader.readAsText(json_file);
      python_reader.addEventListener("load", () => {
        this.input_python = python_reader.result;
        this.GetAPIResult();
      });
    },
    RuleFileSelect(file) {
      let json_file = file.file;
      let rule_reader = new FileReader();
      rule_reader.readAsText(json_file);
      rule_reader.addEventListener("load", () => {
        this.input_rule = JSON.parse(rule_reader.result);
        console.log(this.input_rule);
      });
      this.rule_flag = true;
      this.ChangePage({ page: "trim_select_page" });
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
      this.disp_flag.rule_make_loading = false;
      this.disp_flag.instructions = false;
      this.disp_flag[target.page] = true;
      // trim_select_pageを開こうとしているかつ入力ruleが空の場合にModal表示
      if (target.page === "trim_select_page" && this.rule_flag !== true) {
        this.disp_flag.file_code_select_modal = true;
      }
      // trim_select_pageを開いたらファイル名を削除
      if (target.page === "trim_select_page") {
        this.python_name = "";
      }
      // タイトルに戻ったらルール適用状態を解除する
      if (target.page === "start_page") {
        this.rule_flag = false;
      }
    },
    CodeGenLoading(target) {
      this.input_python = target.code;
      this.ChangePage({ page: "loading_page" });
      this.GetAPIResult();
    },
    RuleGenLoading(target) {
      this.ChangePage({ page: "rule_make_loading" });
      this.rule_file = target.rule;
      // 1秒間待機後にページ遷移
      new Promise(function (resolve) {
        window.setTimeout(resolve, 1000);
      }).then(() => {
        this.ChangePage({ page: "rule_gen_complete" });
      });
    },
  },
};
</script>

<style lang="scss">
#app {
  font-family: heisei-maru-gothic-std, sans-serif;
  font-weight: 800;
  font-style: normal;
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
