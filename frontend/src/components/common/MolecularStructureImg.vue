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
      type: String,
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
    if (!structureData) {
      return fallbackStructure; 
      }
    return "data:image/png;base64," + structureData;
    }    
  }
}
</script>

<style scoped>
</style>