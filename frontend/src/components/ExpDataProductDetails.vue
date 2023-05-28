<template>
  <div>
    <b-alert variant="warning" v-model="showAlert">
      Experimental Data Product is not found
    </b-alert>
    <div v-if="item">
      <b-container fluid>
        <b-row class="m-4">
          <b-col cols="6">
            <b-card style="margin-bottom: 50px;">
              <template #header>
                <h4 class="mb-0">Properties</h4>
              </template>
              <div class="dp-row">
                <div class="dp-key">CAS Number</div>
                <div class="dp-value">{{ item.cas_nr }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Stereo-SMILES</div>
                <div class="dp-value">{{ item.smiles_stereo }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Empirical Formula</div>
                <div class="dp-value">{{ item.emp_formula }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">MW</div>
                <div class="dp-value">{{ item.mw }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Compound Class</div>
                <div class="dp-value">{{ item.comp_class }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Color under white light</div>
                <div class="dp-value">{{ item.color_white }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Color under UV light</div>
                <div class="dp-value">{{ item.color_uv }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Absorption Maxima λmax (nm)</div>
                <div class="dp-value">{{ item.absorb_max }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Absorbance</div>
                <div class="dp-value">{{ item.absorb }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Concentration (mol_L-1)</div>
                <div class="dp-value">{{ item.conc }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Extinction_coefficient ε (M-1 cm-1)</div>
                <div class="dp-value">{{ item.extinc }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Emission_maxima λfl (nm)</div>
                <div class="dp-value">{{ item.emis_max }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Temperature Absorbance (K)</div>
                <div class="dp-value">{{ item.temp_abs }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Emission Quantum yield φ</div>
                <div class="dp-value">{{ item.emis_qy }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Temperature Emission (K)</div>
                <div class="dp-value">{{ item.temp_ems }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Lifetime_(ns)</div>
                <div class="dp-value">{{ item.lifetime }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Temperature CV (K)</div>
                <div class="dp-value">{{ item.temp_cv }}</div>
              </div>
            </b-card>
          </b-col>

          <b-col cols="6">
            <b-row>
              <b-col>
                <b-card style="margin-bottom: 50px;">
                  <div class="dp-row">
                    <div class="dp-key">Family</div>
                    <div class="dp-value">Family</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Formula</div>
                    <div class="dp-value">{{ item.emp_formula }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Number of Atoms</div>
                    <div class="dp-value">68</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Electron Symmetry</div>
                    <div class="dp-value">2-A</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Charge</div>
                    <div class="dp-value">{{ item.mol_chrg }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Multiplicity</div>
                    <div class="dp-value">2</div>
                  </div>
                </b-card>
              </b-col>
              <b-col>
                <b-card style="margin-bottom: 50px;">
                  <div class="font-weight-bold" style="margin-bottom: 10px;">Related Data</div>
                  <a href="url">Molecule 1 V1</a><br/>
                  <a href="url">Molecule 1 V2</a>
                </b-card>
              </b-col>
            </b-row>
            <b-card style="margin-bottom: 50px;">
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
              <div class="dp-row">
                <div class="dp-key">Indexed Time</div>
                <div class="dp-value">{{ item.indexed_time }}</div>
              </div>
            </b-card>
          </b-col>
        </b-row>
      </b-container>
    </div>
  </div>
</template>

<script>
const {utils} = AiravataAPI;

export default {
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

<style>

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
</style>

