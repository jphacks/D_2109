import Vue from "vue";
import App from "./App.vue";
import axios from "axios";
import VueAxios from "vue-axios";

Vue.config.productionTip = false;

Vue.use(VueAxios, axios);

(function (d) {
  var config = {
      kitId: "red3hgc",
      scriptTimeout: 3000,
      async: true,
    },
    h = d.documentElement,
    t = setTimeout(function () {
      h.className = h.className.replace(/\bwf-loading\b/g, "") + " wf-inactive";
    }, config.scriptTimeout),
    tk = d.createElement("script"),
    f = false,
    s = d.getElementsByTagName("script")[0],
    a;
  h.className += " wf-loading";
  tk.src = "https://use.typekit.net/" + config.kitId + ".js";
  tk.async = true;
  tk.onload = tk.onreadystatechange = function () {
    a = this.readyState;
    if (f || (a && a != "complete" && a != "loaded")) return;
    f = true;
    clearTimeout(t);
    try {
      // eslint-disable-next-line no-undef
      Typekit.load(config);
      // eslint-disable-next-line no-empty
    } catch (e) {}
  };
  s.parentNode.insertBefore(tk, s);
})(document);

new Vue({
  render: (h) => h(App),
}).$mount("#app");
