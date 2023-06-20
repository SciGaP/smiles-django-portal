<template>
  <div>
    <b-alert variant="warning" v-model="showAlert">
      Experimental Data Product is not found
    </b-alert>
    <div v-if="item">
      <b-container fluid>
        <b-row class="m-4">
          <b-col cols="6" class="d-flex">
            <b-card class="d-flex justify-content-center align-items-center w-100 h-100 m-0 p-0">
              <molecular-structure-img :structure="item.structure" fit-to-content/>
            </b-card>
          </b-col>

          <b-col cols="6">
            <b-row>
              <b-col cols="8">
                <b-card>
                  <div class="dp-row">
                    <div class="dp-key">Family</div>
                    <div class="dp-value">{{ item.dye_family }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Names</div>
                    <div class="dp-value">
                      <div v-for="(name, index) in item.other_names" :key="index">
                        {{ name }}
                      </div>
                    </div>
                  </div>
                </b-card>
              </b-col>
              <b-col cols="4">
                <b-card>
                  <div class="font-weight-bold" style="margin-bottom: 10px;">Related Data</div>
                  <a href="url">Molecule 1 V1</a><br/>
                  <a href="url">Molecule 1 V2</a>
                </b-card>
              </b-col>
            </b-row>
            <b-row>
              <b-col>
                <b-card class="card-component">
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
              </b-col>
            </b-row>
          </b-col>
        </b-row>


        <b-row class="m-4">
          <b-col cols="6">
            <b-card class="card-component">
              <template #header>
                <h4 class="mb-0">Properties</h4>
              </template>
              <div class="dp-row">
                <div class="dp-key">Mol ID</div>
                <div class="dp-value">{{ item.mol_id }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">CAS Number</div>
                <div class="dp-value">{{ item.cas_nr }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">MW</div>
                <div class="dp-value">{{ item.mw }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">MW Source</div>
                <div class="dp-value">{{ item.color_uv }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">MW Mono ISO</div>
                <div class="dp-value">{{ item.mw_monoiso }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">RDB</div>
                <div class="dp-value">{{ item.rdb }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Validated By</div>
                <div class="dp-value">{{ item.validated_by }}</div>
              </div>
            </b-card>
          </b-col>
        </b-row>

        <b-row class="m-4">
          <b-col cols="6">
            <b-card v-if="item.structural_data" class="card-component">
              <template #header>
                <h4 class="mb-0">Structural Data</h4>
              </template>
              <div class="dp-row">
                <div class="dp-key">SMILES</div>
                <div class="dp-value">{{ item.structural_data.smiles }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">SMILES Stereo</div>
                <div class="dp-value">{{ item.structural_data.smiles_stereo }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Inchi</div>
                <div class="dp-value">{{ item.structural_data.inchi }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Molecular File Blob Source</div>
                <div class="dp-value">{{ item.structural_data.molfile_blob_source }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Emp. Formula</div>
                <div class="dp-value">{{ item.structural_data.emp_formula }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Emp. Formula Sort</div>
                <div class="dp-value">{{ item.structural_data.emp_formula_sort }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Emp. Formula Sorcce</div>
                <div class="dp-value">{{ item.structural_data.emp_formula_source }}</div>
              </div>
            </b-card>
          </b-col>
        </b-row>

        <b-row class="m-4">
          <b-col cols="6">
            <b-card v-if="item.spectral_data" class="card-component">
              <template #header>
                <h4 class="mb-0">Spectral Data</h4>
              </template>
              <div class="dp-row">
                <div class="dp-key">State ofmat</div>
                <div class="dp-value">{{ item.spectral_data.state_ofmat }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Color White</div>
                <div class="dp-value">{{ item.spectral_data.color_white }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Color UV</div>
                <div class="dp-value">{{ item.spectral_data.color_uv }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Absorb Max</div>
                <div class="dp-value">{{ item.spectral_data.absorb_max }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Solvent AE</div>
                <div class="dp-value">{{ item.spectral_data.solvent_ae }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Absorb</div>
                <div class="dp-value">{{ item.spectral_data.absorb }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Conc</div>
                <div class="dp-value">{{ item.spectral_data.conc }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">extinc</div>
                <div class="dp-value">{{ item.spectral_data.extinc }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Emission Max</div>
                <div class="dp-value">{{ item.spectral_data.emis_max }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Absolute Temperature</div>
                <div class="dp-value">{{ item.spectral_data.temp_abs }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Emission QY</div>
                <div class="dp-value">{{ item.spectral_data.emis_qy }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Temperature EMS</div>
                <div class="dp-value">{{ item.spectral_data.temp_ems }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Lifetime</div>
                <div class="dp-value">{{ item.spectral_data.lifetime }}</div>
              </div>
            </b-card>
          </b-col>
        </b-row>
      </b-container>
    </div>
  </div>
</template>

<script>
import MolecularStructureImg from "@/components/common/MolecularStructureImg";

const {utils} = AiravataAPI;

export default {
  props: {
    dp: Object
  },
  components: {
    MolecularStructureImg
  },
  data() {
    return {
      item: null,
      showAlert: false
    };
  },
  mounted() {
    if (!this.item) {
      this.fetchData();
    } else {
      this.item = this.dp;
    }
  },
  methods: {
    fetchData() {
      utils.FetchUtils.get(`/smiles/exp-dp/${this.$route.params.id}`)
          .then(response => this.item = response)
          .catch((e) => {
            if (e.details && e.details.status === 404) {
              this.showAlert = true;
              this.redirectToHome();
            }
          });
    },
    redirectToHome() {
      setTimeout(() => {
        this.$router.push({name: 'data-product-list', query: {type: 'exp'}});
      }, 3000);
    }
  }
}
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
}

.card-component {
  margin-bottom: 20px;
}
</style>

