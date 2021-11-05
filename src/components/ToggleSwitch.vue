<template>
  <div
    class="toggle-switch"
    :class="status ? 'active-bg' : 'nonactive-bg'"
    @click="ChangeStatus()"
  >
    <div
      class="toggle"
      :class="status ? 'active-toggle' : 'nonactive-toggle'"
    />
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
  created() {},
  computed: {},
  methods: {
    ChangeStatus() {
      this.$emit("changeStatus");
    },
  },
};
</script>

<style lang="scss">
.toggle-switch {
  cursor: pointer;
  width: 45px;
  height: 28px;
  border-radius: 999px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  transition: 0.3s;
  .toggle {
    width: 24px;
    height: 24px;
    border-radius: 999px;
    background-color: #ffffff;
    position: absolute;
    transition: 0.3s;
  }
}
.active-bg {
  background-color: #d17559;
  .active-toggle {
    left: 19px;
    background-color: #ffffff;
  }
}

.nonactive-bg {
  background-color: #ffffff;
  .nonactive-toggle {
    left: 2px;
    background-color: #d1d1d1;
  }
}
</style>
