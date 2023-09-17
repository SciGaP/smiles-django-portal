<template>
  <div v-if="item">
    <b-container fluid>
      <b-row>
        <b-card class="w-100 border-0 d-flex justify-content-center align-items-center">
          <molecular-structure-img :structure="item.structure" fit-to-content />
        </b-card>
      </b-row>
      <b-row>
        <b-card class="w-100 border-0 d-flex justify-content-lg-start align-items-start">
          <div class="font-weight-bold" style="margin-bottom: 10px;">Related Data</div>
          <div class="text-left">
            <a href="url">Molecule 1</a><br />
            <a href="url">Molecule 2</a>
          </div>
        </b-card>
      </b-row>
      <b-row>
        <b-card class="w-100 border-0 d-flex justify-content-lg-start align-items-start">
          <div class="dp-row">
            <div class="dp-key">Data Product ID</div>
            <div class="dp-value">{{ item.data_product_id }}</div>
          </div>
          <div class="dp-row">
            <div class="dp-key">Journal</div>
            <div class="dp-value">{{ item.journal }}</div>
          </div>
          <div class="dp-row">
            <div class="dp-key">Author/Created by</div>
            <div class="dp-value">{{ item.auth_of_intr }}</div>
          </div>
          <div class="dp-row">
            <div class="dp-key">Reference</div>
            <div class="dp-value">{{ item.doi_link }}</div>
          </div>
        </b-card>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import MolecularStructureImg from "@/components/common/MolecularStructureImg.vue";

export default {
  components: {
    MolecularStructureImg
  },
  props: {
    dp: Object
  },
  data() {
    return {
      item: null,
      showAlert: false
    };
  },
  mounted() {
    if (this.dp) {
      this.item = this.dp;
    }
  },
  methods: {}
};
</script>

<style scoped>
.dp-row {
  display: flex;
  flex-direction: row;
  margin-bottom: 5px;
}

.dp-key {
  flex: 1;
  font-weight: bold;
}

.dp-value {
  flex: 1;
  color: #666;
  text-align: left;
  word-break: break-all;
}

</style>
