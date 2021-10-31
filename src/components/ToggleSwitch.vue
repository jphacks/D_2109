<template>
  <div class="toggle-switch" :class="status ? 'active-bg' : 'nonactive-bg'" @click="ChangeStatus()">
    <div class="toggle" :class="status ? 'active-toggle' : 'nonactive-toggle'"/>
  </div>
</template>

<script>
export default {
  name: "ToggleSwitch",
  components: {},
  props: {
    status: Boolean,
  },
  data() {
    return {};
  },
  watch: {},
  created() {
  },
  computed: {},
  methods: {
    ChangeStatus() {
      this.$emit("changeStatus");
    },
  },
};
</script>

<style lang="scss">
.toggle-switch{
  cursor: pointer;
  width: 30px;
  height: 18px;
  border-radius: 999px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  transition: 0.3s;
  .toggle{
    width: 14px;
    height: 14px;
    border-radius: 999px;
    background-color: #FFFFFF;
    position: absolute;
    transition: 0.3s;
  }
}
.active-bg{
  background-color: #D17559;
  .active-toggle{
    left: 14px;
    background-color: #FFFFFF;
  }
}

.nonactive-bg{
  background-color: #FFFFFF;
  .nonactive-toggle{
    left: 2px;
    background-color: #D1D1D1;
  }
}
</style>
