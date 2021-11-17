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
      @ShowExpansionModal="ShowExpansionModal()"
    />
    <code-expansion-modal
      v-if="disp_flag.code_expansion_modal"
      :output_python="output_python"
      @ShowExpansionModal="ShowExpansionModal()"
    />
    <rule-edit
      v-if="disp_flag.rule_edit_page"
      @changePage="ChangePage($event)"
      @ruleGen="RuleGenLoading($event)"
      @OpenInstructions="OpenInstructions()"
      @RuleDescriptionModal="RuleDescriptionModal($event)"
    />
    <rule-description-modal
      v-if="disp_flag.rule_description_modal"
      :title="disp_description.title"
      :title_bg_path="disp_description.title_bg_path"
      :desctiptions="disp_description.descriptions"
      :code_before="disp_description.before_code"
      :code_after="disp_description.after_code"
      @RuleDescriptionModal="RuleDescriptionModal($event)"
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
import CodeExpansionModal from "./page/CodeExpansionModal.vue";
import RuleEdit from "./page/RuleEdit.vue";
import RuleDescriptionModal from "./page/RuleDescriptionModal.vue";
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
    CodeExpansionModal,
    RuleEdit,
    RuleDescriptionModal,
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
        code_expansion_modal: false,
        rule_edit_page: false,
        rule_description_modal: false,
        rule_make_loading: false,
        rule_gen_complete: false,
        instructions: false,
      },
      disp_description: {},
      description_lists: [
        {
          title: "スタイルに関するルール",
          title_bg_path: require("./assets/stickynote_blue.svg"),
          descriptions: [
            {
              image_path: require("./assets/line_count.svg"),
              title: "1文字あたりの文字数",
              text: "1行あたりの文字数を決めます。文字数を指定することでコードが複雑になることを防ぎ、点検のしやすいキレイなコードを作ることに役立てることが可能です。<br>PEP8では、最大文字数を80文字にすることが推奨されます。<br>trimでは文字数をオーバーして記憶があった場合は警告を表示します。",
            },
          ],
          before_code:
            "customers = Customer.objects.filter(active_flag=False).order_by('id')[:10].values('id', 'name', 'phone', 'mail', 'gender', 'birth_date', 'active_flag')",
          after_code:
            "# [trim] Warning: 1行あたりの行数は最大80文字です.適切な位置で折り返してください.\ncustomers = Customer.objects.filter(active_flag=False).order_by('id')[:10].values('id', 'name', 'phone', 'mail', 'gender', 'birth_date', 'active_flag') ",
        },
        {
          title: "スタイルに関するルール",
          title_bg_path: require("./assets/stickynote_blue.svg"),
          descriptions: [
            {
              image_path: require("./assets/methods_height.svg"),
              title: "クラス・グローバル関数間の間隔（上下の空白行）",
              text: "PEP8に基づき、クラス・グローバル関数ブロックの上下空白行が2行になるように調整します。<br>上下に空白行を生成することでコードが見やすくなります。",
            },
          ],
          before_code:
            "class ValueNaming(Naming):\n    def __init__():\n        super().__init__()\n\ndef add_box(obj):\n    box.append(obj)",
          after_code:
            "class ValueNaming(Naming):\n    def __init__():\n        super().__init__() \n\n\ndef add_box(obj):\n    box.append(obj) ",
        },
        {
          title: "スタイルに関するルール",
          title_bg_path: require("./assets/stickynote_blue.svg"),
          descriptions: [
            {
              image_path: require("./assets/def_height.svg"),
              title: "メソッドブロック間の間隔（上下の空白行）",
              text: "PEP8に基づき、メソッドブロックの上下空白行が1行になるように調整します。<br>上下に空白行を生成することでコードが見やすくなります。",
            },
          ],
          before_code:
            "class Naming():\n    box = []\n\n\n    def __init__():\n        pass\n    def add_box(obj):\n        self.box.append(obj)\n",
          after_code:
            "class Naming():\n    box = [] \n    \n    def __init__():\n        pass \n\n    def add_box(obj):\n        self.box.append(obj)",
        },
        {
          title: "importに関するルール",
          title_bg_path: require("./assets/stickynote_red.svg"),
          descriptions: [
            {
              image_path: require("./assets/grouping.svg"),
              title: "グルーピング",
              text: "モジュールの種類によって以下の間隔でインポートするようにグループ化します。<br>1. 標準ライブラリ → 2. サードパーティ → 3. ローカルライブラリ（自作のライブラリ）<br>グループ化することでモジュールの管理がしやすくなります。<br>これは、PEP8に準拠します。",
            },
          ],
          before_code:
            "import numpy\nimport math\nimport pandas \nfrom local.objects import obj\nimport blob\nfrom matplotlib import pyplot\nfrom method.naming import ValueNaming\nimport os",
          after_code:
            "# [trim] Info: import部に対し、整形を行いました.\nimport math \nimport os \n\nimport blob \nimport numpy \nimport pandas \nfrom matplotlib import pyplot \n\nfrom local.objects import obj \nfrom method.naming import ValueNaming",
        },
        {
          title: "importに関するルール",
          title_bg_path: require("./assets/stickynote_red.svg"),
          descriptions: [
            {
              image_path: require("./assets/alphabet.svg"),
              title: "アルファベット順に並び替え",
              text: "モジュールをアルファベット順に並び替えます。<br>目的のモジュールの発見が容易になるなど、開発の効率化につながります。<br>グループ化機能と組み合わせることで、モジュールをもっとスッキリまとめることができます。",
            },
          ],
          before_code: "import math\nimport os\nimport glob",
          after_code:
            "# [trim] Info: import部に対し、整形を行いました.\nimport glob\nimport math\nimport os",
        },
        {
          title: "空白に関するルール",
          title_bg_path: require("./assets/stickynote_yellow.svg"),
          descriptions: [
            {
              image_path: require("./assets/margin.svg"),
              title: "空白・スペースのチェック",
              text: "PEP8では、演算子前後や関数の引数部、辞書内など様々な場面で空白を置くかどうか？に関するルールがあります。<br>ここでは、このルールに沿って整形するかどうかを設定できます。",
            },
          ],
          before_code:
            "def    add_box(message:   str)  ->    None:\n    self.box.append(message)\n    count    +=  1",
          after_code:
            "def add_box(message:str) -> None:\n    self.box.append(message) \n    count += 1 ",
        },
        {
          title: "命名規則に関するルール",
          title_bg_path: require("./assets/stickynote_green.svg"),
          descriptions: [
            {
              image_path: require("./assets/capwords.svg"),
              title: "CapWords形式",
              text: 'CapWords形式を命名方法に採用します。<br>最初の１文字を大文字、それ以降はキャメルケースにのっとって記述する方法です。<br>キャメルケース：各構成語の先頭を大文字にする形式（<span style="color:#E55C6E;">J</span>ava<span style="color:#E55C6E;">S</span>cript、<span style="color:#E55C6E;">P</span>lay<span style="color:#E55C6E;">S</span>tationなど）',
            },
            {
              image_path: require("./assets/snake_case.svg"),
              title: "snake_case形式",
              text: "snake_case形式を命名方法に採用します。<br>また、プログラミングでは書く要素名にスペース（空白）が使えない場合がほとんど。（× file download）<br>snake_case形式では各構成語を「_」（アンダースコア）で区切って記述します。<br>なお、snake_case形式には大文字を使えません。",
            },
          ],
          before_code:
            "# 関数: snakeケースのみ許容すると仮定\ndef addBox(obj):\n    box.append(obj)",
          after_code:
            "# [trim] Warning: 関数名に大文字は含められません.\ndef addBox(obj):\n    box.append(obj) ",
        },
      ],
    };
  },
  created() {
    this.ChangePage({ page: "start_page" });
  },
  computed: {},
  methods: {
    RuleDescriptionModal(target) {
      this.disp_description = this.description_lists[target.index];
      this.disp_flag.rule_description_modal =
        !this.disp_flag.rule_description_modal;
    },
    ShowExpansionModal() {
      this.disp_flag.code_expansion_modal =
        !this.disp_flag.code_expansion_modal;
    },
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
          new Promise(function (resolve) {
            window.setTimeout(resolve, 1000);
          }).then(() => {
            this.ChangePage({ page: "code_gen_complete_page" });
          });
        })
        .catch((error) => {
          for (let key of Object.keys(error)) {
            console.log(key);
            console.log(error[key]);
          }
          this.output_python = "入力されたソースコードにエラーがあります。";
          new Promise(function (resolve) {
            window.setTimeout(resolve, 1000);
          }).then(() => {
            this.ChangePage({ page: "code_gen_complete_page" });
          });
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
      this.disp_flag.rule_description_modal = false;
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
