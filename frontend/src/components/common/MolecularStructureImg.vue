<template>
  <b-img
      fluid
      :src="formatImageData(structure)"
      alt="Structure"
      :height="height"
      :width="width"
      :class="{ 'w-100 h-100 object-fit-contain': fitToContent }"
  />
</template>

<script>
import fallbackStructure from "@/assets/images/structure-fallback.svg";

export default {
  props: {
    structure: {
      type: Object,
      required: true
    },
    height: {
      type: String,
      default: "100"
    },
    width: {
      type: String,
      default: "100"
    },
    fitToContent: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    formatImageData(structureData) {
      return structureData
          ? "data:image/svg+xml;base64," + structureData
          : fallbackStructure;
    }
  }
}
</script>

<style scoped>
</style>
