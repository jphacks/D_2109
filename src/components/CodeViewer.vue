<template>
  <div class="code-viewer">
    <div class="number-container">
      <div class="line_number" v-for="line in lines" :key="line.id">
        {{ line }}
      </div>
    </div>
    <markdown-it-vue
      class="md-body"
      :content="disp_code.code_start + code_list + disp_code.code_end"
    />
  </div>
</template>

<script>
import MarkdownItVue from "markdown-it-vue";

export default {
  name: "code_viewer",
  components: {
    MarkdownItVue,
  },
  props: {
    code_list: String,
  },
  data() {
    return {
      disp_code: {
        code_start: "```python\n",
        code_end: "\n```",
      },
      lines: [],
    };
  },
  watch: {
    code_list: {
      handler: function (val_new) {
        this.lines = [];
        for (let i = 1; i <= val_new.split(/\r?\n/g).length; i++) {
          this.lines.push(i);
        }
      },
    },
  },
  created() {
    this.InitLines();
  },
  computed: {},
  methods: {
    InitLines() {
      for (let i = 1; i <= this.code_list.split(/\r?\n/g).length; i++) {
        this.lines.push(i);
      }
    },
  },
};
</script>

<style lang="scss">
$mainColor: #36cbfa;
.code-viewer {
  border-radius: 5px;
  padding: 10px;
  overflow: scroll;
  background-color: #3b3b3b;
  display: flex;
  flex-direction: row;
  box-shadow: 0px 7px 10px -5px rgba(0, 0, 0, 0.6);
  .number-container {
    width: 30px;
    line-height: 23px;
    font-size: 14px;
    color: #858585;
    .line_number {
      border-right: solid 1px #858585;
      padding-right: 7px;
      display: flex;
      justify-content: flex-end;
      align-items: center;
    }
  }
  .md-body {
    margin-left: 10px;
    .markdown-body {
      pre {
        margin: 0;
        code {
          color: rgb(236, 236, 236);
          font-family: inherit;
          line-height: 23px;
          font-size: 15px;
          .hljs-keyword {
            color: rgb(201, 146, 253);
          }
          .hljs-title {
            color: $mainColor;
          }
          .hljs-attr {
            color: rgb(247, 210, 0);
          }
          .hljs-attribute {
            color: palegreen;
          }
          .hljs-variable {
            color: orange;
          }
          .hljs-selector-class {
            color: rgb(214, 157, 50);
          }
          .hljs-built_in {
            color: #d19719;
          }
          .hljs-symbol {
            color: rgb(18, 167, 253);
          }
          .hljs-number {
            color: rgb(172, 255, 172);
          }
          .hljs-string {
            color: rgb(190, 228, 190);
          }
          .hljs-subst {
            color: rgb(250, 99, 89);
          }
          .hljs-meta {
            color: #6594fa;
          }
        }
      }
    }
  }
}
</style>
